import java.awt.Graphics;
import java.util.ArrayList;
import javax.swing.JPanel;

/**
 * Represents a game; including the world and main loop.
 * @author Joseph Lewis <joehms22@gmail.com>
 * @license GNU GPL v2 or higher.
 */
public class Game extends Thread
{	
	// Maps
	private Grid redNest, blackNest, surface, current;
	private JPanel myDrawingPanel;
	
	private int updatedelay = 250; //Number of ms to wait between updates.
	
	private Colony redColony, blackColony;
	private ArrayList<Sprite> myActors = new ArrayList<Sprite>();
	private Ant player; //This sprite is special!
	
	private boolean paused = false; //True if the game is paused.
	
	private static final int FOOD_UNTIL_ADD = 30;
	private static final int FOOD_AFTER_ADD = 750;

	private static final int FOOD_CHECK_INTERVAL = 10;
	private int food_check_time = 0;
	
	private Tile foodLocation;
	
	private int roundsSoFar = 0;
	
	/**
	 * Init a game.
	 */
	public Game()
	{
		surface = Factory.createGrid(GridType.SURFACE);
		blackNest = Factory.createGrid(GridType.BLACKNEST, surface);
		redNest = Factory.createGrid(GridType.REDNEST, surface);
		
		redColony = new Colony(redNest, "red", this);
		blackColony = new Colony(blackNest, "black", this);
		
		current = surface; //Set the current surface to the actual surface.
		
		resetPlayer();
	}
	
	public Tile getFoodLocation()
	{
		return foodLocation;
	}
	
	private void resetPlayer()
	{
		player = Factory.createAnt(AntType.SOLDIER, blackColony, blackColony.startTile.myX, blackColony.startTile.myY);
		player.hatch();
		player.myImg = ImageLoader.getImage(ImageType.YELLOWSOLDIER);
		
		// Let all ants know that the player is reborn!
		Ant.thePlayer = player;
		
		// Reset view to where the player is.
		current = player.getGrid();
	}
	
	/**
	 * Adds a sprite to the list of sprites to move.
	 * @param s
	 */
	public void addSprite(Sprite s)
	{
		synchronized(myActors)
		{
			myActors.add(s);
		}
	}
	
	/**
	 * Removes a sprite from the list of actors.
	 * 
	 * @param s
	 */
	public void removeSprite(Sprite s)
	{
		synchronized(myActors)
		{
			myActors.remove(s);
			
		}
	}	
	
	/**
	 * Returns all of the actors in the game, minus the player.
	 * @return
	 */
	public Sprite[] getActors()
	{
		synchronized(myActors)
		{
			return myActors.toArray(new Sprite[0]);
		}
	}
	
	/**
	 * The main loop of the game.
	 */
	public void run()
	{
		while(1 > 0)
		{
			//Wait some time.
			try 
			{
				Thread.sleep(updatedelay);

				while(paused)
					Thread.sleep(250);
			} catch (InterruptedException e)
			{
				System.err.println("Main Loop interrupted from slumber!");
			}
			
			roundsSoFar++;
			
			// Trigger catastrophies!
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
				Dialogs.showInformationDialog("Score", "Score: "+roundsSoFar);
				return;
			}
			if(blackColony.checkEndgame())
			{
				Dialogs.showInformationDialog("Game Over", "You Lost! The Black queen has died!");
				Dialogs.showInformationDialog("Score", "Score: "+roundsSoFar);
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
	
	public void viewPlayer()
	{
		current = player.getGrid();
	}
	
	public int getPlayerX()
	{
		return player.myX * Tile.WIDTH;
	}
	
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
	
	public void stopAllFollowingPlayer()
	{
		stopFollowingPlayer(Integer.MAX_VALUE);
	}
	
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
	
	public String getContext(Tile t)
	{
		if(t.getAnt() != null)
			return t.getAnt().toString();
		return t.toString();
	}
}
