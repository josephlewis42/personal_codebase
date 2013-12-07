package Game;

public class DecomposingAnt extends Sprite
{

	Game myGame = null;
	
	private int untilDecomposed = 80;
	
	public DecomposingAnt(Ant s)
	{
		super(s);
		
		myGame = s.getColony().getGame();
		
		s.getTile().removeSprite(s);
		
		myGame.removeSprite(s);
		myGame.addSprite(this);
		
		
		myImg = ImageLoader.getImage(
					s.getColony().getImageLocation(AntType.DEAD));
		
	}

	public void move() 
	{ 
		untilDecomposed--;
		
		if(untilDecomposed == 0)
			myGame.removeSprite(this);
	}

}
