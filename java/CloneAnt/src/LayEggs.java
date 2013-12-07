
public class LayEggs extends Directive
{
	private static int MAX_TURNS_TO_LAY_EGG = 50;
	private static int MIN_TURNS_TO_LAY_EGG = 15;
	private int currentTurnsToLay = MAX_TURNS_TO_LAY_EGG; //Slowly decrease
	int turnsToLay = currentTurnsToLay;
	
	public LayEggs(Ant s)
	{
		super(s);
	}

	public boolean move()
	{
		if(! mySprite.isHome())
			precursor = DirectiveFactory.goHome(mySprite);
		
		if(runPrecursor())
			return false;
			
		turnsToLay--;
				
		if(turnsToLay == 0)
		{
			if(currentTurnsToLay > MIN_TURNS_TO_LAY_EGG)
				currentTurnsToLay--;
			
			turnsToLay = currentTurnsToLay;
			
			if(Math.random() < .7)
				//new worker
				mySprite.getColony().newAnt(AntType.WORKER);
			else
				mySprite.getColony().newAnt(AntType.SOLDIER);
			
			//Move one randomly.
			precursor = DirectiveFactory.oneRandom(mySprite);
		}
		
		return false; // Lay eggs until you die!
	}

}
