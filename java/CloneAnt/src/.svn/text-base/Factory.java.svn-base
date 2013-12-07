
/**
 * A multi-purpose factory for creating all sorts of things.
 * 
 * @author Joseph Lewis <Joehms22@gmail.com>
 *
 */
public class Factory
{
	// Sizes of Grids.
	public static final int SURFACE_HEIGHT = 30;
	public static final int SURFACE_WIDTH = 75;
	public static final int NEST_HEIGHT = 50;
	public static final int NEST_WIDTH = 30;
	
	
	// Strengths (Used in determining the outcomes of battles).
	public static final int NEWQUEEN_STRENGTH = 3;
	public static final int QUEEN_STRENGTH = 8;
	public static final int SOLDIER_STRENGTH = 2;
	public static final int WORKER_STRENGTH = 1;
		
	/**
	 * Creates a new grid with no parent.
	 * 
	 * @param p
	 * @return
	 */
	public static Grid createGrid(GridType p)
	{
		return createGrid(p, null);
	}
	
	public static Grid createGrid(GridType p, Grid parent)
	{
		if(p == GridType.BLACKNEST || p == GridType.REDNEST)
		{
			Grid g = new Grid(NEST_WIDTH, NEST_HEIGHT, p, parent);
			//Load up with tiles.
			for(int x = 0; x < g.myTerrain.length; x++)
				for(int y = 0; y < g.myTerrain[0].length; y++)
					g.myTerrain[x][y] = Factory.createTile(TileType.DIRT, g, x, y);
				
			//Set top grass.
			for(Tile[] t: g.myTerrain)
				t[0].myImg = ImageLoader.getImage("/images/tiles/grass.jpg");
			
			return g;
		}
		
		if(p == GridType.SURFACE)
		{
			Grid g = new Grid(SURFACE_WIDTH, SURFACE_HEIGHT, p, parent);
		
			for(int x = 0; x < g.myTerrain.length; x++)
				for(int y = 0; y < g.myTerrain[0].length; y++)
					g.myTerrain[x][y] = Factory.createTile(TileType.GROUND, g, x, y);
			return g;
		}

		return null;
	}
	
	
	/**
	 * Creates a new tile.
	 * 
	 * @param tilename - The type of tile.
	 * @param tileGrid - The grid this tile belongs to.
	 * @param x - The x loc of the tile.
	 * @param y - The y loc of the tile.
	 * @return The newly created tile.
	 */
	public static Tile createTile(TileType tilename, Grid tileGrid, int x, int y)
	{
		if(tilename == TileType.GROUND)
			return new Tile(ImageLoader.getImage("/images/tiles/dirt.jpg"), false, x, y, tileGrid);
		if(tilename == TileType.DIRT)
			return new Tile(ImageLoader.getImage("/images/tiles/dark_dirt.jpg"), true, x, y, tileGrid);
		if(tilename == TileType.GRASS)
			return new Tile(ImageLoader.getImage("/images/tiles/grass.jpg"), true, x, y, tileGrid);
		
		return null;
	}
	
	/**
	 * Creates a new ant at the same place as the given sprite.
	 * 
	 * @param t - The kind of ant.
	 * @param c - The colony the ant is to belong to.
	 * @param s - The sprite whose location is to be taken to create the ant.
	 * 
	 * @return A new ant.
	 */
	public static Ant createAnt(AntType t, Colony c, Sprite s)
	{		
		return createAnt(t, c, s.myX, s.myY);
	}
	
	/**
	 * Creates a new ant at the given location.
	 * 
	 * @param t - The kind of ant.
	 * @param c - The colony the ant is to belong to.
	 * @param x - The x location of the ant.
	 * @param y - The y location of the ant.
	 * 
	 * @return A new ant.
	 */
	public static Ant createAnt(AntType t, Colony c, int x, int y)
	{
		Ant a = null;
		if(t == AntType.NEWQUEEN)
			return null;
		if(t == AntType.QUEEN)
			a = new Ant(x, y, QUEEN_STRENGTH, t, c);
		if(t == AntType.SOLDIER)
			a = new Ant(x, y, SOLDIER_STRENGTH, t, c);
		if(t == AntType.WORKER)
			a = new Ant(x, y, WORKER_STRENGTH, t, c);
				
		return a;
	}
}
