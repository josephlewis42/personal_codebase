/**
Allows a file to connect to the database.
**/
using Sqlite;
using Gtk;

public class DataConnection
{	
	private Database db;
	private string welcome_message = """<html><body><h1>Welcome to AzulWiki!</h1></body></html>""";
	
	public DataConnection(string location)
	{
		int rc;
		
        rc = Database.open (location, out db);

        if (rc != Sqlite.OK) {
            show_error ("Can't open database: %d, %s\n".printf( rc, db.errmsg ()));
        }
        
        // Setup database if needed.
        db.exec("CREATE VIRTUAL TABLE Pages USING fts3(title TEXT UNIQUE, page TEXT, deleted INTEGER);");
	}

	public void delete_category(string catname)
	{
		if(catname == null)
			return;
			
		Statement stmt;
		if(db.prepare_v2 ("UPDATE Pages SET deleted = 1 WHERE title = ?", -1, out stmt) != 0) 
		{
			show_error("Couldn't delete the category: " + db.errmsg ());
			return;
		}
		
		stmt.bind_text(1, catname);
	
		if(stmt.step() != Sqlite.DONE)
			show_error("Couldn't delete the category: " + catname);
	}
	
	public void undelete_category(string catname)
	{
		if(catname == null)
			return;
			
		Statement stmt;
		if(db.prepare_v2 ("UPDATE Pages SET deleted = 0 WHERE title = ?", -1, out stmt) != 0) 
		{
			show_error("Couldn't undelete the category: " + db.errmsg ());
			return;
		}
		
		stmt.bind_text(1, catname);
	
		if(stmt.step() != Sqlite.DONE)
			show_error("Couldn't undelete the category: " + catname);
	}
	
	public string[] read_categories()
	{
    	Statement stmt;
    	int rc = 0;


		if ((rc = db.prepare_v2 ("SELECT title FROM Pages WHERE deleted=0;", -1, out stmt, null)) == 1) {
		    printerr ("SQL error: %d, %s\n", rc, db.errmsg ());
		    return new string[]{"Database","Error","Occured"};
		}
		
		int rows;
		for(rows = 0; stmt.step() != Sqlite.DONE; rows++);
		stmt.reset();
		
    	
    	string[] output = new string[rows];
    	
    	for(int i = 0; i < rows; i++)
    	{
			stmt.step();
			output[i] = stmt.column_text(0);
		}
		
		return output;
	}
	
	public void rebuild_index ()
	{
		db.exec("INSERT INTO Pages(Pages) VALUES('rebuild');");
	}

	// Reads categories with a custom search string.
	public string[] search_categories(string search)
	{
		// If no search params, return everything we have.
		if(search == null || search == "")
			return read_categories();
	
		stderr.printf("Searching categories for %s\n", search);
    	Statement stmt;
    	int rc = 0;

		if ((rc = db.prepare_v2 ("SELECT title FROM Pages WHERE deleted=0 AND Pages MATCH ?;", -1, out stmt, null)) == 1) {
		    printerr ("SQL error: %d, %s\n", rc, db.errmsg ());
		    return new string[]{"Database","Error","Occured"};
		}
		
		stmt.bind_text(1, search);
		
		int rows;
		int stepval;
		for(rows = 0; (stepval = stmt.step()) == Sqlite.ROW; rows++);
		
		if(stepval != Sqlite.DONE)
		{
			stderr.printf(db.errmsg());
			rebuild_index ();
			//return search_categories (search);
		}
		stmt.reset();
    	
    	string[] output = new string[rows];
    	
    	for(int i = 0; i < rows; i++)
    	{
			stmt.step();
			output[i] = stmt.column_text(0);
		}
		
		return output;
	}
	
	
	public void compact_database()
	{
		db.exec("INSERT INTO Pages(Pages) VALUES('optimize');");
		db.exec("VACUUM;");
	}

	public void show_error(string? s)
	{
		if(s != null && s != "")
		{
			var dialog = new Gtk.MessageDialog(null,Gtk.DialogFlags.MODAL,Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "%s",s);
			dialog.set_title("Database Error");
			dialog.run();
			dialog.destroy();
		}
	}
	
	public bool category_exists(string catname)
	{
		if(catname == null)
			return false;
			
		Statement stmt;
		if(db.prepare_v2 ("SELECT title FROM Pages WHERE title = ?;", -1, out stmt) != 0) 
		{
			show_error(db.errmsg ());
			return true;
		}
		
		stmt.bind_text(1, catname);
	
		return stmt.step() == Sqlite.ROW;
	}

	public bool category_deleted(string catname)
	{
		if(catname == null)
			return false;
			
		Statement stmt;
		if(db.prepare_v2 ("SELECT title FROM Pages WHERE title = ? AND deleted = 1;", -1, out stmt) != 0) 
		{
			show_error(db.errmsg ());
			return true;
		}
		
		stmt.bind_text(1, catname);
	
		return stmt.step() == Sqlite.ROW;
	}
	
	public void create_category(string catname)
	{
		if(catname == null)
			return;
			
		if(category_exists (catname))
		{
			show_error("That page already exists, try another name.");
			undelete_category (catname);
			return;
		}
			
		Statement stmt;
		if(db.prepare_v2 ("INSERT INTO Pages VALUES (?, '',0);", -1, out stmt) != 0) 
		{
			show_error("Couldn't create the page: " + db.errmsg ());
			return;
		}
		
		stmt.bind_text(1, catname);
	
		if(stmt.step() != Sqlite.DONE)
			show_error("Couldn't create the page: " + catname);
	}
	
	/**
	 * Updates the text in the given category.
	 */
	public void update_text(string catname, string text)
	{
		if(catname == null || catname == "")
			return;
		
		if(text == null)
			return;
			
		Statement stmt;
		if(db.prepare_v2 ("UPDATE Pages SET page = ? WHERE title = ? AND deleted = 0;", -1, out stmt) != 0) 
		{
			show_error("Couldn't update the text:" + db.errmsg ());
			return;
		}
		
		stmt.bind_text(1, text);
		stmt.bind_text(2, catname);
	
		if(stmt.step() != Sqlite.DONE)
			show_error("Couldn't update the text: " + catname);
	}
	
	/**
	 * Reads the text for the given category.
	 */
	public string read_text(string catname)
	{
		if(catname == null || catname == "")
			return welcome_message;
			
		Statement stmt;
		if(db.prepare_v2 ("SELECT page FROM Pages WHERE title = ?;", -1, out stmt) != 0) 
		{
			show_error(db.errmsg ());
			return "";
		}
		
		stmt.bind_text(1, catname);
	
		if(stmt.step() != Sqlite.ROW)
		{
			show_error("Couldn't read the text: " + catname);
			return "";
		}

		return stmt.column_text(0);
	}
}
