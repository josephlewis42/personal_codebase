package Game.Directive;

import java.util.ArrayList;

import Game.Ant;
import Game.DirectiveFactory;
import Game.Tile;

/**
 * Moves toward a given Tile in a leisurely manner; if the given
 * tile is NE of here, any tile can be chosen to get there, unless it
 * is the three directions moving away from the given tile (i.e. SW, W, or S)
 * this should provide a realistic looking way to get around.
 * 
 * If the given tile is not on this map, 
 * 
 * @author Joseph Lewis <joehms22@gmail.com>
 *
 */
public class Meander extends Directive
{
	private static final int DIST_TO_RELEASE = 0; //How far away we can be before we exit.
	private Tile dest; //The tile we want to go to.
	
	public Meander(Ant s, Tile location)
	{
		super(s);
		dest = location;
	}

	public boolean move()
	{
		// If we are close enough to the tile, just exit.
		if(mySprite.getTile().getDistance(dest) <= DIST_TO_RELEASE)
			return true;
		
		if(runPrecursor())
			return false;
		
		// Check if the given tile is on this map, if not try to move to a map that can get us there.
		if(dest.myMap != mySprite.myMap)
		{
			Tile[] t = mySprite.myMap.getLinksTo(dest.myMap.gridType);
			
			if(t.length != 0) //If this map links to the map wanted, go there.
				precursor = new GoTo(mySprite, dest.getClosest(t));
			
			else // If not, go to the surface.
				precursor = DirectiveFactory.goSurface(mySprite);
		}
			
		if(runPrecursor())
			return false;
		
		
		// We just be on the right map, and not close enough to the tile, huzzah!
		Tile[] neighbors = mySprite.getGrid().getPossibleMoves(mySprite.getTile());
		ArrayList<Tile> myNeighbors = new ArrayList<Tile>();
		
		for(Tile t: neighbors)
			myNeighbors.add(t);
		
		// Remove the farthest three tiles.
		Tile far = dest.getFarthest(neighbors);
		Tile[] farNeighbors = mySprite.getGrid().getPossibleMoves(far);
		
		myNeighbors.remove(far);
		for(Tile t: farNeighbors)
			myNeighbors.remove(t);
				
		// Move to one of the remaining tiles.
		mySprite.moveTo(random(myNeighbors));
		
		return false;
	}
}