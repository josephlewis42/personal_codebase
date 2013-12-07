import java.awt.Image;

/**
 * Grows the ants in position until ready to "hatch" from their eggs.
 * 
 * @author Joseph Lewis
 *
 */
public class Hatch extends Directive
{
	private static int TURNS_TO_HATCH = 200;
	private static int TURNS_TO_MED = (TURNS_TO_HATCH / 3) * 2; // 2/3 of the way left.
	private static int TURNS_TO_LG = (TURNS_TO_HATCH / 3); // 1/3 of the way left.

	int turnsLeft = 200;
	Image img;
	
	public Hatch(Ant s)
	{
		super(s);
		
		// Store image.
		img = mySprite.myImg;
		mySprite.myImg = ImageLoader.getImage(ImageType.SMALLEGG);
	}

	public boolean move()
	{
		turnsLeft--;
		
		if(turnsLeft == TURNS_TO_MED)
			mySprite.myImg = ImageLoader.getImage(ImageType.MEDEGG);
			
		if(turnsLeft == TURNS_TO_LG)
			mySprite.myImg = ImageLoader.getImage(ImageType.LARGEEGG);
		
		if(turnsLeft <= 0)
		{
			mySprite.hatch();
			mySprite.myImg = img; // Restore the image.
			return true; // Alert that we are done.
		}
		
		return false;
	}

}
