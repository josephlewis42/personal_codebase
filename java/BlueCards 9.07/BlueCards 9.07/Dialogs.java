
/**
 * Dialogs provides a set of nice dialogs to go with the program
 * 
 * @author Joseph Lewis 
 * @version July 30, 2009
 */

import javax.swing.JFileChooser;
import javax.swing.filechooser.FileFilter;
import java.io.File;
import javax.swing.*;
import javax.swing.JOptionPane;
import java.awt.Toolkit;

public class Dialogs extends JFrame
{


    /**
     * Constructor for objects of class Dialogs
     */
    public Dialogs()
    {
        
    }
    
   /**
    * Show Save Dialog shows an open dialog that has an array of
    * file extention options
    * @param string[] (Each Element is An Acceptable extention, first is description)
    * @param boolean  if entire folders are selectable
    * @param boolean  if folders are shown (to navigate) but not selctable
    * @param boolean  all files is acceptable
    * @return filePath
    * This will be null if the user quit the dialog
    */
   public String showSaveDialog (final String[] extentions, String currentLocation, boolean folderSelect, final boolean folderShow, boolean allFiles)
   {
       JFileChooser fc = new JFileChooser();
       JFileChooser fileChooser = new JFileChooser();//Starts the main file chooser and readies it
       fileChooser.addChoosableFileFilter(new FileFilter() 
       {
           public boolean accept(File f) 
           {
               boolean b = false;
               //For each extention accept the files with it
               //I is set at 1 becasue the first element 0 is the Description
               for(int i = 1; i < extentions.length; i++)
               {
                   if(f.getName().endsWith(extentions[i])){b = true;}
               }
                
                if(f.isDirectory() && folderShow) { b = true;}
                return b;
            }

            public String getDescription() { return extentions[0];}
        }
        );

        if(folderSelect){fc.setFileSelectionMode(JFileChooser.FILES_AND_DIRECTORIES);}
        fc.setAcceptAllFileFilterUsed(allFiles); 

        //Get the user option
        int input = fileChooser.showSaveDialog(this);
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
        }
        if(input != JFileChooser.APPROVE_OPTION)//If the user canceled/quit
        {
            filePath = "";
        }

        return filePath;
    }
        
        /**
         * Show Open Dialog shows an open dialog that has an array of
         * file extention options
         * @param string[] (Each Element is An Acceptable extention, first is description)
         * @param boolean  if entire folders are selectable
         * @param boolean  if folders are shown (to navigate) but not selctable
         * @param boolean  all files is acceptable
         * @return filePath
         * This will be null if the user quit the dialog
         */
        public String showOpenDialog (final String[] extentions, String currentLocation, boolean folderSelect, final boolean folderShow, boolean allFiles)
        {
            JFileChooser fc = new JFileChooser();
            JFileChooser fileChooser = new JFileChooser();//Starts the main file chooser and readies it
                fileChooser.addChoosableFileFilter(new FileFilter() 
                {
                    public boolean accept(File f) 
                    {
                        boolean b = false;
                        //For each extention accept the files with it
                        //I is set at 1 becasue the first element 0 is the Description
                        for(int i = 1; i < extentions.length; i++)
                        {
                            if(f.getName().endsWith(extentions[i])){b = true;}
                        }
                        
                        if(f.isDirectory() && folderShow) { b = true;}
                        return b;
                    }

                    public String getDescription() { return extentions[0];}
                }
            );
       
            if(folderSelect){fc.setFileSelectionMode(JFileChooser.FILES_AND_DIRECTORIES);}
            fc.setAcceptAllFileFilterUsed(allFiles); 
            
            //Get the user option
            int input = fileChooser.showOpenDialog(this);
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
        public int showQuitDialog()
        {
            Toolkit.getDefaultToolkit().beep();
            int n = JOptionPane.showConfirmDialog(this,"Do you want to save before you quit?","Quit?",JOptionPane.YES_NO_CANCEL_OPTION);
            return n;
        }
        
        /**
         * Error Dialog - allerts the user of an error
         *
         * @param A string to tell the user of the error title,body
         */
        public void showErrorDialog(String title, String body)
        {
            JOptionPane.showMessageDialog(this,body,title,JOptionPane.ERROR_MESSAGE);
        }
        
        /**
         * Warning Dialog - allerts the user of an warning
         *
         * @param A string to tell the user of the warning title,body
         */
        public void showWarningDialog(String title, String body)
        {
            JOptionPane.showMessageDialog(this,body,title,JOptionPane.WARNING_MESSAGE);
        }
        
        /**
         * Information Dialog - shows Information to the user
         *
         * @param A string to tell the user of the information title,body
         */
        public void showInformationDialog(String title, String body)
        {
            JOptionPane.showMessageDialog(this,body,title,JOptionPane.INFORMATION_MESSAGE);
        }
        
        /**
         * Yes/No Dialog - shows Information to the user
         *
         * @param A string to tell the user of the question title,body
         * @return The values for this integer are YES_OPTION, NO_OPTION, CANCEL_OPTION, OK_OPTION, and CLOSED_OPTION
         */
        public int showYesNoQuestionDialog(String title, String body)
        {
            int n = JOptionPane.showConfirmDialog(this,body,title,JOptionPane.YES_NO_OPTION);
            return n;
        }
}