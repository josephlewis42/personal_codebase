/**
 * The sprite class provides a way to hold sprites.
 * @author Joseph Lewis <joehms22@gmail.com>
 *
 */

import java.util.ArrayList;

public class FillerSprite extends BouncySprite
{
	boolean is_being_drawn = true; //Set to false on first hit.
	int  gravity = 1;
	private static final double GROWTH_RATE = 0.01;
	private static final double INIT_RADIUS = 0.01; //The initial radius for the whitesprite
	
	/**
	 * Constructs a sprite in a location that no other sprite is at.
	 * If this is impossible there will be an infinite loop, so be
	 * careful.
	 * 
	 * @param spritearray
	 * @param idnumber  - A UUID for the sprite.
	 */
	public FillerSprite(ArrayList<BouncySprite> spritearray, int idnumber)
	{
		super(spritearray, idnumber);
		
		do //Keep calculating as long as sprite is on top of another.
		{
			//radius = Math.random()*0.5 + 0.1;
			radius = INIT_RADIUS;
			/*
			 * Limit the size of the area for the ball to be generated in to be 2*radius
			 * smaller than the entire screen, then shift the entire location to the right
			 * by radius.  This keeps the balls from being generated off screen.
			 */
			location_x = StdDraw.mouseX(); //Math.random()*(2-radius*2) -1 + radius; //Allow balls to be generated in
			location_y = StdDraw.mouseY(); //Math.random()*(2-radius*2) -1 + radius; //Coordinates II, III, IV
		}
		while( hit_test(spritearray) );
	}
	
	/**
	 * The function that updates and draws this sprite.  Uses the 
	 * spritelist to detect collisions and update those sprites
	 * as well.
	 * 
	 * @param spritelist
	 */
	public void draw_sprite(ArrayList<BouncySprite> spritelist)
	{
		System.out.println("Updating sprite: "+ id_number);
		last_sprite_hit = null;
		
		// Bounce off other sprites
        fast_hit_test(spritelist);
		
        //Gravity. it equals 0 when you hit another ball.
        if( ! is_being_drawn && location_y - radius > -1.0 && gravity > 0)
        {
        	location_y += gravity * -.0032;
        	gravity++;
        }
        
        if( is_being_drawn )
        {
        	//Grow a little
        	radius += GROWTH_RATE;
        	
        	//If the ball has hit the sides in growth, begin moving the ball center.
        	//like in the real filler game.
            if( location_y - radius < -1.0 ) location_y += GROWTH_RATE; //Move Right
            if( location_y + radius > 1.0 )  location_y -= GROWTH_RATE; //Move Left
            if( location_x - radius < -1.0 ) location_x += GROWTH_RATE; //Move Up
            if( location_x + radius > 1.0 )  location_x -= GROWTH_RATE; //Move Down
        }
        
		// draw ball on the screen
        StdDraw.setPenColor(StdDraw.WHITE); 
        StdDraw.filledCircle(location_x, location_y, radius);
	}
	
	protected void modify_direction(BouncySprite s)
	{
		//If the sprite is hit while being drawn, this sprite needs to stop growing.
		if( is_being_drawn )
		{
			is_being_drawn = false;
		}
		
		if( s instanceof FillerSprite)
		{
			gravity = 0;
		}
		
		if( s.can_hit(this) )
		{
			s.reset_hit(this);
			s.modify_direction(this);
		}
	}
}
