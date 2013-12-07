/**
Provides a utility to read and write .ini style settings files.
**/

public class SettingsFile
{
	private Gee.HashMap<string,string> settings_map = new Gee.HashMap<string, string>();
	private File m_file;
	
	public SettingsFile(string location)
	{
		// A reference to our file
		this.m_file = File.new_for_path (location);

		if (!m_file.query_exists ()) 
		{
			stderr.printf("File '%s' doesn't exist.\n", this.m_file.get_path ());
			return;
		}

		try 
		{
		    // Open file for reading and wrap returned FileInputStream into a
		    // DataInputStream, so we can read line by line
		    var dis = new DataInputStream (this.m_file.read ());
		    string line;
		    
		    // Read lines until end of file (null) is reached
		    while ((line = dis.read_line (null)) != null) 
		    {
		        string start = line.split("=")[0];
		        string end = line.split("=")[1];
		        this.settings_map.set(start,end);
		        stderr.printf("\t%s -> %s \n", start, end);
		    }
		    dis.close();
		} catch (Error e) {
		    error ("%s", e.message);
		}
	}
	
	public void write_file()
	{
		try 
		{
		    // Open file for reading and wrap returned FileInputStream into a
		    // DataInputStream, so we can read line by line
		    if (this.m_file.query_exists ()) 
			{
			    this.m_file.delete();
			}


		    var dis = new DataOutputStream (this.m_file.create (FileCreateFlags.REPLACE_DESTINATION));

		     foreach (var entry in this.settings_map.entries) {
       			dis.put_string(entry.key + "=" + entry.value+"\n");
   			 }
		    
		} catch (Error e) {
		    error ("%s", e.message);
		}
	}
	
	public string get_value(string key, string def)
	{
		var val = this.settings_map[key];
		if(val == null)
			return def;
		return val;
	}
	
	public void set_value(string key, string val)
	{
		this.settings_map[key] = val;
		write_file();
	}
}
