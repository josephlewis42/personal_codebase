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
	public static int WIDTH = 24; //The width of every tile in pixels
	public static int HEIGHT = 24; //The height of every tile in pixels
	
	public static int SCENT_MAX = 100; //The number of times for a scent to stick on a tile.
	
	//int type; //Type of this tile.
	public int food; //Amount of food on this tile.
	
	private Ant myAnt;//A sprite that inhabits this tile.
	
	int scent = 0; //Food scent that is on this tile.
	
	Tile portalTo; //If this is a portal to another tile...
	
	boolean traversable = true;
	boolean isUnderground = false;
	boolean isDug = false;
	
	//private static final int scentDecrease = 1;
	
	public Tile(Image j, boolean underground, int x, int y, Grid parent)
	{
		super(x,y, parent, j);
		isUnderground = underground;
		updateImage();
	}
	
	public void move()
	{ 
		if(scent > 0)
			scent--;
		if(myAnt != null && myAnt.getTile()!= this)
			 myAnt = null;
	}
	
	public void setFood(int newFood)
	{
		if(newFood >= 0 && newFood <= 5)
			food = newFood;
		
		updateImage();
	}
	
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
				portalTo = myMap.getParent().addPortal(this);
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
	
	public Tile getFurthest(Tile[] tiles)
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
	
	public void removeSprite(Ant mySprite)
	{
		if(mySprite == myAnt)
			mySprite = null;
	}

	public Sprite getSprite()
	{
		return myAnt;
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

	public Ant getAnt()
	{
		return myAnt;
	}	
	
	public String toString()
	{
		String build = "";
		build += "Tile At (" + myX + ", " + myY + ")";
		
		build += "\nFood: "+ food;
		build += "\nScent: "+ scent;
		build += "\nTraversable: "+traversable;
		build += "\nUnderground? "+isUnderground;
		build += "\nDug? "+isDug;
		
		if(portalTo != null)
			build += "\nPortal to: "+portalTo.myMap.getType();
		
		return build;
	}
}