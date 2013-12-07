package Game.Directive;
import java.util.ArrayList;
import java.util.Collections;

import Game.*;

/**
 * A directive that has the Ant dig.
 * 
 * @author Joseph Lewis <joehms22@gmail.com>
 */
public class Dig extends Directive
{
	private int amount;

	private Direction d;
	
	/**
	 * Creates a new directive.
	 * 
	 * @param s - The ant whose directive this is.
	 * @param amount - The amount to dig in tiles.
	 */
	public Dig(Ant s, int amount)
	{
		super(s);
		this.amount = amount;
	}

	public boolean move()
	{
		if(runPrecursor())
			return false;
				
		// Are we in our home?
		if(!mySprite.isHome())
			precursor = DirectiveFactory.goHome(mySprite);
		
		// Check if there is no dirt around here.
		else if(mySprite.getPossibleMoves().length <= mySprite.getDugMoves().length)
			precursor = DirectiveFactory.oneRandom(mySprite);
		
		// Try running the precursor again.
		if(runPrecursor())
			return false;
		
		// We must be in the nest and next to dirt, yay!
		ArrayList<Tile> t = new ArrayList<Tile>();
		
		for(Tile x : mySprite.getPossibleMoves())
			t.add(x);
		
		// If we already have a direction set try to go that way again.
		if(d != null)
		{
			for(Tile ti : t)
				if(ti.getRelation(mySprite.getTile()) == d)
				{
					if(ti.isDug == false)
					{
						mySprite.moveTo(ti);
						amount--;
						return amount <= 0;
					}
				}
		}

		Collections.shuffle(t);
		
		for(Tile ti: t)
			if(ti.isDug == false)
			{
				amount--;
				d = ti.getRelation(mySprite.getTile());
				mySprite.moveTo(ti);
				return amount <= 0;
			}
		
		return true;
	}
}