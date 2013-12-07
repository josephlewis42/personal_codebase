/**
 * The class sends the given ant to the given tile.
 * 
 * @author Joseph Lewis <joehms22@gmail.com>
 *
 */
public class GoTo extends Directive
{
	public static boolean DEBUGGING = false;
	
	Tile myTile; //The tile we are going to.
	Tile lastTile; //The last tile we were at (don't go there again if we are lost).
	
	public GoTo(Ant s, Tile t)
	{
		super(s);
		myTile = t;
	}

	public boolean move()
	{		
		if(runPrecursor())
			return false;
		
		//Check if this tile is on this map, if not try to move to a map that can get us there.
		if(myTile.myMap != mySprite.myMap)
		{
			Tile[] t = mySprite.myMap.getLinksTo(myTile.myMap.getType());
			
			if(t.length != 0) //If this map links to the map wanted, go there.
				precursor = new GoTo(mySprite, myTile.getClosest(t));
			
			else // If not, go to the surface.
				precursor = DirectiveFactory.goSurface(mySprite);
		}
			
		if(runPrecursor())
			return false;
		
		Tile[] possibleMoves = mySprite.getPossibleMoves();
		
		Tile t = myTile.getClosest(possibleMoves);
		
		if(DEBUGGING)
		{
			System.out.println("Wanted: "+myTile);
			System.out.println("Closest: "+t);
		}
		
		mySprite.moveTo(t);
		if(t == myTile)
		{
			if(myTile.getPortal() == null)
			{
				//If carrying food, drop it.
				if(mySprite.hasFood())
				{
					mySprite.placeFood();
				}
				else
					if(t.food > 0 && ! mySprite.hasFood())
						mySprite.pickFood();
			}
			
			return true;
		}
		return false;
	}
}