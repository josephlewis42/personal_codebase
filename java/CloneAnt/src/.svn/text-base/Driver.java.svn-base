public class Driver
{
	/**
	 * We all know what this does!
	 * 
	 * @param args - No Params for the game yet.
	 */
	public static void main(String[] args)
	{
		// Create a game for the gui to use.
		final Game g = new Game();
		
		// Start the GUI in a thread.
		javax.swing.SwingUtilities.invokeLater(new Runnable()
		{
			public void run()
			{
				MainWindow.createAndShowGUI(g);
			}
		});
		
		// Start the main game in this thread as a daemon so it dies
		// when the GUI does.
		g.setDaemon(true);
		g.start();
	}
}