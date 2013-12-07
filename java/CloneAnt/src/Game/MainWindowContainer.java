package Game;

import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

/**
 * The MainWindow provides a Swing interface to the game backend. It is
 * responsible for providing a drawing surface for the tiles and characters.
 * 
 * @author Joseph Lewis <joehms22@gmail.com>
 */
public class MainWindowContainer extends Container implements MouseListener, ActionListener
{
	private static final long serialVersionUID = 6680845837845480095L;

	private JPanel drawingPane;
	
	private JToolBar toolBar;
	private JButton redHome, blackHome, surface, myAnt;
	private JScrollPane scroller;
	private JRadioButtonMenuItem slow, med, fast, lightning, africanswallow;
	private JMenuItem callFive, callTen, releaseFive, releaseTen, releaseAll, about, newGame;
	private JCheckBoxMenuItem paused;
	private JLabel numAnts;

	private Game myGame; // Used to pass in drawing information

	// Used in the double clicking madness.
	private boolean wasDoubleClick;
	private int clickX, clickY;

	
	/**
	 * Creates a new MainWindow whose parentFrame is given by parentFrame and
	 * whose game it controls is g.
	 * 
	 * @param parentFrame
	 *            - The owner of this window.
	 * @param g
	 *            - The game this frame displays.
	 */
	public MainWindowContainer(RootPaneContainer parentFrame)
	{
		setLayout(new BorderLayout());
		
		// Set up the toolbar.
		toolBar = new JToolBar("Still draggable");
		toolBar.setOrientation(javax.swing.SwingConstants.VERTICAL);
		addButtons(toolBar);
		toolBar.setFloatable(false);
		
		// Set up menubar.
		JMenuBar menu = setupMenu();

		// Set up the drawing area.
		drawingPane = new DrawingPane();
		drawingPane.setBackground(Color.black);
		drawingPane.addMouseListener(this);

		// Put the drawing area in a scroll pane.
		scroller = new JScrollPane(drawingPane);
		scroller.setPreferredSize(new Dimension(800, 600));

		// Lay out this demo.
		add(menu, BorderLayout.PAGE_START);
		add(toolBar, BorderLayout.LINE_START);
		add(scroller, BorderLayout.CENTER);
		
		// Start the main game in this thread as a daemon so it dies
		// when the GUI does.
		setUpGame();
	}
	
	/**
	 * Creates and sets up a new game.
	 */
	private void setUpGame()
	{
		boolean cont = false;
		
		if(myGame != null)
			cont = Dialogs.showYesNoQuestionDialog("New Game", "Starting a new game will exit your current one, continue?");
		else
			cont = true;
		
		if(! cont)
			return;
		
		myGame = new Game();
		myGame.setDaemon(true);
		myGame.start();

		myGame.setDrawingPane(drawingPane);
		myGame.setAntCount(numAnts);
	}

	// Adds the buttons to the toolbar.
	private void addButtons(JToolBar t)
	{
		surface = makeButton("surface.jpg", "Go to the surface.", "Surface");
		blackHome = makeButton("black_nest.jpg", "Go to the black nest.",
				"Black");
		redHome = makeButton("red_nest.jpg", "Go to the red nest.", "Red");
		myAnt = makeButton("yellow_ant.png", "View my player.", "Player");

		t.add(surface);
		t.add(blackHome);
		t.add(redHome);
		t.addSeparator();
		t.add(myAnt);
		t.addSeparator();
		
		t.add(new JLabel("<html><b>Ants</b></html>"));
		numAnts = new JLabel();
		t.add(numAnts);
	}

	/**
	 * Makes a new JButton with an image
	 * 
	 * Copyright Oracle, under an MIT License.
	 * http://download.oracle.com/javase/
	 * tutorial/uiswing/components/toolbar.html
	 * 
	 * @param imageName
	 *            - The image to read.
	 * @param toolTipText
	 *            - The tooltip for the
	 * @param altText
	 *            - The text to use if the image isn't found.
	 * @return A button.
	 */
	private JButton makeButton(String imageName, String toolTipText, String altText)
	{
		Image myImg = ImageLoader.getImage("/images/interface/" + imageName);

		// Create and initialize the button.
		JButton button = new JButton();
		button.setToolTipText(toolTipText);
		button.addActionListener(this);

		if (myImg != null)
			button.setIcon(new ImageIcon(myImg, altText));
		else
			button.setText(altText);

		return button;
	}

	/**
	 * Makes a new menu button and returns it.
	 * 
	 * @param name
	 *            - The string for this button.
	 * @param mnemonic
	 *            - The mnemonic letter for this button.
	 * @param ks
	 *            - The keystroke for this item.
	 * @return
	 */
	private JMenuItem makeMenuButton(String name, int mnemonic, KeyStroke ks)
	{
		JMenuItem b = new JMenuItem(name);
		b.setMnemonic(mnemonic);
		b.addActionListener(this);
		b.setAccelerator(ks);
		return b;
	}

	private JRadioButtonMenuItem makeRadioMenuItem(String name, int mnemonic,
			KeyStroke ks, ButtonGroup g)
	{
		JRadioButtonMenuItem b = new JRadioButtonMenuItem(name);
		b.setMnemonic(mnemonic);
		b.addActionListener(this);
		b.setAccelerator(ks);
		g.add(b);
		return b;
	}

	/**
	 * Creates a menu bar for the window.
	 * 
	 * @return The window's menu bar.
	 */
	public JMenuBar setupMenu()
	{
		// Create the menu bar.
		JMenuBar menuBar = new JMenuBar();

		// Build the first menu.
		JMenu menu = new JMenu("Clone Ant");
		menu.setMnemonic(KeyEvent.VK_C);
		menuBar.add(menu);
		
		newGame = makeMenuButton("New Game", 0, null);
		menu.add(newGame);
		
		menu.addSeparator();

		paused = new JCheckBoxMenuItem("Pause");
		paused.setAccelerator(KeyStroke.getKeyStroke(KeyEvent.VK_P, 0));

		paused.getAccessibleContext().setAccessibleDescription(
				"Pause the game.");
		menu.add(paused);
		paused.addActionListener(this);

		// a group of radio button menu items
		menu.addSeparator();
		ButtonGroup group = new ButtonGroup();

		slow = makeRadioMenuItem("Slow", KeyEvent.VK_S, KeyStroke.getKeyStroke(
				KeyEvent.VK_0, ActionEvent.ALT_MASK), group);
		
		med = makeRadioMenuItem("Med", KeyEvent.VK_M, KeyStroke.getKeyStroke(
				KeyEvent.VK_1, ActionEvent.ALT_MASK), group);
		
		fast = makeRadioMenuItem("Fast", KeyEvent.VK_F, KeyStroke.getKeyStroke(
				KeyEvent.VK_2, ActionEvent.ALT_MASK), group);
		
		lightning = makeRadioMenuItem("Lightning", KeyEvent.VK_L, KeyStroke
				.getKeyStroke(KeyEvent.VK_3, ActionEvent.ALT_MASK), group);
		
		africanswallow = makeRadioMenuItem("African Swallow (Do Not Attempt!)",
				KeyEvent.VK_A, KeyStroke.getKeyStroke(KeyEvent.VK_4, ActionEvent.ALT_MASK), group);

		med.setSelected(true);

		menu.add(slow);
		menu.add(med);
		menu.add(fast);
		menu.add(lightning);
		menu.add(africanswallow);

		// A menu for ants.
		menu = new JMenu("Ant");
		menu.setMnemonic(KeyEvent.VK_A);
		menuBar.add(menu);
		
		callFive = makeMenuButton("Call Five", 0, null);
		menu.add(callFive);
		callTen = makeMenuButton("Call Ten", 0, null);
		menu.add(callTen);
		
		menu.addSeparator();
		
		releaseFive = makeMenuButton("Release Five", 0, null);
		menu.add(releaseFive);
		releaseTen = makeMenuButton("Release Ten", 0, null);
		menu.add(releaseTen);
		releaseAll = makeMenuButton("Release All", 0, null);
		menu.add(releaseAll);
		
		// The help menu.
		menu = new JMenu("Help");
		menu.setMnemonic(KeyEvent.VK_H);
		menuBar.add(menu);
		
		about = makeMenuButton("About CloneAnt", 0, null);
		menu.add(about);

		return menuBar;
	}

	/** The component inside the scroll pane. */
	@SuppressWarnings("serial")
	public class DrawingPane extends JPanel
	{
		protected void paintComponent(Graphics g)
		{
			super.paintComponent(g);

			myGame.draw(g);

			// Reset
			Dimension d = new Dimension(myGame.getWidth(), myGame.getHeight());
			drawingPane.setPreferredSize(d);
			drawingPane.revalidate();
		}
	}

	/**
	 * Handles mouse events.
	 */
	public void mouseReleased(MouseEvent e)
	{
		clickX = e.getX();
		clickY = e.getY();

		if (clickX < 0)
			clickX = 0;

		if (clickY < 0)
			clickY = 0;

		if (SwingUtilities.isRightMouseButton(e))
		{
			Tile t = myGame.tileAt(clickX, clickY);
			myGame.setPause(true);
			paused.setState(true);
			Dialogs.showInformationDialog("Info", myGame.getContext(t));
			
		} else
		{
			if(!SwingUtilities.isRightMouseButton(e))
			{
			// Because Java, in its infinite wisdom doesn't have a way to detect
			// double vs single
			// clicks, we'll just use this code:
			// http://stackoverflow.com/questions/548180/java-ignore-single-click-on-double-click
			// Essentially a callback that is run after a timer checks if the
			// double click has
			// been fired, if so, don't run the single click action :)
			if (e.getClickCount() == 2)
			{
				Tile t = myGame.tileAt(clickX, clickY);
				myGame.selectTile(t);
				wasDoubleClick = true;
				myGame.setPause(false);
				paused.setState(false);
			} else {
				int timerinterval = (Integer) Toolkit.getDefaultToolkit()
						.getDesktopProperty("awt.multiClickInterval");

				Timer timer = new Timer(timerinterval, new ActionListener()
				{
					public void actionPerformed(ActionEvent e)
					{
						if (wasDoubleClick)
							wasDoubleClick = false; // reset flag
						else
							scrollTo(clickX, clickY);
					}
				});
				timer.setRepeats(false);
				timer.start();
			}

		}
		drawingPane.repaint();
		}
	}

	/**
	 * Scrolls the viewpane to the given x and y.
	 * 
	 * @param x
	 * @param y
	 */
	private void scrollTo(int x, int y)
	{
		x = x - scroller.getWidth() / 2;
		y = y - scroller.getHeight() / 2;
		scroller.getHorizontalScrollBar().setValue(x);
		scroller.getVerticalScrollBar().setValue(y);
	}

	public void mouseClicked(MouseEvent e)
	{
	}

	public void mouseEntered(MouseEvent e)
	{
	}

	public void mouseExited(MouseEvent e)
	{
	}

	public void mousePressed(MouseEvent e)
	{
	}

	/**
	 * Handles all of the actions for the MainWindow.
	 */
	public void actionPerformed(ActionEvent e)
	{
		if (e.getSource() == blackHome)
			myGame.viewBlackNest();

		if (e.getSource() == redHome)
			myGame.viewRedNest();

		if (e.getSource() == surface)
			myGame.viewSurface();

		if (e.getSource() == slow)
			myGame.setUpdateDelay(1000); // 1 sec

		if (e.getSource() == med)
			myGame.setUpdateDelay(500); // .5 sec

		if (e.getSource() == fast)
			myGame.setUpdateDelay(250); // .25 sec

		if (e.getSource() == lightning)
			myGame.setUpdateDelay(100); // .1 sec

		if (e.getSource() == africanswallow)
			myGame.setUpdateDelay(0); // 0 sec

		if (e.getSource() == paused)
			myGame.setPause(paused.getState());
		
		if(e.getSource() == callFive)
			myGame.followPlayer(5);

		if(e.getSource() == callTen)
			myGame.followPlayer(10);
		
		if(e.getSource() == releaseFive)
			myGame.stopFollowingPlayer(5);

		if(e.getSource() == releaseTen)
			myGame.stopFollowingPlayer(10);
		
		if(e.getSource() == releaseAll)
			myGame.stopAllFollowingPlayer();
		
		if(e.getSource() == newGame)
			setUpGame();
		
		if(e.getSource() == about)
		{
			new AboutDialog();
			myGame.setPause(true);
			paused.setState(true);
		}
		if (e.getSource() == myAnt)
		{
			myGame.viewPlayer();
			scrollTo(myGame.getPlayerX(), myGame.getPlayerY());
		}
	}
}
