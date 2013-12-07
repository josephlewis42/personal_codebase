package Game;
import Game.Directive.*;

/**
 * Creates complex directives out of simple ones.
 * 
 * @author Joseph Lewis <joehms22@gmail.com>
 *
 */
public class DirectiveFactory
{
	/**
	 * Creates a new directive and sets it for the given ant.
	 * 
	 * @param s
	 */
	public static void direct(Ant s)
	{
		s.myDirective = getDirective(s);
	}
	
	/**
	 * This directive controls the ant.
	 * 
	 * @param s
	 */
	private static Directive getDirective(Ant s)
	{
		// Check for hatched ant.
		if(! s.getHatched() )
			return new Hatch(s);
		
		// Check for can move.
		if(! s.canMove )
			return new Wait(s, 1);
		
		// If this is the mythic player do nothing.
		if(s == Ant.thePlayer)
			return new Wait(s, 1);
		
		// If this ant is carrying food, send them home to drop it.
		if(s.hasFood())
			return getFood(s);
		
		// If this ant is a soldier, and we are ready to attach the other colony, do it.
		// The colony which the player belongs to doesn't get to attack, unless the player 
		// leads.
		if(s.getColony() != Ant.thePlayer.getColony() && s.getColony().attackReady())
		{
			System.out.println("DirectiveFactory.java DEBUG Attacking!");
			// "Follow" the other colony's Queen, we're not talkin' 'bout twitter!
			return new Follow(s, Ant.thePlayer.getColony().getQueen()); 
		}
		
		// If this ant isn't home, but is on top of food, pick it up and send them back.
		if(! s.isHome() && s.getTile().getFood() > 0)
			return getFood(s);
		
		// Get variables from ant.
		AntType myType = s.myType;
		Colony 	myCol  = s.getColony();
		
		// Queens lay eggs, that is all.
		if(myType == AntType.QUEEN)
			return new LayEggs(s);
		
		// TODO add attack directive!
		if(! myCol.enoughDug() )
			return DirectiveFactory.dig(s);
		
		
		return DirectiveFactory.getFood(s);
	}
	
	/**
	 * Waits for a turn to be completed.
	 * 
	 * @param s
	 * @return
	 */
	public static Directive wait(Ant s)
	{
		return new Wait(s, 1);
	}
	
	/**
	 * Makes the ant wander around.
	 * 
	 * @param s
	 */
	public static Directive wander(Ant s)
	{
		return new Wander(s);
	}

	/**
	 * Makes the ant grow and hatch.
	 * 
	 * @param s
	 */
	public static Directive hatch(Ant s)
	{
		return new Hatch(s);
	}
	
	/**
	 * Makes the ant move one random square.
	 * 
	 * @param s
	 * @return
	 */
	public static Directive oneRandom(Ant s)
	{
		return new Wander(s, 2);
	}
	
	/**
	 * Makes the ant go home, if not already there.
	 * 
	 * @param s
	 * @return
	 */
	public static Directive goHome(Ant s)
	{
		//Go home if the ant is not there.
		//Get my colony type.
		GridType ct = s.getColony().getGrid().gridType;
		
		if(s.myMap.gridType == ct)
			return null; //Ant is home.
		
		//If ant is not on surface, go there before home.
		Tile[] links;
		
		Directive pre = null;
		
		if(s.myMap.gridType != GridType.SURFACE)
		{
			pre = goSurface(s);
			links = s.myMap.parent.getLinksTo(ct);
		}
		else // We are on the surface
		{
			links = s.myMap.getLinksTo(ct);
		}		
		
		Tile closest = s.getTile().getClosest(links);
		
		Directive goHome = goTo(s, closest);
		goHome.precursor = pre;
		return goHome;
	}
		
	/**
	 * Makes the ant go to the surface, if not already there.
	 * 
	 * @param s
	 * @return
	 */
	public static Directive goSurface(Ant s)
	{
		//Go to the surface if the ant is not there.
		if(s.myMap.gridType == GridType.SURFACE)
			return null;
		
		Tile[] links = s.myMap.getLinksTo(GridType.SURFACE);
		
		Tile closestExit = s.getTile().getClosest(links);
		
		if(closestExit == null)
			return null;
		
		return goTo(s, closestExit);
	}
	
	/**
	 * Makes the ant dig five tiles.
	 * 
	 * @param s
	 * @return
	 */
	public static Directive dig(Ant s)
	{
		return new Dig(s, 5);
	}
	
	/**
	 * Makes the ant GoTo the given tile.
	 * 
	 * @param s
	 * @param t
	 * @return
	 */
	public static Directive goTo(Ant s, Tile t)
	{
		return new GoTo(s,t);
	}
	
	/**
	 * The job of a Queen!
	 * 
	 * @param s
	 * @return
	 */
	public static Directive layEgg(Ant s)
	{
		return new LayEggs(s);
	}
	
	/**
	 * Fetching food keeps the colony sustained!
	 */
	public static Directive getFood(Ant s)
	{
		return new GetFood(s);
	}
	
	public static Directive follow(Ant s, Ant other)
	{
		return new Follow(s, other);
	}
	
	public static Directive meander(Ant s, Tile t)
	{
		return new Meander(s,t);
	}
}
