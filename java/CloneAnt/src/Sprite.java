import java.awt.Graphics;
import java.awt.Image;

/**
 * A class representing an object on a Grid. All sprites 
 * can move, belong to a grid, have a location on that 
 * grid, 
 * 
 * @author Joseph Lewis <joehms22@gmail.com>
 *
 */
public abstract class Sprite
{
	public Grid myMap = null;
	public int myX = 0;
	public int myY = 0;
	public Image myImg = null;
	
	/**
	 * Creates a sprite on the given grid at the given location.
	 * @param x
	 * @param y
	 * @param map
	 */
	public Sprite(int x, int y, Grid map)
	{
		myX = x;
		myY = y;
		myMap = map;
	}
	
	/**
	 * Creates a sprite on the given grid at the given
	 * x and y, with the given image.
	 * 
	 * @param x
	 * @param y
	 * @param map
	 * @param g
	 */
	public Sprite(int x, int y, Grid map, Image g)
	{
		this(x, y, map);
		myImg = g;
	}
	
	/**
	 * Creates a sprite on the given grid with the given
	 * coordinates and the image at the given location.
	 * 
	 * @param x
	 * @param y
	 * @param map
	 * @param imgLoc
	 */
	public Sprite(int x, int y, Grid map, String imgLoc)
	{
		this(x, y, map, ImageLoader.getImage(imgLoc));
	}
	
	/**
	 * Moves this sprite.
	 */
	public abstract void move();
	
	/**
	 * Returns the image of the sprite.
	 */
	public void draw(Graphics g)
	{
		g.drawImage(myImg, myX*Tile.WIDTH, myY*Tile.HEIGHT, null);
	}
	
	/**
	 * Moves to the given tile, if the tile is a link, 
	 * moves to the linked location.
	 * @param t
	 */
	protected void moveTo(Tile t)
	{
		if(t.portalTo != null)
		{
			myX = t.portalTo.myX;
			myY = t.portalTo.myY;
			myMap = t.portalTo.myMap;
		}
		else
		{
			myX = t.myX;
			myY = t.myY;
		}
	}
	
	/**
	 * Returns the tile associated with this sprite, if the sprite is a tile, returns this.
	 * 
	 * @return
	 */
	public Tile getTile()
	{
		return myMap.myTerrain[myX][myY];
	}
	
	/**
	 * Returns the grid associated with this sprite.
	 * 
	 * @return
	 */
	public Grid getGrid()
	{
		return myMap;
	}
	
	/**
	 * Provides a pretty represenation of this sprite.
	 */
	public String toString()
	{
		return "X: " + myX + "Y: " + myY;
	}
	
	/**
	 * Returns a list of the possible moves for this sprite.
	 */
	public Tile[] getPossibleMoves()
	{
		return myMap.getPossibleMoves(this);
	}
	
	/**
	 * Returns a list of dug moves around this sprite.
	 */
	public Tile[] getDugMoves()
	{
		return myMap.getDugMoves(this);
	}
}