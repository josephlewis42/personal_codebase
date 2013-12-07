package Game.Directive;
import java.util.ArrayList;

import Game.Ant;
import Game.DirectiveFactory;
import Game.GridType;
import Game.Tile;


public class GetFood extends Directive
{
	private ArrayList<Tile> mostRecent = new ArrayList<Tile>();
	private int scent = 0;
	
	public GetFood(Ant s)
	{
		super(s);
	}

	public boolean move()
	{	
		if(! mySprite.hasFood())
		{
			if(runPrecursor())
				return false;
			
			// Move above ground if not there.
			if(mySprite.myMap.gridType != GridType.SURFACE)
				precursor = DirectiveFactory.goSurface(mySprite);
			
			if(runPrecursor())
				return false;
						
			// Choose the best looking ground as to food.
			Tile bestTile = null;
			boolean bestTileUpdated = false;
			
			for(Tile t : mySprite.getPossibleMoves())
			{				
				if(bestTile == null)
					bestTile = t;
				else
					if(t.scent >= bestTile.scent)
						if(t.getFood() > 0)
						{
							mySprite.moveTo(t);
							mySprite.pickFood();							
							return false;
						}
						else
						{
							//Make sure we haven't been here recently.
							if((t.scent >  bestTile.scent && ! mostRecent.contains(t)) || t.hasFood())
							{
								bestTile = t;
								bestTileUpdated = true;
							}
						}
			}
			
			if(! bestTileUpdated)
			{
				precursor = DirectiveFactory.meander(mySprite, mySprite.getColony().getGame().getFoodLocation());
				precursor.move();
				precursor = null;
			}
			else
			{
				mostRecent.add(bestTile);
				mySprite.moveTo(bestTile);
			}
		}
		else
		{
			if(!mySprite.isHome())
				precursor = DirectiveFactory.goTo(mySprite, mySprite.getColony().getStartTile());
			
			if(runPrecursor())
			{
				scent --;
				mySprite.getTile().updateScent(scent);
				return false;
			}
			
			//Sprite must be in home tile.
			// Go to the middle tile at home, and drop the food if the tile has space,
			
			if(mySprite.placeFood())
				return true;
			else // If not move around until there is space.
				precursor = DirectiveFactory.oneRandom(mySprite);

		}
		return false;
	}
}