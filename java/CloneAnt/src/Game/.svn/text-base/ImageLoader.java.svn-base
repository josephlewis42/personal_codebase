package Game;

import java.awt.Graphics;
import java.awt.Image;
import java.awt.Toolkit;
import java.awt.geom.AffineTransform;
import java.awt.image.AffineTransformOp;
import java.awt.image.BufferedImage;
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
		if(mapper.containsKey(imgLocation))
			return mapper.get(imgLocation);
		
		URL imageURL = Factory.class.getResource(imgLocation);

		if (imageURL != null) 
		{	
				Image j = new ImageIcon(imageURL).getImage();
				mapper.put(imgLocation, j);
				
				return j;
		}
		
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
		Image o = null;
		
		switch(i)
		{
		case ANT_FIGHT:	o = getImage("/images/sprites/ant_fight.png");	break;
		case GRASS:		o = getImage("/images/tiles/grass.jpg");	break; 
		case HOLE:		o = getImage("/images/tiles/hole.jpg");		break; 
		case LARGEEGG:	o = getImage("/images/sprites/egg_lg.png"); break;
		case MEDEGG:	o = getImage("/images/sprites/egg_me.png"); break;
		case SMALLEGG:	o = getImage("/images/sprites/egg_sm.png");	break; 	
		case SURFACE_TILE:	o = getImage("/images/tiles/dirt.jpg");	break; 
		case SURFACE_ONE_FOOD: o = getImage("/images/tiles/dirt_1.jpg");	break; 
		case SURFACE_TWO_FOOD: o = getImage("/images/tiles/dirt_2.jpg");	break; 
		case SURFACE_THREE_FOOD: o = getImage("/images/tiles/dirt_3.jpg");	break; 
		case SURFACE_FOUR_FOOD: o = getImage("/images/tiles/dirt_4.jpg");	break;
		case SURFACE_FIVE_FOOD: o = getImage("/images/tiles/dirt_5.jpg");	break; 
		case UNDUG: o = getImage("/images/tiles/dark_dirt.jpg");	break; 
		case YELLOWSOLDIER: o = getImage("/images/sprites/yellow_soldier.png");	break; 
		}
		
		return o;
	}
	
	/**
	 * Rotates the given image to the requested proper position, returns a copy.
	 * 
	 * @param toRotate
	 * @param direction
	 * @return
	 */
	public static Image getRotatedImage(Image toRotate, Direction direction)
	{
		
		//Check if it is in the mapper already.
		String representation = toRotate.toString() + direction.toString();
		if(mapper.containsKey(representation))
			return mapper.get(representation);
		
		
		double amount_to_rotate = 0;
		BufferedImage bi = new BufferedImage(Tile.WIDTH, Tile.HEIGHT, BufferedImage.TYPE_INT_ARGB_PRE);
		
		
		Graphics g = bi.createGraphics();

	    // Paint the image onto the buffered image
	    g.drawImage(toRotate, 0, 0, null);
	    g.dispose();
		
		
		switch(direction)
		{
		case NORTHEAST: amount_to_rotate = Math.PI/4; break;
		case EAST: 		amount_to_rotate = Math.PI/2; break;
		case SOUTHEAST: amount_to_rotate = 3*Math.PI/4; break;
		case SOUTH:		amount_to_rotate = Math.PI; break;
		case SOUTHWEST: amount_to_rotate = 5*Math.PI/4; break;
		case WEST: 		amount_to_rotate = 3*Math.PI/2; break;
		case NORTHWEST: amount_to_rotate = 7*Math.PI/4; break;
		}
		
		
		// http://www.exampledepot.com/egs/java.awt.image/CreateTxImage.html
		AffineTransform tx = new AffineTransform();
		tx.rotate(amount_to_rotate, bi.getWidth()/2, bi.getHeight()/2);
		
		AffineTransformOp op = new AffineTransformOp(tx, AffineTransformOp.TYPE_BILINEAR);
		bi = op.filter(bi, null);
		
		Image output = Toolkit.getDefaultToolkit().createImage(bi.getSource());
		
		mapper.put(representation, output);
		
	    return output;
	}
}
