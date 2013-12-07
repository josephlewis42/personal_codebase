package Game.Directive;
import java.util.ArrayList;
import java.util.Collections;

import Game.*;

/**
 * A directive that just moves randomly.
 * 
 * @author Joseph Lewis <joehms22@gmail.com>
 *
 */
public class Wander extends Directive
{
	private Tile lastTile = null;
	private int timeoutLeft = 0;
	private boolean timeout = false;
	
	/**
	 * Makes the given ant just wander for five moves..
	 * 
	 * @param s
	 */
	public Wander(Ant s)
	{
		this(s, 5);
	}
	
	/**
	 * Makes the given ant wander for timeout number of moves.
	 * @param s
	 * @param timeout
	 */
	public Wander(Ant s, int timeout)
	{
		super(s);
		timeoutLeft = timeout;
		this.timeout = true;
	}

	public boolean move()
	{
		timeoutLeft--;
		if(timeout && timeoutLeft <=0)
			return true;
				
		// We must be in the nest and next to dirt, yay!
		ArrayList<Tile> tiles = new ArrayList<Tile>();
		
		for(Tile x : mySprite.getPossibleMoves())
			tiles.add(x);
		
		Collections.shuffle(tiles);
		
		
		for(Tile t: tiles)
			if(t.isDug)
				if(t != lastTile)
				{
					lastTile = mySprite.getTile();
					mySprite.moveTo(t);
					return false;
				}
		//Can't go anymore, reset last tile.		
		lastTile = null;
		return true;
	}
}