package Game;

import javax.swing.JApplet;
import javax.swing.UIManager;

public class Applet extends JApplet
{
	private static final long serialVersionUID = 1L;

	public Applet()
	{
		setContentPane(new MainWindowContainer(this));
	}
	
	public void init()
	{
		try {
			// Set System look and feel.
			UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
		} catch (Exception e) {
			System.err.println("Look and feel exception, ignoring.");
		}
	}
}
