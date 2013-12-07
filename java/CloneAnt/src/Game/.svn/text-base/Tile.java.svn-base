package Game;

import java.awt.Graphics;
import java.awt.Image;

/**
 * A representation of a tile in the map.
 * 
 * @author Joseph Lewis <joehms22@gmail.com>
 *
 */
public class Tile extends Sprite
{	
	public static final int WIDTH 		= 24;  // The width of every tile in pixels
	public static final int HEIGHT 		= 24;  // The height of every tile in pixels
	public static final int SCENT_MAX 	= 100; // The number of times for a scent to stick on a tile.
	
	private int food = 0; // Amount of food on this tile.
	private Ant myAnt; // A sprite that inhabits this tile.
	public int scent = 0; // Food scent that is on this tile.
	private Tile portalTo; // The tile this is a portal to, if it is one.
	
	public boolean traversable = true;
	public boolean isUnderground = false;
	public boolean isDug = false;
	
	
	/**
	 * Creates a new tile.
	 * 
	 * @param j - The image for this tile.
	 * @param underground - Is this tile underground?
	 * @param x - The x location of the tile.
	 * @param y - The y location of the tile.
	 * @param parent - The Grid parent of this tile.
	 */
	public Tile(Image j, boolean underground, int x, int y, Grid parent)
	{
		super(x,y, parent, j);
		isUnderground = underground;
		updateImage();
	}
	
	/**
	 * Moves this tile (tiles are sprites). Decreases scent and 
	 * removes the ants from the tile.
	 */
	public void move()
	{ 
		if(scent > 0)
			scent--;
		if(myAnt != null && myAnt.getTile()!= this)
			 myAnt = null;
	}
	
	/**
	 * Sets the amount of food on this tile between 1 and 5;
	 * if this isn't a portal.
	 * 
	 * @param newFood - Amount of food to set tile to have.
	 */
	public void setFood(int newFood)
	{
		if(newFood >= 0 && newFood <= 5 && !hasPortal())
			food = newFood;
		
		updateImage();
	}
	
	/**
	 * Gets this tile's portal.
	 * 
	 * @return The portal for this tile.
	 */
	public Tile getPortal()
	{
		return portalTo;
	}
	
	/**
	 * Updates the image based upon how much food there is on the tile.
	 */
	private void updateImage()
	{
		if(isDug || !isUnderground)
			switch(food)
			{
			case(0): myImg = ImageLoader.getImage(ImageType.SURFACE_TILE); break;
			case(1): myImg = ImageLoader.getImage(ImageType.SURFACE_ONE_FOOD); break;
			case(2): myImg = ImageLoader.getImage(ImageType.SURFACE_TWO_FOOD); break;
			case(3): myImg = ImageLoader.getImage(ImageType.SURFACE_THREE_FOOD); break;
			case(4): myImg = ImageLoader.getImage(ImageType.SURFACE_FOUR_FOOD); break;
			case(5): myImg = ImageLoader.getImage(ImageType.SURFACE_FIVE_FOOD); break;
			}
	}
	
	/**
	 * Excavates this tile.
	 */
	public void dig()
	{
		digAndLink(false);
	}

	/**
	 * Digs out this tile and adds a portal if it is in a location that 
	 * creates portals and link is true, also changes the image of this sprite.
	 */
	public void digAndLink(boolean link)
	{
		if(isUnderground && !isDug)
		{
			myImg = ImageLoader.getImage("/images/tiles/dirt.jpg");
			isDug = true;
			
			myMap.notifyTileDug(); //Notifies the grid that the tile has been dug.
						
			//If this is in row 0, connect to parent map.
			if(myY == 0 && portalTo == null && link)
				portalTo = myMap.parent.addPortal(this);
		}
	}
	
	/**
	 * Sets the portal for this sprite, and changes the image.
	 * @param t - The tile to link to.
	 */
	public void setPortal(Tile t)
	{
		myImg = ImageLoader.getImage(ImageType.HOLE);
		portalTo = t;
	}
	
	/**
	 * Get the closest tile to this one given a list of tiles.
	 * 
	 * @param tiles
	 * @return
	 */
	public Tile getClosest(Tile[] tiles)
	{
		int dist = Integer.MAX_VALUE;
		Tile closest = null;
		
		for(Tile t: tiles)
			if(getDistance(t) < dist)
			{
				closest = t;
				dist = getDistance(t);
			}
		return closest;
	}
	
	/**
	 * Gets the farthest tile from this one in the given list.
	 * 
	 * @param tiles
	 * @return
	 */
	public Tile getFarthest(Tile[] tiles)
	{
		int dist = Integer.MIN_VALUE;
		Tile furthest = null;
		
		for(Tile t: tiles)
			if(getDistance(t) > dist)
			{
				furthest = t;
				dist = getDistance(t);
			}
		return furthest;
	}
	
	/**
	 * Gets a rough estimate of the distance between this tile and another.
	 * @param t
	 * @return
	 */
	public int getDistance(Tile t)
	{
		int distY = Math.abs(t.myY - myY);
		int distX = Math.abs(t.myX - myX);
		
		return distY + distX;
	}
	
	/**
	 * Call the move then draw on this tile (as move isn't called for tiles).
	 */
	public void draw(Graphics g)
	{
		move();
		super.draw(g);
	}
	
	/**
	 * Returns the direction this tile is compared to other.
	 * i.e. this tile is at 1 1 and other is at 0 0, SOUTHEAST
	 * would be returned.
	 */
	public Direction getRelation(Tile other)
	{
		if(myX == other.myX) //N or S
			if(myY < other.myY)
				return Direction.NORTH;
			else
				return Direction.SOUTH;
		
		if(myY == other.myY)
			if(myX < other.myX)
				return Direction.WEST;
			else
				return Direction.EAST;
		
		
		if(myX > other.myX)
			if(myY > other.myY)
				return Direction.SOUTHEAST;
			else
				return Direction.NORTHEAST;
		
		//myX < other.myX
		if(myY > other.myY)
			return Direction.SOUTHWEST;
		
		return Direction.NORTHWEST;
	}

	/**
	 * 
	 * @return The amount of food on this tile.
	 */
	public int getFood()
	{
		return food;
	}
	
	/**
	 * Removes a piece of food from this square.
	 * @return True if there was food, false if there was not.
	 */
	public boolean pickFood()
	{
		food--;
		updateImage();
		return food >= 0;
	}
	
	/**
	 * Adds some food if possible, you can't add food on a
	 * portal.
	 * 
	 * @return True if the food was added, false otherwise.
	 */
	public boolean placeFood()
	{
		if(food < 5 && portalTo == null)
		{
			food++;
			updateImage();
			return true;
		}
		return false;
	}
	
	public boolean hasFood(){ return food > 0; }
	
	/**
	 * Updates the food scent on this tile.
	 */
	public void updateScent()
	{
		scent = SCENT_MAX;
	}

	/**
	 * Notifies this tile that a sprite is on it, if there is already
	 * a sprite here, return that sprite.
	 * @param mySprite
	 * @return
	 */
	public Ant setSprite(Ant mySprite)
	{
		if(myAnt == null)
		{
			myAnt = mySprite;
			return null;
		}
		
		Ant temp = myAnt;
		myAnt = mySprite;
		return temp;
	}
	
	/**
	 * Removes the given sprite from the tile if it is the currently
	 * registered one.
	 * @param mySprite
	 */
	public void removeSprite(Ant mySprite)
	{
		if(mySprite == myAnt)
			mySprite = null;
	}

	/**
	 * Updates the scent on this tile, adding amount to the already
	 * updates amount.
	 * @param amount
	 */
	public void updateScent(int amount)
	{
		updateScent();
		scent += amount;
	}

	/**
	 * Returns the ant on this tile.
	 */
	public Ant getAnt()
	{
		return myAnt;
	}	
	
	/**
	 * A pretty represenation of this tile:
	 * <pre>
	 * Surface Tile (15, 47)
	 * Food: 67
	 * Scent: 89
	 * Portal To: UNDERGROUND
	 */
	public String toString()
	{
		String build = "";
		//ex: Surface Tile (14, 55)
		build += (isUnderground)?"Underground":"Surface";		
		build += " Tile (" + myX + ", " + myY + ")";
		
		build += "\nFood: "+ food;
		build += "\nScent: "+ scent;
		build += "\nTraversable: "+ ((traversable)?"Yes":"No");
		
		if(isUnderground)  
			build += "\nExcavated: "+((isDug)?"Yes":"No");
		
		if(portalTo != null)
			build += "\nPortal to: "+portalTo.myMap.gridType;
		
		return build;
	}

	/**
	 * Does this tile have a portal to another?
	 */
	public boolean hasPortal() { return portalTo != null; }

}