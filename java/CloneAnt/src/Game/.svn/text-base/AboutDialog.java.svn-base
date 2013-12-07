package Game;

import java.awt.Component;
import java.awt.ScrollPane;
import java.io.InputStream;
import java.util.Scanner;

import javax.swing.*;

public class AboutDialog extends JFrame
{

	private static final long serialVersionUID = 1L;

	public AboutDialog()
	{
		setSize(600, 500);
		setTitle("About CloneAnt");
		
		JTabbedPane tabbedPane = new JTabbedPane();
		tabbedPane.addTab("General", buildGeneral());
		tabbedPane.addTab("License", buildLicense());

		add(tabbedPane);
		setLocationRelativeTo(null);
		setVisible(true);

	}
	
	public Component buildLicense()
	{
		JTextArea l = new JTextArea();
		ScrollPane w = new ScrollPane();
		w.add(l);
		
		Scanner gpl;
		InputStream rsc = AboutDialog.class.getResourceAsStream("/resources/gpl.txt");

		String text = "";
		gpl = new Scanner( rsc );
		gpl.useDelimiter("\n");
		while(gpl.hasNext())
			text += gpl.next()+"\n";
		l.setText(text);
		l.setEditable(false);
		return w;
	}
	
	public Component buildGeneral()
	{
		JEditorPane l = new JEditorPane();
		ScrollPane w = new ScrollPane();
		w.add(l);
		
		String text = "";
		text += "<html><div align=\"center\"><h1>CloneAnt</h1><br> Copyright (c) 2011 Joseph Lewis &lt;joehms22@gmail.com&gt;<br>";
		text += "Licensed under the GNU GPL Version 2<br>";
		text += "Contact Joseph for the source.</div><br>";
		text += "<h2>Coders:</h2><ul><li>Joseph Lewis &lt;joehms22@gmail.com&gt;</li></ul>";
		text += "<h2>Artwork:</h2><ul><li>Joseph Lewis &lt;joehms22@gmail.com&gt;</li></ul>";
		text += "<h2>Notes:</h2>Based upon the game SimAnt which was created by Maxis in 1991.<br>\n";
		text += "<p>Built as a project for COMP 2673, taught by Dr. Jeffrey Edgington, at the University of Denver</p></html>";

        l.setContentType("text/html"); // lets Java know it will be HTML                  
		l.setText(text);
		l.setPreferredSize(w.getPreferredSize());
		
		l.setEditable(false);
		return w;
	}
}
