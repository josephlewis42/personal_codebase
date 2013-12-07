
public class DecomposingAnt extends Sprite
{

	Game myGame = null;
	
	private int untilDecomposed = 80;
	
	public DecomposingAnt(Ant s)
	{
		super(s.myX, s.myY, s.getGrid());
		
		myGame = s.getColony().getGame();
		
		myGame.removeSprite(s);
		myGame.addSprite(this);
		
		
		myImg = ImageLoader.getImage(
					s.getColony().getImageLocation(AntType.DEAD));
		
	}

	public void move() { 
		untilDecomposed--;
		
		if(untilDecomposed == 0)
			myGame.removeSprite(this);
	}

}
