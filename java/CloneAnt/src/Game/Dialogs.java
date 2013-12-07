package Game;
/**
 * Dialogs provides an easy way to access Java swing dialogs in a static 
 * context.
 * 
 * @author Joseph Lewis <joehms22@gmail.com>
 * @version December 17, 2010
 * @license GNU GPL V 2 or higher.
 * Changelog:
 * July 30, 2009 Original
 * October 27, 2010 Made all methods static.
 * December 17, 2010 General cleanup.
 */

import javax.swing.filechooser.FileFilter;
import java.io.File;
import javax.swing.*;
import java.awt.Toolkit;

public class Dialogs
{

	/**
	 * Shows an open dialog that has an array of file extension options.
	 * 
	 * @param extensions (Each Element is An Acceptable extension, first is description)
	 * Example: ["images","jpg","png"]
	 * @param currentLocation The location to open the dialog to.  Blank is home folder.
	 * @param folderSelect  Should entire folders be selectable?
	 * @param folderShow  Should folders be shown? (to navigate, usually true)
	 * @param allFiles  Can the user choose any file (true) or just the ones you allowed
	 * in extensions?
	 * 
	 * @return The path of the file the user selected, null if user quit.
	 */
	public static String showSaveDialog(final String[] extensions, 
			String currentLocation, 
			boolean folderSelect, 
			final boolean folderShow, 
			boolean allFiles)
	{
		//JFileChooser fc = new JFileChooser();
		JFileChooser fileChooser = new JFileChooser();  //Starts the main file chooser and readies it

		fileChooser.addChoosableFileFilter(new FileFilter() 
		{
			public boolean accept(File f) 
			{
				//For each extension accept the files with it
				//I is set at 1 becasue the first element 0 is the Description
				for(int i = 1; i < extensions.length; i++)
					if(f.getName().endsWith(extensions[i]))
						return true;

				if(f.isDirectory() && folderShow) 
					return true;

				return false;
			}

			public String getDescription() 
			{ 
				return extensions[0];
			}
		}
		);

		if(folderSelect)
			fileChooser.setFileSelectionMode(JFileChooser.FILES_AND_DIRECTORIES);

		fileChooser.setAcceptAllFileFilterUsed(allFiles); 

		//Get the user option
		JFrame jf = new JFrame();
		int input = fileChooser.showSaveDialog(jf);
		String filePath = null;
		//If the user approves  a file get that filepath and send it
		if(input == JFileChooser.APPROVE_OPTION)
		{   
			File file = fileChooser.getSelectedFile();
			try 
			{
				filePath = file.getPath();
			}
			catch (Exception ex)
			{
				showErrorDialog("Save Error","Save Error:\nDid you move or delete\nthe file you are trying to open?\n"+ex);
			}
		}else{  //If the user canceled/quit
			filePath = null;
		}

		return filePath;
	}

	/**
	 * Shows an open dialog that has an array of file extension options.
	 * 
	 * @param extensions (Each Element is An Acceptable extension, first is description)
	 * Example: ["images","jpg","png"]
	 * @param currentLocation The location to open the dialog to.  Blank is home folder.
	 * @param folderSelect  Should entire folders be selectable?
	 * @param folderShow  Should folders be shown? (to navigate, usually true)
	 * @param allFiles  Can the user choose any file (true) or just the ones you allowed
	 * in extensions?
	 * 
	 * @return The path of the file the user selected, null if user quit.
	 */
	public static String showOpenDialog (final String[] extensions, 
			String currentLocation, 
			boolean folderSelect, 
			final boolean folderShow, 
			boolean allFiles)
	{
		//JFileChooser fc = new JFileChooser();
		JFileChooser fileChooser = new JFileChooser();//Starts the main file chooser and readies it
		fileChooser.addChoosableFileFilter(new FileFilter() 
		{
			public boolean accept(File f) 
			{
				//For each extension accept the files with it
				//I is set at 1 becasue the first element 0 is the Description
				for(int i = 1; i < extensions.length; i++)
					if(f.getName().endsWith(extensions[i]))
						return true;

				if(f.isDirectory() && folderShow)
					return true;

				return false;
			}

			public String getDescription() 
			{ 
				return extensions[0];
			}
		}
		);

		if(folderSelect)
			fileChooser.setFileSelectionMode(JFileChooser.FILES_AND_DIRECTORIES);

		fileChooser.setAcceptAllFileFilterUsed(allFiles); 

		//Get the user option
		JFrame jf = new JFrame();
		int input = fileChooser.showOpenDialog(jf);
		String filePath = null;
		//If the user approves  a file get that filepath and send it
		if(input == JFileChooser.APPROVE_OPTION)
		{   
			File file = fileChooser.getSelectedFile();
			try 
			{
				filePath = file.getPath();
			}
			catch (Exception ex)
			{
				showErrorDialog("Open Error","Open Error:\nDid you move or delete\nthe file you are trying to open?\n"+ex);
			}
		}else{
			filePath = null;
		}

		return filePath;
	}

	/**
	 * Shows a quit dialog and returns the option
	 *
	 * @return     option (yes no cancel)
	 */
	public static int showQuitDialog()
	{
		Toolkit.getDefaultToolkit().beep();
		JFrame jf = new JFrame();
		int n = JOptionPane.showConfirmDialog(jf, "Do you want to save before you quit?", "Quit?", JOptionPane.YES_NO_CANCEL_OPTION);
		return n;
	}

	/**
	 * Error Dialog - alerts the user of an error
	 *
	 * @param title The title for the dialog window.
	 * @param body The prompt of the window.
	 */
	public static void showErrorDialog(String title, String body)
	{
		JFrame jf = new JFrame();
		JOptionPane.showMessageDialog(jf, body, title, 
				JOptionPane.ERROR_MESSAGE);
	}

	/**
	 * Warning Dialog - alerts the user of an warning
	 *
	 * @param title The title for the dialog window.
	 * @param body The prompt of the window.
	 */
	public static void showWarningDialog(String title, String body)
	{
		JFrame jf = new JFrame();
		JOptionPane.showMessageDialog(jf, body, title, 
				JOptionPane.WARNING_MESSAGE);
	}

	/**
	 * Information Dialog - shows Information to the user
	 *
	 * @param title The title for the dialog window.
	 * @param body The prompt of the window.
	 */
	public static void showInformationDialog(String title, String body)
	{
		JFrame jf = new JFrame();
		JOptionPane.showMessageDialog(jf, body, title, 
				JOptionPane.INFORMATION_MESSAGE);
	}

	/**
	 * Yes/No Dialog - Requests the user to say yes or no.
	 *
	 * @param title The title for the dialog window.
	 * @param body The prompt of the window.
	 * 
	 * @return True if the user pressed yes, False on anything else.
	 */
	public static boolean showYesNoQuestionDialog(String title, String body)
	{
		JFrame jf = new JFrame();
		int n = JOptionPane.showConfirmDialog(jf, body, title, 
				JOptionPane.YES_NO_OPTION);
		return n == JOptionPane.YES_OPTION;
	}

	/**
	 * Show the dialog for user input.
	 * 
	 * @param title The title for the dialog window.
	 * @param body The prompt of the window.
	 * @return The text the user entered.
	 */
	public static String showUserInputDialog(String title, String body)
	{
		JFrame jf = new JFrame();
		return (String) JOptionPane.showInputDialog(jf, body, title, 
				JOptionPane.PLAIN_MESSAGE);
	}
}
