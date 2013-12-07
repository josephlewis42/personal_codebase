import java.util.ArrayList;

/**
 * A directive tells an Ant how to move every turn. Example directives could be:
 * Go Home, Dig, Wander, Attack, Chase...
 * 
 * @author Joseph Lewis <joehms22@gmail.com>
 *
 */
public abstract class Directive
{
	Ant mySprite;
	Directive precursor; //A directive to be run before this one.

	/**
	 * Creates a directive for this ant.
	 * 
	 * @param s
	 */
	public Directive(Ant s)
	{
		mySprite = s;
	}
	
	/**
	 * @return True if this directive is completed.
	 */
	public abstract boolean move();
	
	/**
	 * Runs a precursor, returns true if there was a precursor and it ran.
	 * 
	 * A precursor is another directive that needs to be completed before
	 * this one is run; therefore complex directives can be created out of
	 * simple ones: Kill Queen could be, leave nest, go to other nest, stalk
	 * queen.
	 * 
	 * @return Was there a precursor, and did it run?
	 */
	public boolean runPrecursor()
	{
		if(precursor == null)
			return false;
		
		if(precursor.move())
			precursor = null;
		
		return true;
	}
	
	
	/**
	 * Chooses a random tile from the given ones, returns null if there are no tiles.
	 * 
	 * @param tiles
	 * @return
	 */
	public Tile random(Tile[] tiles)
	{
		try
		{
			return tiles[(int) (Math.random()*tiles.length)];
		}catch(ArrayIndexOutOfBoundsException ex)
		{
			return null;
		}
	}
	
	public Tile random(ArrayList<Tile> tiles)
	{
		return random(tiles.toArray(new Tile[0]));
	}

}
