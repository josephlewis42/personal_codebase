package Game;

import javax.swing.JFrame;
import javax.swing.UIManager;

public class SwingSet extends JFrame
{
	private static final long serialVersionUID = -4568445609586612020L;

	/**
	 * Create the GUI and show it.
	 */
	public SwingSet()
	{
		try
		{
			// Set System look and feel.
			UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
		} catch (Exception e)
		{
			System.err.println("Look and feel exception, ignoring.");
		}

		// Create and set up the window.
		setTitle("CloneAnt");
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

		// Create and set up the content pane.
		setContentPane( new MainWindowContainer(this));

		// Display the window.
		pack();
		setVisible(true);
	}
	
	public static void main(String[] args)
	{
		new SwingSet();
	}
}
