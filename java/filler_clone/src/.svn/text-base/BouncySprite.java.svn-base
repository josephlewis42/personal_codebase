/**
 * The sprite class provides a way to hold sprites.
 * @author Joseph Lewis <joehms22@gmail.com>
 * @author Chris Meyer  <angelic33@gmail.com>
 *
 */

import java.awt.Color;
import java.lang.Math;
import java.util.ArrayList;

public class BouncySprite 
{

	double location_x;
	double location_y;
	Vector v = new Vector(true);  //Create a random vector.
	
	double radius = 0.05;
	int id_number = 0;
	BouncySprite last_sprite_hit = null;  //Null if the last turn didn't hit a sprite.
	
	Color rgb = StdDraw.BLACK; //Default color for balls is black.
	private static final double PI = 3.14159;

	/**
	 * Constructs a sprite in a location that no other sprite is at.
	 * If this is impossible there will be an infinite loop, so be
	 * careful.
	 * 
	 * @param spritearray
	 * @param idnumber  - A UUID for the sprite.
	 */
	public BouncySprite(ArrayList<BouncySprite> spritearray, int idnumber)
	{
		//Id numbers are used for determining which sprite moves
		//the other one in collisions.
		id_number = idnumber;
		
		do //Keep calculating as long as sprite is on top of another.
		{			
			/*
			 * Limit the size of the area for the ball to be generated in to be 2*radius
			 * smaller than the entire screen, then shift the entire location to the right
			 * by radius.  This keeps the balls from being generated off screen.
			 */
			location_x = Math.random()*(2-radius*2) -1 + radius; //Allow balls to be generated in
			location_y = Math.random()*(2-radius*2) -1 + radius; //Coordinates II, III, IV
        
		}
		while( hit_test(spritearray) );
	}
	
	/**
	 * Constructor for Sprite.
	 * 
	 * @param spritearray The array of sprites to be tested for hits.
	 * @param idnumber A uuid for this sprite.
	 * @param c The color of the sprite to be drawn.
	 */
	public BouncySprite (ArrayList<BouncySprite> spritearray, int idnumber, Color c)
	{
		this(spritearray, idnumber);
		
		rgb = c;
	}
	
	public double get_location_x()
	{
		return location_x;
	}	
	public double get_location_y()
	{
		return location_y;
	}
	public int get_id()
	{
		return id_number;
	}	
	public double get_radius()
	{
		return radius;
	}
	public double get_size()
	{
		return PI * (radius * radius); //PI r squared
	}
	
	/**
	 * Checks if a certain sprite is allowed to hit this one, 
	 * returns false if the sprites are still touching from
	 * a prior engagement. 
	 */
	public boolean can_hit(BouncySprite sprite)
	{
		//Check if this sprite is not still touching the last sprite.
		System.out.println(id_number+" can Hit: "+sprite.id_number+" = "+(sprite != last_sprite_hit));
		return sprite != last_sprite_hit;
	}
	
	/**
	 * Resets the sprite for the can_hit test.
	 * @param uuid
	 */
	public void reset_hit(BouncySprite sprite)
	{
		last_sprite_hit = sprite;
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
		System.out.println("Updating Sprite: "+id_number);
		//Check if this sprite is not still touching the last sprite.
		if( last_sprite_hit != null )
		{
			if( ! individual_hit_test(last_sprite_hit) )
				last_sprite_hit = null;
		}
		
		// Bounce off other sprites, but do the calculation quickly so 
		// lag is kept to a minimal.
        fast_hit_test(spritelist);
        
		//Update the sprite's location
		update_sprite();
		
		// Draw sprite on the screen
        StdDraw.setPenColor( rgb );
        StdDraw.filledCircle(location_x, location_y, radius);
	}
	
	/**
	 * Updates the sprite's position.
	 */
	private void update_sprite()
	{
		// Bounce off wall according to law of elastic collision
        if (Math.abs(location_y + v.get_velocity_y()) > 1.0 - radius) 
        	v.reverse_velocity_y();
        
        if (Math.abs(location_x + v.get_velocity_x()) > 1.0 - radius) 
        	v.reverse_velocity_x();
        
        // Update the locations.
		location_x = v.get_new_position_x(location_x);
		location_y = v.get_new_position_y(location_y);
	}
	
	/**
	 * Parses an ArrayList of sprites and tests if any are touching this
	 * particular sprite.  Only do the hit test on balls with a higher
	 * uuid, this avoids a ball doing a test on itself, and multiple hit 
	 * registers when every ball gets the entire arraylist.
	 * 
	 * If a ball is touching modify it's directions.
	 * 
	 * @param spritearray
	 * @return bool, if are touching or not.
	 */
	protected boolean fast_hit_test( ArrayList<BouncySprite> spritearray)
	{
		
		boolean is_hitting = false;
		
		for( BouncySprite s : spritearray )
		{ 
			
			if( s.get_id() > id_number )
			{
				if( individual_hit_test(s) )
				{
					modify_direction(s);
					is_hitting = true;
				}
			}
		}
		return is_hitting; //Only if there are no hits with objects of a greater id.
	}
	
	/**
	 * Parses an ArrayList of sprites and tests if any are touching this
	 * particular sprite.  If so modify the directions of both sprites accordingly.
	 * 
	 * @param spritearray
	 * @return bool If touching anything
	 */
	protected boolean hit_test( ArrayList<BouncySprite> spritearray)
	{
		boolean is_hitting = false;
		
		for( BouncySprite s : spritearray )
		{
			if( individual_hit_test(s) )
			{
				modify_direction(s);
				is_hitting = true;
			}
		}
		return is_hitting; //Only if there are no hits with objects of a greater id.
	}
	
	/**
	 * Modify the direction of this and the other sprite, it is this sprite's duty.
	 * If and only if this sprite is allowed to.
	 * 
	 * @param s The sprite that this one is touching.
	 */
	protected void modify_direction(BouncySprite s)
	{
		if( s.can_hit(this) )
		{
			//Keep sprites from getting stuck together.
			s.reset_hit(this);
			
			//Normalize this vector.
			v.normalize();  //A

			//The point of collision vector.
			double poc_x = location_x + v.get_velocity_x() * radius;
			double poc_y = location_y + v.get_velocity_y() * radius;
			Vector poc = new Vector(poc_x, poc_y);
			
			//This vector is the one pointing out from the static circle.
			poc.subtract( new Vector(s.location_x, s.location_y) ); //B
			poc.normalize();

			poc.multiply( v.dot_product(poc) ); //D
			
			v.subtract(poc); //E
			poc.multiply(-1);
			v.multiply (.1); //modifies E
			v.add(poc);
			v.normalize();
			
			v.multiply(0.03);
			
			s.modify_direction(this);
			
			/**
			//Find new x values.
			double total_energy 	= Math.abs( velocity_x ) + 
										Math.abs( s.get_velocity_x() );
			double actual_energy	= velocity_x + s.get_velocity_x();
			
			//Find the percents of energy each ball has.
			double percent_total_this  	= Math.abs(velocity_x) / total_energy;
			double percent_total_other 	= Math.abs(s.get_velocity_x()) / total_energy;
			
			//Distribute the total x energy proportionately between the balls.
			s.set_velocity_x( percent_total_this * actual_energy );
			set_velocity_x( percent_total_other * actual_energy );
			
			//Find new y values.
			total_energy 	= Math.abs( velocity_y ) + Math.abs( s.get_velocity_y() );
			actual_energy 	= velocity_y + s.get_velocity_y();
			
			percent_total_this  = Math.abs(velocity_y) / total_energy;
			percent_total_other = Math.abs(s.get_velocity_y()) / total_energy;
			
			s.set_velocity_y(percent_total_this * actual_energy);
			set_velocity_y(percent_total_other * actual_energy);
			
			//Alert the user of a hit.
			System.out.println("\n <-- Hit -->");
			System.out.println("Actual Energy: "+actual_energy);
			System.out.println("This Energy: "+velocity_y);
			System.out.println("Other Energy: "+s.get_velocity_y());
			**/
		}
	}
	
	/**
	 * Returns True if this sprite is touching another,
	 * returns False otherwise.
	 * 
	 * This uses the Pythagorean theorem to judge the distance
	 * between the two circles, side a is the difference of 
	 * x positions, b is difference in y's.  If the hypotenuse is of a smaller
	 * size than the two radiuses added together then the Sprites are touching.
	 */
	protected boolean individual_hit_test( BouncySprite s )
	{		
		double a = location_x - s.get_location_x();
		double b = location_y - s.get_location_y();
		
		double a_squared = a * a;
		double b_squared = b * b;
		
		double max_hypotenuse = radius + s.get_radius();
		
		//Return True if circles are touching.
		return Math.sqrt(a_squared + b_squared) < max_hypotenuse;
	}
}