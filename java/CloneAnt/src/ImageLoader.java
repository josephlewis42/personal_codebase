import java.awt.Image;
import java.net.URL;
import java.util.TreeMap;

import javax.swing.ImageIcon;


/**
 * An image loader that caches images and will return the cashed versions
 * by default. Good on memory!
 * 
 * @author Joseph Lewis <joehms22@gmail.com>
 */
public class ImageLoader
{
	private static TreeMap<String, Image> mapper = new TreeMap<String, Image>();
	
	/**
	 * Fetches the image from the class/folder or from the cache.
	 * The startup time of the program dropped about five seconds 
	 * after introducing the cache, I'm sure the memory footprint
	 * dropped too :) - Joe
	 * 
	 * @param imgLocation The location of the image.
	 * @return An Image.
	 */
	public static Image getImage(String imgLocation)
	{
		if(mapper.get(imgLocation) != null)
			return mapper.get(imgLocation);
		
		URL imageURL = Factory.class.getResource(imgLocation);

		if (imageURL != null) 
		{	
				Image j = new ImageIcon(imageURL).getImage();
				mapper.put(imgLocation, j);
				return j;
		}
		else
			System.err.println("Resource not found: "+imgLocation);
		
		return null;
	}
	
	/**
	 * Returns the image for the specific image type found in ImageType.java
	 * 
	 * @param i
	 * @return
	 */
	public static Image getImage(ImageType i)
	{
		if(i == ImageType.SMALLEGG)
			return getImage("/images/sprites/egg_sm.png");
		
		if(i == ImageType.MEDEGG)
			return getImage("/images/sprites/egg_me.png");
		
		if(i == ImageType.LARGEEGG)
			return getImage("/images/sprites/egg_lg.png");
		
		if(i == ImageType.YELLOWSOLDIER)
			return getImage("/images/sprites/yellow_soldier.png");
		
		if(i == ImageType.SURFACE_TILE)
			return getImage("/images/tiles/dirt.jpg");
		
		if(i == ImageType.SURFACE_ONE_FOOD)
			return getImage("/images/tiles/dirt_1.jpg");
		
		if(i == ImageType.SURFACE_TWO_FOOD)
			return getImage("/images/tiles/dirt_2.jpg");

		if(i == ImageType.SURFACE_THREE_FOOD)
			return getImage("/images/tiles/dirt_3.jpg");

		if(i == ImageType.SURFACE_FOUR_FOOD)
			return getImage("/images/tiles/dirt_4.jpg");

		if(i == ImageType.SURFACE_FIVE_FOOD)
			return getImage("/images/tiles/dirt_5.jpg");
		
		if(i == ImageType.HOLE)
			return getImage("/images/tiles/hole.jpg");
		
		if(i == ImageType.ANT_FIGHT)
			return getImage("/images/sprites/ant_fight.png");
		
		return null;
	}
}
