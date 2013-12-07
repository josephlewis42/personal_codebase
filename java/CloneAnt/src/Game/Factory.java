package Game;

/**
 * A multi-purpose factory for creating all sorts of things.
 * 
 * @author Joseph Lewis <Joehms22@gmail.com>
 *
 */
public class Factory
{
	// Sizes of Grids.
	private static final int SURFACE_HEIGHT = 50;
	private static final int SURFACE_WIDTH = 70;
	private static final int NEST_HEIGHT = 50;
	private static final int NEST_WIDTH = 50;
	
	
	// Strengths (Used in determining the outcomes of battles).
	private static final int NEWQUEEN_STRENGTH = 3;
	private static final int QUEEN_STRENGTH = 8;
	private static final int SOLDIER_STRENGTH = 2;
	private static final int WORKER_STRENGTH = 1;
		
	/**
	 * Creates a new grid with no parent.
	 * 
	 * @param p
	 * @return
	 */
	public static Grid createGrid(GridType p)
	{
		if(p == GridType.BLACKNEST || p == GridType.REDNEST)
		{
			Grid g = new Grid(NEST_WIDTH, NEST_HEIGHT, p, Grid.surfaceGrid);
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
			Grid g = new Grid(SURFACE_WIDTH, SURFACE_HEIGHT, p, null);
		
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
			return new Tile(ImageLoader.getImage(ImageType.SURFACE_TILE), false, x, y, tileGrid);
		if(tilename == TileType.DIRT)
			return new Tile(ImageLoader.getImage(ImageType.UNDUG), true, x, y, tileGrid);
		if(tilename == TileType.GRASS)
			return new Tile(ImageLoader.getImage(ImageType.GRASS), true, x, y, tileGrid);
		
		return null;
	}
	
	/**
	 * Creates a new ant for the given colony..
	 * 
	 * @param t - The kind of ant.
	 * @param c - The colony the ant is to belong to.
	 * 
	 * @return A new ant.
	 */
	public static Ant createAnt(AntType t, Colony c)
	{
		// If there is a queen, new ants are created here, else they are 
		// started at the center of the nest.
		Sprite start = (c.getQueen() != null)? c.getQueen():c.getStartTile();
		
		int x = start.myX;
		int y = start.myY;
		
		Ant a = null;
		
		switch(t) {
		case NEWQUEEN:	a = new Ant(x, y, NEWQUEEN_STRENGTH, t, c);	break; 
		case QUEEN:		a = new Ant(x, y, QUEEN_STRENGTH, t, c);	break; 
		case SOLDIER:	a = new Ant(x, y, SOLDIER_STRENGTH, t, c);	break;
		case WORKER:	a = new Ant(x, y, WORKER_STRENGTH, t, c);	break;
		}
							
		return a;
	}
	
}
