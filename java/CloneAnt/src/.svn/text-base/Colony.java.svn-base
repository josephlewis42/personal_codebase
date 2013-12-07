import java.util.ArrayList;


/**
 * A representation of an ant colony.
 * 
 * @author Joseph Lewis <joehms22@gmail.com>
 */
public class Colony
{
	private Grid myMap;
	private String myName; //"red" or "black", used in fetching tiles.
	Tile startTile;
	private Ant myQueen;
	private Game myGame;
	
	/**
	 * Creates a colony on the given grid with the given name. The name corresponds to 
	 * image prefixes in the images/sprites folder i.e. black would use all images that
	 * begin with black_ for its ants.
	 * 
	 * Also digs out the basic colony and creates a Queen.
	 * 
	 * @param g - The grid to start the colony on.
	 * @param name - The name of the colony.
	 * @param myGame - The game this colony belongs to (to add new ants to list).
	 */
	public Colony(Grid g, String name, Game myGame)
	{
		myMap = g;
		myName = name;
		this.myGame = myGame;
		
		//Dig a nest.
		for(int i = 0; i <= g.getHeight()/3; i++)
			g.myTerrain[g.getWidth()/2][i].digAndLink(true);
		
		startTile = g.myTerrain[g.getWidth()/2][g.getHeight()/3];
		startTile.food = 3;
		
		myQueen = Factory.createAnt(AntType.QUEEN, this, startTile);
		myQueen.hatch();
		myGame.addSprite(myQueen);
		
		Ant worker1 = Factory.createAnt(AntType.WORKER, this, startTile);
		worker1.hatch();
		myGame.addSprite(worker1);
		
		Ant worker2 = Factory.createAnt(AntType.WORKER, this, startTile);
		worker2.hatch();
		myGame.addSprite(worker2);
	}
	
	/**
	 * Returns the amount of food this colony has in its nest.
	 */
	public int getFood()
	{
		return myMap.getFood();
	}
	
	/**
	 * Gets this colony's grid.
	 */
	public Grid getGrid()
	{
		return myMap;
	}

	public String getMyName()
	{
		return myName;
	}

	public Tile getStartTile()
	{
		return startTile;
	}

	public Ant getQueen()
	{
		return myQueen;
	}

	public Game getGame()
	{
		return myGame;
	}
	
	/**
	 * Lays a new egg for a new ant of the type given.
	 * 
	 * @param t
	 */
	public synchronized void newAnt(AntType t)
	{
		myGame.addSprite(Factory.createAnt(t, this, myQueen));
	}
	
	/**
	 * Takes 1 food from a tile in the nest.
	 * Returns True if there was enough food.
	 * Returns False if there was not.
	 */
	public boolean takeFood()
	{
		for(Tile[] t : myMap.myTerrain)
			for(Tile ti : t)
			{
				if(ti.food > 0)
				{
					ti.pickFood();
					return true;
				}
			}
		return false;
	}
	
	/**
	 * Returns the image for the given ant type in this colony
	 * (the red colony will return red ants, while the black 
	 * will return black! :)
	 * 
	 * To cut down on the number of comparisons, put the most
	 * numerous types of ants first!
	 * 
	 * @param t
	 * @return
	 */
	public String getImageLocation(AntType t)
	{		
		String loc = "";
		switch(t)
		{
		case SOLDIER: 	loc = "/images/sprites/"+myName+"_soldier.png";	break;
		case WORKER: 	loc = "/images/sprites/"+myName+"_worker.png"; 	break;
		case NEWQUEEN: 	loc = "/images/sprites/"+myName+"_newqueen.png"; break;
		case QUEEN: 	loc = "/images/sprites/"+myName+"_queen.png"; 	break;
		case DEAD: 		loc = "/images/sprites/"+myName+"_dead.png"; 	break;
		}
		return loc;

	}
		
	/**
	 * Returns true if this colony is dead, false if it is not.
	 */
	public boolean checkEndgame()
	{
		if(myQueen != null && myQueen.isAlive())
			return false;
		return true;
	}
	
	/**
	 * Returns the members of this colony.
	 * 
	 * @return
	 */
	public Ant[] getMembers()
	{
		ArrayList<Ant> myAnts = new ArrayList<Ant>();
		
		for(Sprite s: myGame.getActors())
			if(s instanceof Ant)
			{
				Ant j = (Ant) s;
				if(j.getColony() == this)
					myAnts.add(j);
			}
		
		return myAnts.toArray(new Ant[0]);
	}
	
	/**
	 * Returns true if the nest is big enough for all of the ants.
	 * There should be 4 spaces underground for every ant.
	 * 
	 * @return true if the nest is big enough, false otherwise.
	 */
	public boolean enoughDug()
	{
		return getMembers().length * 4 < myMap.getNumDug();
	}
}
