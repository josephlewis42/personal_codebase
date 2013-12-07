package Game;
import java.awt.Graphics;
import java.util.ArrayList;

/**
 * A 2d Map for the game, holds a bunch of tiles.
 * 
 * @author Joseph Lewis <joehms22@gmail.com>
 *
 */
public class Grid
{
	public final Tile[][] myTerrain; // Can't change the tile array.	
	public final int width, height;  // The width and height of this grid.
	public final int pxWidth, pxHeight; // The pixel width and height of this grid.
	public final GridType gridType;	// The type of this grid.
	public final Grid parent; // The parent grid for this tile.

	public static Grid surfaceGrid;
	
	private int numDug = 0;
	private final ArrayList<Grid> myChildren = new ArrayList<Grid>();


	/**
	 * Creates a new Grid.
	 * 
	 * @param width - The width of the grid in tiles.
	 * @param height - The height in tiles of the grid.
	 * @param mytt - The TileType of the tiles here (all new tiles will be of this type).
	 * @param p 
	 */
	public Grid(int width, int height, GridType p, Grid parentGrid)
	{
		gridType = p;
		parent = parentGrid;
		
		if(parentGrid != null)
			parentGrid.registerChild(this);
		
		myTerrain = new Tile[width][height];
		
		this.width = width;
		this.height = height;
		
		pxWidth = width * Tile.WIDTH;
		pxHeight = height * Tile.HEIGHT;
		
		if(p == GridType.SURFACE)
			surfaceGrid = this;
	}
	
	
	/**
	 * Adds the current grid to the children of this grid.
	 */
	public void registerChild(Grid g)
	{
		if(g != null)
			myChildren.add(g);
	}
	
	
	/**
	 * Draws the terrain to the given graphics component.
	 * 
	 * @param g
	 */
	public void draw(Graphics g)
	{	
		for(int x = 0; x < myTerrain.length; x++)
			for(int y = 0; y < myTerrain[0].length; y++)
				myTerrain[x][y].draw(g);
	}
	
	
	/**
	 * Gets all of the moves around here that have been dug 
	 * (if the grid is underground).
	 * 
	 * @param s - The sprite to check for moves around.
	 * @return - A list of tiles that are dug around the sprite.
	 */
	public Tile[] getDugMoves(Sprite s)
	{
		ArrayList<Tile> tileList = new ArrayList<Tile>();
		
		for(Tile t : getPossibleMoves(s))
			if(t.isUnderground)
			{
				if(t.isDug)
					tileList.add(t);
			}
			else
			{
				tileList.add(t);
			}
		
		return tileList.toArray(new Tile[1]);
	}
	
	/**
	 * Gets all of the tiles around the given sprite.
	 * 
	 * @param s - The sprite to check for tiles around.
	 * @return A list of tiles around the sprite.
	 */
	public Tile[] getPossibleMoves(Sprite s)
	{
		return getPossibleMoves(s.myX, s.myY);
	}
	
	/**
	 * Gets all of the possible moves around a coordinate.
	 * 
	 * @param x - The x location on the grid to get tiles around.
	 * @param y - The y location on the grid to get tiles around.
	 * @return A list of tiles that can be traversed (traversable = true).
	 */
	public Tile[] getPossibleMoves(int x, int y)
	{
		ArrayList<Tile> tileList = new ArrayList<Tile>();
		
		for(Tile t : getSurrounding(x,y))
			if(t.traversable)
				tileList.add(t);
		
		return tileList.toArray(new Tile[1]);
	}
	
	/**
	 * Returns the surrounding tiles for the coordinates.
	 * @param x - The x location to check for tiles around.
	 * @param y - The y location to check for tiles around.
	 * @return A list of all tiles around the given coordinates.
	 */
	public Tile[] getSurrounding(int x, int y)
	{
		ArrayList<Tile> tileList = new ArrayList<Tile>();
		
		tileList.add(safeGetTile(x-1, y-1));
		tileList.add(safeGetTile(x, y-1));
		tileList.add(safeGetTile(x+1, y-1));
		tileList.add(safeGetTile(x-1, y));
		tileList.add(safeGetTile(x+1, y));
		tileList.add(safeGetTile(x-1, y+1));
		tileList.add(safeGetTile(x, y+1));
		tileList.add(safeGetTile(x+1, y+1));

		//Remove all nulls
		while(tileList.remove(null));
		
		return tileList.toArray(new Tile[0]);
	}
	
	/**
	 * Returns a list of tiles with links out of this location.
	 */
	public Tile[] getLinks()
	{
		ArrayList<Tile> links = new ArrayList<Tile>();
		
		for(Tile[] row : myTerrain)
			for(Tile cell : row)
				if(cell.hasPortal())
					links.add(cell);
		
		return links.toArray(new Tile[0]);
	}
	
	/**
	 * Get links which point to the given GridType
	 * @param g
	 * @return
	 */
	public Tile[] getLinksTo(GridType g)
	{
		ArrayList<Tile> links = new ArrayList<Tile>();
		
		for(Tile cell : getLinks())
			if(cell.hasPortal() && cell.getPortal().myMap.gridType == g)
				links.add(cell);
		
		return links.toArray(new Tile[0]);
	}
	
	/**
	 * Safely gets the tile at the given location (no out of bounds exceptions)
	 * @param x
	 * @param y
	 * @return
	 */
	private Tile safeGetTile(int x, int y)
	{
		try {
			return myTerrain[x][y];
		} catch(ArrayIndexOutOfBoundsException ex) {
			return null;
		}
	}
	
	/**
	 * Adds a portal in a random location to the given location.
	 * 
	 * Some additional constraints are here, suppose this is the 
	 * main grid (surface) and two nests exist, red and black.
	 * Each of those nest's grids are added to this grid, each
	 * grid will be given half of the surface which is "theirs"
	 * mounds created from either of those grids will always pop
	 * up on their half.
	 * 
	 * If there are n child grids, then there are n divisions of 
	 * this grid.
	 * 
	 * @param to
	 * @return
	 */
	public Tile addPortal(Tile to)
	{	
		//Get the part of the grid to add tiles to.
		int index = myChildren.indexOf(to.myMap);
		int w = this.width/(myChildren.size());
		
		int randomx = (index * w) + (int)(Math.random()*w);
		int randomy = (int)(Math.random()*height);
		
		//Randomly choose a place.
		Tile t = myTerrain[randomx][randomy];
		
		//Set a link.
		t.setPortal(to);

		return t;
	}
	
	/**
	 * Pretty prints information about this grid.
	 */
	public String toString()
	{
		return "Grid: "+gridType+" X-Width: "+width+" Y-Height: "+height;
	}
	
	/**
	 * Returns the amount of food on this map
	 */
	public int getFood()
	{
		int amt = 0;
		for(Tile[] t : myTerrain)
			for(Tile ti : t)
				amt += ti.getFood();
		return amt;
	}
	
	/**
	 * Returns a random tile in the grid that isn't linked.
	 * 
	 * @return
	 */
	public Tile randomTile()
	{		
		int randomx = (int)(Math.random()*width);
		int randomy = (int)(Math.random()*height);
		
		//Randomly choose a place.
		Tile t = myTerrain[randomx][randomy];
		
		if(!t.hasPortal())
			return t;
		return randomTile();
	}
	
	/**
	 * Resets the terrain.
	 */
	public void update()
	{
		for(Tile[] row : myTerrain)
			for(Tile cell : row)
				cell.move();
	}
		
	/**
	 * Tiles call this method to alert the grid that a tile has been dug.
	 * One call here keeps from using copious amounts of for loops later.
	 */
	public void notifyTileDug() { numDug++; }
	
	/**
	 * Get the number of tiles dug on this map.
	 * @return
	 */
	public int getNumDug() { return numDug; }
}
