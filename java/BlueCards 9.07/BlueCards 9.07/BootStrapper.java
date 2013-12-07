/**
 * BootStrapper Starts the Program
 * 
 * @author Joseph Lewis 
 * @version July 29, 2009
 */ 

import javax.swing.UIManager; // allows for look and feel of windows

public class BootStrapper
{
    public static void main(String[] args)
    {
        //Set to look like windows:
        try 
        {
            UIManager.setLookAndFeel(
            "com.sun.java.swing.plaf.windows.WindowsLookAndFeel");
        } 
        catch (Exception e){};
          
        new MainWindow();
        
    }
}