/**
 * A representation of a generic ant.
 * 
 * @author Joseph Lewis <joehms22@gmail.com>
 * 
 */
public class Ant extends Sprite
{
	private Colony myColony;
	private int myStrength;
	AntType myType;
	
	private int myFood = 200;
	private boolean	alive 		 = true;		
	private boolean isHatched 	 = false;	
	public 	boolean canMove 	 = true;		//False if in battle or stuck in rain etc.
	private boolean carryingFood = false;	
	
	Directive myDirective;
	
	public static Ant thePlayer = null; // The magical player, some say the gods speak to it!
	
	/**
	 * Returns whether or not this Ant has been hatched.
	 */
	public boolean getHatched() { return isHatched; }
	
	/**
	 * Hatch the ant.
	 */
	public void hatch() { isHatched = true; }
	
	/**
	 * Makes the Ant pick up food from the tile if it can.
	 * Returns True if the ant has food, false otherwise.
	 */
	public boolean pickFood() 
	{
		if(!carryingFood && getTile().pickFood())
			carryingFood = true;
		
		return carryingFood;	
	}
	
	/**
	 * Makes the Ant drop the food on this tile if it has
	 * food and if the tile isn't full.
	 * 
	 * @return True if the ant was able to place the food.
	 */
	public boolean placeFood()
	{
		if(carryingFood && getTile().placeFood())
			carryingFood = false;
		
		return ! carryingFood;
	}
	
	/**
	 * Returns true if the Ant is carrying food, false otherwise.
	 */
	public boolean hasFood() { return carryingFood; }

	/**
	 *  Returns true if this ant is alive, false otherwise.
	 */
	public boolean isAlive() { return alive; }
	
	/**
	 * Attacks this ant.
	 * 
	 * @param attacking
	 */
	public void attack(Ant attacking)
	{
		// What is the chance this ant wins in a battle against the attacker?
		double thisWins = (double)myStrength / (attacking.getStrength() + myStrength);
			
		// Determine the winner!
		double dice = Math.random();
		
		if(dice < thisWins) //This ant won, yay!
			attacking.kill();
		else //Opponent won.
			alive = false;
	}
	
	/** 
	 * Returns the colony to which this ant belongs.
	 */
	public Colony getColony() { return myColony; }
	
	/**
	 * Returns the strength for this Ant.
	 */
	public int getStrength() { return myStrength; }
	
	
	/** Sets the living status of this ant to false **/
	private void kill() { alive = false; }
	
	
	/**
	 * Creates a new Ant on the colony's grid.
	 * 
	 * @param x - The x position of the ant on the grid.
	 * @param y - The y position of the ant on the grid.
	 * @param strength - The strength of the Ant.
	 * @param type - The type of ant this is.
	 * @param col - The colony that this ant belongs to (used for color generation).
	 */
	public Ant(int x, int y, int strength, AntType type, Colony col)
	{
		super(x,y, col.getGrid(), col.getImageLocation(type));
		
		myStrength = strength;
		myType = type;
		myColony = col;
	}
	
	/**
	 * Is this Ant in its colony?
	 */
	public boolean isHome() { return myMap == myColony.getGrid(); }
	
	
	public void move()
	{
		if(!alive)
		{
			decompose();
			return;
		}
		
		if(canMove)
		{
			// Check for change in directive.
			if(myDirective == null)
				DirectiveFactory.direct(this);
					
			// Hand over control to directive.		
			if( myDirective.move() == true)
				myDirective = null;
		}
		
		if(isHatched && alive)
		{
			myFood--;
			
			if(myFood <= 0)
				if(myColony.takeFood())
					myFood = 200;
				else
					kill();
		}
	}
	
	
	/**
	 * Moves the ant to the given tile, if the tile is underground
	 * dig it up.
	 */
	protected void moveTo(Tile t)
	{
		getTile().removeSprite(this); // Remove this ant from the current tile.
		super.moveTo(t); // Move to the given tile.
		
		// Ant specific stuff.
		if(t.isUnderground && ! t.isDug)
			t.dig();
		
		// Check if there is an ant in the tile we are occupying.
		Ant there = t.setSprite(this);
		
		if(there != null && there.getColony() != myColony) // Hey, you look funny, let's fight!
		{
			new AntFight(there, this);
		}
	}
	
	/**
	 * Remove this ant from the game.
	 */
	public void decompose()
	{
		getTile().removeSprite(this);
		new DecomposingAnt(this);
	}
	
	/**
	 * Returns a string which represents this specific ant.
	 * <pre>
	 * Black Soldier
	 * Alive: True
	 * Hatched: True
	 * ...
	 * </pre>
	 */
	public String toString()
	{
		String build = "";
		build += myColony.getMyName() + " " + myType;
		build = build.toUpperCase();
		return build+"\nAlive: "+alive+"\nHatched: "+isHatched+
				"\nFood: "+myFood+"\nCan Move: "+canMove+
				"\nCarrying Food: "+carryingFood;
	}
}