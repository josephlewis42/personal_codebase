package Game;

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
	public Image defaultImg;
	private Tile lastTile;
	
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
		lastTile = getTile();
	}
	
	/**
	 * Creates a new sprite on the same location and grid as the given sprite.
	 * 
	 * @param s
	 */
	public Sprite(Sprite s)
	{
		this(s.myX, s.myY, s.myMap);
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
		defaultImg = g;
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
		lastTile = getTile();
		Tile temp = t.getPortal();
		if(temp != null)
		{
			myX = temp.myX;
			myY = temp.myY;
			
			myMap = temp.myMap;
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
	
	/**
	 * Returns a direction which this sprite is facing, if
	 * the sprite hasn't ever moved, direction is NORTH.
	 */
	public Direction getDirectionFacing()
	{
		if(lastTile != getTile())
			return getTile().getRelation(lastTile);
		return Direction.NORTH;
	}
}