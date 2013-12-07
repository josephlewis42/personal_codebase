package Game.Directive;

import Game.*;

/**
 * Stalks the given ant.
 * 
 * @author Joseph Lewis <joehms22@gmail.com>
 *
 */
public class Follow extends Directive
{

	public Ant toFollow;
	
	/**
	 * Follows the given at as best as possible, until it dies.
	 * 
	 * @param s
	 * @param other
	 */
	public Follow(Ant s, Ant other)
	{
		super(s);
		toFollow = other;
		
	}

	
	public boolean move()
	{
		if(! toFollow.isAlive())
			return true;
		
		precursor = DirectiveFactory.goTo(mySprite, toFollow.getTile());
		
		if(runPrecursor())
			return false;
				
		return false;
	}

}
