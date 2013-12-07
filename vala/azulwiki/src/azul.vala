/**
valac --pkg gtk+-3.0 --pkg sqlite3 --pkg glib-2.0 --pkg webkitgtk-3.0 --pkg gee-1.0 todo.vala settings.vala data_connection.vala
**/

using Gtk;

using GLib;
using Gee;
using WebKit;
using Granite;
using Gdk;

public class TreeViewSample : Gtk.Window 
{
	private ListStore		page_container;
	private DataConnection	data_source;
	private TreeView 		categories;
	private Entry			search_box;
	private string 			current_page_name = "";
	private string			current_document_name = "";
	private string 			settings_file_path = GLib.Environment.get_user_config_dir () + "/wiki.config";
	private SettingsFile 	settings_file;
	private WebView 		web_view;
	private Toolbar 		wiki_page_bar;
	private Label			document_title;
	private Granite.Widgets.AppMenu appmenu;
	private VBox			document_split;
	private string 			user_css = "data:text/css;base64," + Base64.encode("""
		body {
			background-color:#2a3b4c;
		}
	""".data);
	
    public TreeViewSample (string? user_path) 
    {
    	settings_file = new SettingsFile (settings_file_path);
    	
    	// Get the filepath from the saved settings file, the default, or the user.
    	current_document_name = GLib.Environment.get_user_config_dir ()  + "/default.wiki";
    	current_document_name = settings_file.get_value("lastopen", current_document_name);
    	current_page_name = settings_file.get_value("openpage","");
    	
    	if(user_path != "" && user_path != null)
    	{
    		current_document_name = user_path;
    		current_page_name = "";
    	}
        
        
        // Set up the window stuff.
        set_default_size (800, 600);
        destroy.connect (quit); // custom quit to save state
        
        
        // Set up the page chooser.
        page_container = new ListStore (1, typeof (string));
        
        categories = new TreeView.with_model (page_container);
        categories.headers_visible = false;
        categories.insert_column_with_attributes (-1, "Page", new CellRendererText (), "text", 0);
        
        update_categories ();
        categories.set_cursor (new TreePath.from_string("0:0"), categories.get_column(0), false);
        on_category_change ();
        categories.cursor_changed.connect (on_category_change);
        
        // Set up the webview the user will be editing from.
        document_split = new VBox (false, 0);
        
        document_title = new Label(current_page_name);
        document_split.pack_start(document_title, false, true, 0);
        
        web_view = new WebView ();
		web_view.editable = true;
		
		web_view.get_settings ().user_stylesheet_uri = user_css;
		
		

        var scroll = new ScrolledWindow (null, null);
        scroll.set_policy (PolicyType.AUTOMATIC, PolicyType.AUTOMATIC);
        scroll.add (this.web_view);
        document_split.pack_start(scroll, true, true, 0);
		
		var vbox = new VBox (false, 0);
		
		var keyGroup = new AccelGroup();
		
		// Setup the main appmenu for the application
		var menu = new Gtk.Menu ();
		var new_wiki_menu = new Gtk.MenuItem.with_label ("New Wiki...");
		new_wiki_menu.activate.connect (new_document);
		new_wiki_menu.add_accelerator("activate", keyGroup, 'N', Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE);
		
		var open_wiki_menu = new Gtk.MenuItem.with_label ("Open Wiki...");
		open_wiki_menu.activate.connect (open_document);
		open_wiki_menu.add_accelerator("activate", keyGroup, 'O', Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE);

		var fullscreen_menu = new ImageMenuItem.from_stock (Gtk.Stock.FULLSCREEN, keyGroup);
		fullscreen_menu.activate.connect (toggle_fullscreen);
		//fullscreen_menu.add_accelerator("activate", keyGroup, "F11", null, Gtk.AccelFlags.VISIBLE);

		var edit_menu = new Gtk.MenuItem.with_label ("Edit HTML...");
		edit_menu.activate.connect (on_edit_page);
		
		var quit_menu = new Gtk.MenuItem.with_label ("Quit");
		quit_menu.activate.connect (quit);
		quit_menu.add_accelerator("activate", keyGroup, 'Q', Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE);

		add_accel_group(keyGroup);

		menu.append (new_wiki_menu);
		menu.append (open_wiki_menu);
		menu.append (fullscreen_menu);
		menu.append (edit_menu);
		menu.append (quit_menu);
		
		appmenu = new Granite.Widgets.AppMenu(menu);
		
		// Setup the main toolbar for the application.
		var toolbar = new Toolbar();
		vbox.pack_start (toolbar, false, true, 0);
		toolbar.get_style_context ().add_class (STYLE_CLASS_PRIMARY_TOOLBAR);
		
		/**		
		//	New
		var new_button = new ToolButton.from_stock(Gtk.Stock.NEW);
		new_button.clicked.connect(new_document);
		toolbar.add(new_button);		
		
		//	Open
		var open_button = new ToolButton.from_stock(Gtk.Stock.OPEN);
		open_button.clicked.connect(open_document);
		toolbar.add(open_button);
		
		toolbar.add(new SeparatorToolItem()); // ---	
		**/
		
		//	The editor functions
    	add_script_tool_button(Gtk.Stock.PRINT, "window.print();", toolbar);

    	toolbar.add(new SeparatorToolItem()); // ---
		add_tool_button(Gtk.Stock.BOLD, "bold", toolbar);
		add_tool_button(Gtk.Stock.ITALIC, "italic", toolbar);
		add_tool_button(Gtk.Stock.UNDERLINE, "underline", toolbar);
		add_tool_button(Gtk.Stock.STRIKETHROUGH, "strikethrough", toolbar);
    	
    	toolbar.add(new SeparatorToolItem()); // ---
    	add_tool_button(Gtk.Stock.JUSTIFY_LEFT, "justifyleft", toolbar);
    	add_tool_button(Gtk.Stock.JUSTIFY_RIGHT, "justifyright", toolbar);
    	add_tool_button(Gtk.Stock.JUSTIFY_CENTER, "justifycenter", toolbar);
       	add_tool_button(Gtk.Stock.JUSTIFY_FILL, "justifyfull", toolbar); 	
    	
    	toolbar.add(new SeparatorToolItem()); // ---
    	add_tool_button(Gtk.Stock.INDENT, "insertUnorderedList", toolbar);
    	
    	
    	var ti = new ToolButton.from_stock(Gtk.Stock.INDENT);
    	ti.clicked.connect (() => {
       		insert_image();
    	});
    	toolbar.add(ti);
    	
		
		// An item to force the search bar to the right.
		var forceright = new ToolItem ();
		forceright.set_expand (true);
		toolbar.add(forceright);
		
		var searchitem = new ToolItem ();
		search_box = new Entry ();
		search_box.set_placeholder_text ("Search") ;
		search_box.get_buffer ().inserted_text.connect (on_search_changed);
		search_box.get_buffer ().deleted_text.connect (on_search_changed);
		searchitem.add(search_box);
		toolbar.add(searchitem);
		
    	toolbar.add(appmenu);
		
		
		// The editor for the wiki stuff, below the wiki pane.
		wiki_page_bar = new Toolbar ();
		wiki_page_bar.set_icon_size (IconSize.SMALL_TOOLBAR);
		
		//	Add
		var add_button = new ToolButton.from_stock(Gtk.Stock.ADD);
		add_button.clicked.connect(on_add_category);
		wiki_page_bar.add(add_button);	
		
		//	Delete
		var del_button = new ToolButton.from_stock(Gtk.Stock.DELETE);
		del_button.clicked.connect(on_delete_category);
		wiki_page_bar.add(del_button);
		
		var leftbox = new VBox (false,0);
		leftbox.pack_start (categories, true, true, 0);
		leftbox.pack_start (wiki_page_bar, false, true, 0);
		
		
		var hbox = new Paned (Orientation.HORIZONTAL);
        hbox.add1 (leftbox);
        hbox.add2 (document_split);	// The webview in its cozy scroller
        
        hbox.set_position (200); // TODO save between sessions
        
        vbox.pack_start (hbox, true, true, 0);
        add (vbox);
        
        
        
        // Set up the data-soruce
		open_file (current_document_name);
    }
    
    public void show_error(string? s)
	{
		if(s != null && s != "")
		{
			var dialog = new Gtk.MessageDialog(null,Gtk.DialogFlags.MODAL,Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "%s",s);
			dialog.set_title("Error");
			dialog.run();
			dialog.destroy();
		}
	}
    
    private bool is_fullscreen = false;
    public void toggle_fullscreen ()
    {
		if( is_fullscreen )
			unfullscreen ();
		else
			fullscreen ();
		
		is_fullscreen = ! is_fullscreen;	
	}
    
    public void on_search_changed()
    {
		update_categories ();
		
		highlight_text ();
	}
	
	public void highlight_text ()
	{
		string searchbox_val = search_box.get_buffer().get_text ();
		
		if(searchbox_val != "" && searchbox_val != null)
		{
			web_view.unmark_text_matches ();
			web_view.mark_text_matches (searchbox_val, false, 1000);
			web_view.set_highlight_text_matches (true);
		}
		else
		{
			web_view.unmark_text_matches ();
			web_view.set_highlight_text_matches (false); 
		}
	}
    
    /**
    def on_select_font(self, action):
dialog = gtk.FontSelectionDialog("Select a font")
if dialog.run() == gtk.RESPONSE_OK:
fname, fsize = dialog.fontsel.get_family().get_name(), dialog.fontsel.get_size()
self.editor.execute_script("document.execCommand('fontname', null, '%s');" % fname)
self.editor.execute_script("document.execCommand('fontsize', null, '%s');" % fsize)
dialog.destroy()
def on_select_color(self, action):
dialog = gtk.ColorSelectionDialog("Select Color")
if dialog.run() == gtk.RESPONSE_OK:
gc = str(dialog.colorsel.get_current_color())
color = "#" + "".join([gc[1:3], gc[5:7], gc[9:11]])
self.editor.execute_script("document.execCommand('forecolor', null, '%s');" % color)
dialog.destroy()
**/
	
	/**
	Opens a new file
	**/
	public void open_file(string filepath)
	{
	    stderr.printf ("Opening new file: %s\n", filepath);
	    
		current_document_name = filepath;
		current_page_name = "";
		data_source = new DataConnection (current_document_name);
		
		// Set the categories.
        clear_searchbar ();
        update_categories ();
        update_page_view ();
        
        // Set window title
        title = "AzulWiki - " + current_document_name;
	}
	
	
	
	public void clear_searchbar()
	{
		search_box.get_buffer ().delete_text(0,-1);
	}
    
    
    
    public void apply_format(string formatname)
    {
    	web_view.execute_script("document.execCommand('"+formatname+"', false, false);");
    }
    
    
    
    public void insert_image()
    {
		var dialog = new FileChooserDialog("Select an image file", this, 
				FileChooserAction.OPEN, Gtk.Stock.CANCEL, Gtk.ResponseType.CANCEL, 
				Gtk.Stock.OPEN, Gtk.ResponseType.OK, null);
			
		if(dialog.run() == Gtk.ResponseType.OK)
		{
			string fn = dialog.get_filename();
			web_view.execute_script("document.execCommand('insertImage', null, '"+fn+"');");
		}
		dialog.destroy();
    }
    
    
    
    public void add_tool_button(string stock_item, string fmt_str, Toolbar tb)
    {
   		ToolButton ti;
    	ti = new ToolButton.from_stock(stock_item);
    	ti.clicked.connect (() => {
    		apply_format(fmt_str);
    	});
    	tb.add(ti);
    }
    
    
    
    public void add_script_tool_button(string stock_item, string fmt_str, Toolbar tb)
    {
   		ToolButton ti;
    	ti = new ToolButton.from_stock(stock_item);
    	ti.clicked.connect (() => {
       		web_view.execute_script(fmt_str);
    	});
    	tb.add(ti);
    }
    
    
    
    public void new_document()
    {
    	save_changes();
    	var fcd = new FileChooserDialog ("New Wiki", this, FileChooserAction.SAVE,  
    									Stock.CANCEL, ResponseType.CANCEL,
                                      	Stock.NEW, ResponseType.ACCEPT);
    	var wiki_filter = new FileFilter();
		wiki_filter.add_pattern ("*.wiki");
		wiki_filter.set_filter_name ("AzulWiki Files");
    	fcd.add_filter (wiki_filter);
    	fcd.select_filename (current_document_name);
    	
    	if(fcd.run() == ResponseType.ACCEPT)
    		open_file (fcd.get_filename());
    	
		fcd.destroy();
    }
    
    
    
    public void open_document()
    {
    	save_changes();
    	var fcd = new FileChooserDialog ("Open Wiki", this, FileChooserAction.OPEN,
    									Stock.CANCEL, ResponseType.CANCEL,
                                      	Stock.OPEN, ResponseType.ACCEPT); 
		var wiki_filter = new FileFilter();
		wiki_filter.set_filter_name("AzulWiki Files");
		wiki_filter.add_pattern("*.wiki");
    	fcd.add_filter(wiki_filter);
    	fcd.select_filename (current_document_name);
    	
    	if(fcd.run() == ResponseType.ACCEPT)
    		open_file(fcd.get_filename());

    	fcd.destroy ();
    }
    
    
    
    public void quit()
    {
    	hide ();
    	save_changes ();
    	settings_file.set_value ("openpage", current_page_name);
    	settings_file.set_value ("lastopen", current_document_name);
    	
    	data_source.compact_database ();
    	Gtk.main_quit ();
    }
    
    
    
    /**
    Updates the list of pages.
    **/
    public string[] update_categories()
    {
        stderr.printf ("Updating categories\n");
		page_container.clear();
		
		TreeIter iter;

		string[] rows;
		string search_box_val = search_box.get_buffer().get_text ();
		
		stderr.printf ("Searchbox is: %s\n", search_box_val);
		// If the search bar isn't empty, filter it
		if(search_box_val == "" || search_box_val == null)
			rows = data_source.read_categories();
		else
			rows = data_source.search_categories(search_box_val + "*"); // Search for all matches
			
		stderr.printf ("Updating page container");
        foreach(string s in rows)
        {
            page_container.append (out iter);
        	page_container.set (iter, 0, s);
        }
        
        return rows;
	}
    
    
    
    public void on_add_category () 
    {
        stderr.printf ("on_add_category called\n");
    	save_changes();
    	Dialog d = new Dialog.with_buttons ("New Category", this, DialogFlags.MODAL, Gtk.Stock.OK, 1, "Cancel", 2, null);
    	
    	Entry e = new Entry();
    	var content = d.get_content_area () as Box;
    	content.pack_start(new Label("Enter category name:"));
		content.pack_start(e);
		content.show_all();
		d.show_all();
    	d.add_action_widget(new Entry(),3);

       	d.response.connect((responseid) => {
        	if(responseid == 1)
        	{
        		string new_category_name = e.get_buffer().get_text();
        		this.data_source.create_category(new_category_name);
				clear_searchbar ();
        		update_categories();
        		
        		// Update the view to the new page.
        		save_changes ();
        		current_page_name = new_category_name;
        		update_page_view ();
        	}
			d.destroy();
   		 });
    	d.run();
	}
	
	
	
	public void on_edit_page () 
    {
    	if(current_page_name == null || current_page_name == "")
    	{
    		show_error("You must open a page before editing it!");
    		return;
    	}
    	
        stderr.printf ("on_edit_page called\n");
    	save_changes();
    	Dialog d = new Dialog.with_buttons ("Edit Page", this, DialogFlags.MODAL, Gtk.Stock.OK, 1, "Cancel", 2, null);
    	
    	TextView e = new TextView();
    	var scroll = new ScrolledWindow (null, null);
        scroll.set_policy (PolicyType.AUTOMATIC, PolicyType.AUTOMATIC);
        scroll.add (e);
        
    	var content = d.get_content_area () as Box;
		content.pack_start(scroll);
		content.show_all();
		d.show_all();
    	d.add_action_widget(new Entry(),3);
    	
    	string curr_val = data_source.read_text (current_page_name);
    	e.get_buffer().set_text(curr_val);

       	d.response.connect((responseid) => {
        	if(responseid == 1)
        	{
        		TextIter start;
        		TextIter end;
        		e.get_buffer().get_start_iter (out start);
        		e.get_buffer().get_end_iter (out end);
        		
        		string val = e.get_buffer().get_text(start, end, false);
        		
        		// Update the view to the new page.
        		data_source.update_text (current_page_name, val);
        		
        		update_page_view ();
        	}
			d.destroy();
   		 });
    	d.run();
	}



	/**
	 * Saves the changes to the currently edited text.
	 */
	public void save_changes ()
	{
		stderr.printf ("Saving changes to %s\n", current_page_name);
		if(this.current_page_name != null && this.current_page_name != "")
		{
			web_view.execute_script("document.title='';document.title=document.documentElement.innerHTML;");
			string val = web_view.get_main_frame().get_title();

			data_source.update_text(current_page_name, val);
		}
	}
	
	
	
	public void on_delete_category () 
	{
		save_changes ();
	    stderr.printf ("Deleting category\n");
		
		data_source.delete_category (current_page_name);
		
		current_page_name = null;
		update_categories ();
		update_page_view ();
	}
	
	
	public void on_category_change ()
	{
		TreeModel m;
		TreeIter i;
		GLib.Value val;

		categories.get_selection().get_selected(out m, out i);
		m.get_value(i, 0, out val);

		if(val.type() == typeof(string) && (string) val != current_page_name)
		{
			save_changes();
			stderr.printf ("on_category_change called\n");
	
			current_page_name = (string) val;
			update_page_view();
		}
	}
	
	
	public void update_page_view ()
	{
		web_view.get_settings ().user_stylesheet_uri = user_css;
		if(current_page_name == null || current_page_name == "" ||
			!data_source.category_exists (current_page_name))
		{
			web_view.set_sensitive (false);
			
			// Update the page title
			document_title.set_text ("Create a page to begin editing");
			web_view.load_html_string ("<html><body style='background-color:#999;'></body></html>", "file:///");
			
			return;
		}
		web_view.set_sensitive (true);
		
		stderr.printf ("updating page view to: %s\n", current_page_name);
		
		// Load the page
		string inner = data_source.read_text (current_page_name);
		web_view.load_html_string (inner, "file:///");
		
		// Update the page title
		document_title.set_text (current_page_name);
		
		// Highlight the desired text
		highlight_text ();
	}


    public static int main (string[] args)
    {     
        Gtk.init (ref args);
        
       	string path = null;
       	if(args.length != 1 && ! args[1].has_prefix("-"))
       		path = args[1];
       	
        var sample = new TreeViewSample (path);
        sample.show_all ();
        Gtk.main ();

        return 0;
    }
}
