package Game;

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
	private Tile startTile;
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
		for(int i = 0; i <= g.height/3; i++)
			g.myTerrain[g.width/2][i].digAndLink(true);
		
		startTile = g.myTerrain[g.width/2][g.height/3];
		startTile.setFood(3);
		
		myQueen = Factory.createAnt(AntType.QUEEN, this);
		myQueen.hatch();
		myGame.addSprite(myQueen);
		
		Ant worker1 = Factory.createAnt(AntType.WORKER, this);
		worker1.hatch();
		myGame.addSprite(worker1);
		
		Ant worker2 = Factory.createAnt(AntType.WORKER, this);
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
		myGame.addSprite(Factory.createAnt(t, this));
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
				if(ti.getFood() > 0)
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
	 * @param t
	 * @return
	 */
	public String getImageLocation(AntType t)
	{
		return "/images/sprites/"+myName+"_"+t.toString().toLowerCase()+".png";
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
	 * Returns the alive members of this colony.
	 * 
	 * @return An array of Ants in this colony.
	 */
	public Ant[] getMembers()
	{
		ArrayList<Ant> myAnts = new ArrayList<Ant>();
		
		for(Sprite s: myGame.getActors())
			if(s instanceof Ant)
			{
				Ant j = (Ant) s;
				if(j.getColony() == this && j.isAlive() && j.getHatched())
					myAnts.add(j);
			}
		
		return myAnts.toArray(new Ant[0]);
	}
	
	/**
	 * Returns members of this colony that are of the given type, all
	 * must be alive and hatched to be returned.
	 * 
	 * @return An array of ants in this colony that are the given type.
	 */
	public Ant[] getMembers(AntType t)
	{
		ArrayList<Ant> myAnts = new ArrayList<Ant>();
		
		for(Sprite s: myGame.getActors())
			if(s instanceof Ant)
			{
				Ant j = (Ant) s;
				if(j.getColony() == this && j.myType == t && j.isAlive() && j.getHatched())
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
	
	/**
	 * Returns true if we are ready to attack, double food than ants
	 * at least five soldiers, and big enough nest.
	 */
	public boolean attackReady()
	{
		return (enoughDug() && (getMembers(AntType.SOLDIER).length >= 5));
	}
}
