package Game;

public class AntFight extends Sprite
{
	Ant one, two;
	
	int fight_length = 5;
	
	Game myGame;
	
	public AntFight(Ant a, Ant b)
	{
		super(a);
		
		
		myGame = a.getColony().getGame();
		one = a;
		two = b;

		// Remove these sprites from being played and add me.
		myGame.addSprite(this);
		myGame.removeSprite(a);
		myGame.removeSprite(b);
		
		a.getTile().setSprite(null);
		
		a.canMove = false;
		b.canMove = false;
		
		myImg = ImageLoader.getImage(ImageType.ANT_FIGHT);

	}

	public void move()
	{
		fight_length--;
		
		if(fight_length == 0)
		{
			one.attack(two);
			
			myGame.removeSprite(this);
			myGame.addSprite(one);
			myGame.addSprite(two);
			
			one.canMove = true;
			two.canMove = true;
		}
	}

}
