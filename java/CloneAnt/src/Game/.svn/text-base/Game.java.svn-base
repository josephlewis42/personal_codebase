package Game;

import java.awt.Graphics;
import java.util.ArrayList;

import javax.swing.JLabel;
import javax.swing.JPanel;

import Game.Directive.Follow;

/**
 * Represents a game; including the world and main loop.
 * @author Joseph Lewis <joehms22@gmail.com>
 * @license GNU GPL v2 or higher.
 */
public class Game extends Thread
{	
	private JPanel myDrawingPanel; // The place to draw the map.
	
	// Variables for controlling food placement.
	private static final int FOOD_UNTIL_ADD = 30; // Amount of food until more is dumped.
	private static final int FOOD_AFTER_ADD = 750; // Amount of food to dump.
	private static final int FOOD_CHECK_INTERVAL = 10; // Check for food amounts this number of turns.
	private int food_check_time = 0; // Turns since last food check.
	
	// Game variables.
	private int updatedelay = 250; //Number of ms to wait between movements.
	private boolean paused = false; //True if the game is paused.
	private int roundsSoFar = 0; // Counts the number of rounds the game has played so far.
	
	// Concerning this game.
	private Grid redNest, blackNest, surface, current;
	private Colony redColony, blackColony;
	private ArrayList<Sprite> myActors = new ArrayList<Sprite>();
	private Ant player; //This sprite is special!
	
	// The last tile food was placed at.
	private Tile foodLocation;
	
	
	/**
	 * Init a game.
	 */
	public Game()
	{
		// Create the surface grid first, so the Game knows what the surface is.
		surface = Factory.createGrid(GridType.SURFACE);
		blackNest = Factory.createGrid(GridType.BLACKNEST);
		redNest = Factory.createGrid(GridType.REDNEST);
		
		redColony = new Colony(redNest, "red", this);
		blackColony = new Colony(blackNest, "black", this);
		
		resetPlayer(); // Set up the player for the first time.
	}
	
	/**
	 * @return The last tile the food was placed at. 
	 */
	public Tile getFoodLocation() { return foodLocation; }
	
	
	/**
	 * Regenerates the player.
	 */
	private void resetPlayer()
	{
		player = Factory.createAnt(AntType.SOLDIER, blackColony);
		player.hatch();
		player.myImg = ImageLoader.getImage(ImageType.YELLOWSOLDIER);
		player.defaultImg = player.myImg;
		
		// Let all ants know that the player is reborn!
		Ant.thePlayer = player;
		
		// Reset view to where the player is.
		current = player.getGrid();
	}
	
	/**
	 * Adds a sprite to the list of sprites to move.
	 * @param s
	 */
	public synchronized void addSprite(Sprite s) { myActors.add(s); }
	
	/**
	 * Removes a sprite from the list of actors.
	 * 
	 * @param s
	 */
	public synchronized void removeSprite(Sprite s) { myActors.remove(s); }	
	
	/**
	 * Returns all of the actors in the game, minus the player.
	 * @return
	 */
	public synchronized Sprite[] getActors() { return myActors.toArray(new Sprite[0]); }
	
	
	/**
	 * Takes care of pausing the game, and sleeping between
	 * frame draws.
	 */
	protected void sleepSome()
	{
		sleepSome(updatedelay);
		
		while(paused) //If we are paused, wait until we aren't.
			sleepSome(250);
	}
	
	/**
	 * Actually sets the sleep.
	 * @param amt
	 */
	protected void sleepSome(int amt)
	{
		try 
		{
			Thread.sleep(amt);
		} 
		catch (InterruptedException e)
		{
			System.err.println("Main Loop interrupted from slumber!");
		}
	}
	
	/**
	 * Checks if there is enough food on the surface, if not 
	 * puts some more there.
	 */
	protected void checkFood()
	{
		food_check_time--;
		if(food_check_time <= 0)
		{
			food_check_time = FOOD_CHECK_INTERVAL;
			
			if(FOOD_UNTIL_ADD > surface.getFood())
			{
				foodLocation = surface.randomTile();
				Tile newFood = foodLocation;
				ArrayList<Tile> t = new ArrayList<Tile>();
				t.add(foodLocation);
				
				for(int i = 0; i < FOOD_AFTER_ADD/4; i++)
				{
					newFood.setFood(4);
					
					for(Tile ti: newFood.getPossibleMoves())
						t.add(ti);
					newFood = t.get(i);
				}
				System.out.println("Adding food");
			}
		}
	}
	
	/**
	 * Checks the number of black and red ants, then sets the jLabel saying
	 * how many.
	 */
	protected void checkAnts()
	{
		// Check for black and
		int numRed = redColony.getMembers().length;
		int numBlack = blackColony.getMembers().length;
		
		
		antCounter.setText("<html><b>"+numRed+"</b><br /><b><font color=#ff0000>"+numBlack+"</font></b></html>");
	}
	
	
	/**
	 * The main loop of the game.
	 */
	public void run()
	{
		// Wait for a drawing panel before starting the game.
		while(myDrawingPanel == null)
		{
			sleepSome(250);
		}
		
		while(1 > 0) // Do this forever!
		{
			roundsSoFar++;

			sleepSome(); // Sleep for a bit so we don't explode the brains of the puny humans!
			
			
			// Trigger catastrophes! TODO add some catastrophes...
			checkFood();
			checkAnts();
			
			
			// Move everyone.
			synchronized(myActors)
			{
				for(Sprite s : myActors.toArray(new Sprite[0]))
					s.move();
				player.move();
			}
			
			// Update screen.
			update();
			
			if(redColony.checkEndgame())
			{
				Dialogs.showInformationDialog("Game Over", "You won! The Red queen has died!");
				notifyScore();
				return;
			}
			if(blackColony.checkEndgame())
			{
				Dialogs.showInformationDialog("Game Over", "You Lost! The Black queen has died!");
				notifyScore();
				return;
			}
			if(!player.isAlive() || player == null)
			{
				Dialogs.showInformationDialog("Alert", "You died!");
				resetPlayer();
			}
		}
	}
	
	/**
	 * Notifies the player of the score.
	 */
	public void notifyScore()
	{
		Dialogs.showInformationDialog("Score", "Score: "+roundsSoFar);
	}
	
	/**
	 * Changes the update delay to the given value if that value is greater than or equal to 0.
	 * 
	 * @param us
	 */
	public void setUpdateDelay(int us)
	{
		if(us >= 0)
			updatedelay = us;
	}
	

	/**
	 * Set the game to paused or not.
	 */
	public void setPause(boolean paused)
	{
		this.paused = paused;
	}
	
	public void setDrawingPane(JPanel j)
	{
		myDrawingPanel = j;
	}
	
	JLabel antCounter;
	public void setAntCount(JLabel output)
	{
		antCounter = output;
	}
	
	/**
	 * Called by the DrawingPanel to repaint the grid..
	 */
	public void draw(Graphics g)
	{
		// Draw Surface
		current.draw(g);
		
		// Draw actors
		synchronized(myActors)
		{
			for(Sprite s: myActors)
				if(s.myMap == current)
					s.draw(g);
		}
		if(player.myMap == current)
			player.draw(g);
	}
	
	/**
	 * Forces the DrawingPanel that originally called draw to 
	 * repaint itself with the current surfaces.
	 */
	private void update()
	{
		if(myDrawingPanel != null)
			myDrawingPanel.repaint();
		else
			System.err.println("Game.java, Drawing panel not set!");
	}
	
	/**
	 * @return Returns the width of the current map in pixels.
	 */
	public int getWidth()
	{
		return current.pxWidth;
	}
	
	/**
	 * @return The height of the current map in pixels.
	 */
	public int getHeight()
	{
		return current.pxHeight;
	}
	
	/**
	 * Sets the current view to the red nest.
	 */
	public void viewRedNest()
	{
		current = redNest;
		update();
	}
	
	/**
	 * Sets the current view to the black nest.
	 */
	public void viewBlackNest()
	{
		current = blackNest;
		update();
	}
	
	/**
	 * Sets the current view to the surface.
	 */
	public void viewSurface()
	{
		current = surface;
		update();
	}
	
	/**
	 * Sets the current view to wherever the player is.
	 */
	public void viewPlayer()
	{
		current = player.getGrid();
	}
	
	/**
	 * Gets the location of the player in pixels.
	 */
	public int getPlayerX()
	{
		return player.myX * Tile.WIDTH;
	}
	
	/**
	 * Returns the Y location of the player in pixels.
	 */
	public int getPlayerY()
	{
		return player.myY * Tile.HEIGHT;
	}
	
	/**
	 * Returns the tile at the given location in pixels from the upper left.
	 * 
	 * If x or y is greater than the actual width (large screens) then switch to
	 * the closest tile.
	 * 
	 * @param x
	 * @param y
	 * @return The selected tile.
	 */
	public Tile tileAt(int x, int y)
	{		
		if( y > current.pxHeight )
			y = current.pxHeight - 1;
		if( x > current.pxWidth )
			x = current.pxWidth - 1;
		
		return current.myTerrain[x/Tile.WIDTH][y/Tile.HEIGHT];
	}
	
	/**
	 * Selects the given tile and sets it as the directive for the character's ant.
	 * @return 
	 */
	public void selectTile(Tile t)
	{
		player.myDirective = DirectiveFactory.goTo(player,t);
	}
	
	
	/**
	 * Tells this number of ants to follow the player.
	 * 
	 * @param number
	 */
	public void followPlayer(int number)
	{
		Ant[] myAmigos = blackColony.getMembers();
		
		for(Ant a: myAmigos)
		{
			if(a.myType != AntType.QUEEN)
				if(!(a.myDirective instanceof Follow) && a.getHatched())
				{
					a.myDirective = DirectiveFactory.follow(a, player);
					number--;
				}
			if(number == 0)
				return;
		}	
	}
	
	/**
	 * Stop all black ants from following the player.
	 */
	public void stopAllFollowingPlayer()
	{
		stopFollowingPlayer(Integer.MAX_VALUE);
	}
	
	/**
	 * Stop the given number of ants from following the player.
	 * 
	 * @param number
	 */
	public void stopFollowingPlayer(int number)
	{
		Ant[] myAmigos = blackColony.getMembers();
		
		for(Ant a: myAmigos)
		{
			if(a.myDirective instanceof Follow)
				if(((Follow)a.myDirective).toFollow == player)
				{
					DirectiveFactory.direct(a); // Find new directive.
					number--;
				}
			if(number == 0)
				return;
		}	
	}
	
	/**
	 * Gets the context information on a specific tile.
	 * 
	 * @param t
	 * @return
	 */
	public String getContext(Tile t)
	{
		if(t.getAnt() != null)
			return t.getAnt().toString() + "\n\n" + t.toString();
		return t.toString();
	}
}
