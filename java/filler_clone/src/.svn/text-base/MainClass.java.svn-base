/**
 * Physics simulation of bouncing balls against each other and
 * static white circles.
 *
 * Copyright (c) 2010 Joseph Lewis <joehms22@gmail.com> 
 * Copyright (c) 2010 Chris Meyer  <angelic33@gmail.com>
 * GNU GPL V 2.0
 **/

import java.util.ArrayList;

public class MainClass
{ 
	// spritearray holds all of the sprites that can be drawn.
	static ArrayList<BouncySprite> spritearray = new ArrayList<BouncySprite>();
	 
	// Current uuid for generating sprites (used in collision detection)
    static int uuid = 0;
    
    static FillerSprite current_white = null;
    
    public static void reset_vars()
    {
    	spritearray = new ArrayList<BouncySprite>();
    	uuid = 0;
    	current_white = null;
    }
	
	public static void add_white_sprite() {
		current_white = new FillerSprite(spritearray, -uuid);
    	uuid++;
	}
	
	public static void stop_drawing_white() {
		current_white.is_being_drawn = false;
		spritearray.add(current_white);
		
		delete_white_sprite(); //Clean up and get ready for next one.
	}
	
	public static void delete_white_sprite() {
		current_white = null;
	}
		
	public static double get_percent_filled()
	{
		double pf = 0;
		
		for(BouncySprite s : spritearray)
			pf += s.get_size();
		
		pf = (pf/4.0) * 100; //The size of the grid is 4
		
		return pf;
	}
	
	public static int play_round(int lives)
	{
		// Clear the background
        StdDraw.setPenColor(StdDraw.GRAY);
        StdDraw.filledSquare(0, 0, 1.0);
        
        //Check for mouse press to create new 
        if(StdDraw.mousePressed())
        {
        	//if mouse pressed and no sprite being drawn
        	if(current_white == null)
        	{
        		add_white_sprite();
        		lives--; //You now have fewer lives
        	}
        	else
        	{
            	//If mouse pressed and current white is not being drawn, it must
        		//have been hit.  Explode!
            	if(current_white.is_being_drawn == false)
            	{
            		StdDraw.setPenColor(StdDraw.RED);
                    StdDraw.filledSquare(0, 0, 1.0);
                    
                    delete_white_sprite();
            	}
        	}
        }
        else
        {
        	//if mouse not pressed and sprite being drawn, just drop it.
        	if(current_white != null)
        		stop_drawing_white();
        }

        // Draw each actor individually, updating it as you go along.
        synchronized(spritearray)
        {
	        for(BouncySprite mysprite : spritearray)
	        {
        		mysprite.draw_sprite(spritearray);
	        }
	        
			if(current_white != null)
				current_white.draw_sprite(spritearray);
        }
        
        // Display stats for the user
        StdDraw.setPenColor(StdDraw.WHITE);
        StdDraw.textLeft(-1.0, 0.95, " Lives: "+lives+" Percent: "+get_percent_filled());
        
        // Display and pause for 20 ms.
        StdDraw.show(20);
        
        return lives;
	}
	
	public static boolean play_level(int level_number) {
	
		double percent_needed = 61 - level_number; //Need 60 first level
		int lives = 19 + level_number; //Start with 20
		double percent_filled = 0;
		
		reset_vars(); //Reset from last round
		
		//Generate sprites.
        for(int i = 0; i < level_number+2; i++) //3 to start with
        {
        	spritearray.add(new BouncySprite(spritearray, uuid));
        	uuid++;
        }
        
        //Tell the user what they need
        Dialogs.showInformationDialog("JavaFiller", "You have "+lives+" lives to get "+percent_needed+" %");
        
        //Keep drawing frames until round is over.
		while(percent_needed > percent_filled && lives > 0)
		{
			lives = play_round(lives);
			percent_filled = get_percent_filled();
		}
		
		//True if player completed level, false if they failed
		return lives > 0;
	}
	
    public static void main(String[] args) 
    {
    	// Set up standard draw.
        StdDraw.setXscale(-1.0, 1.0);
        StdDraw.setYscale(-1.0, 1.0);
        
        //Play rounds until game is over.
        int current_level = 0;
        boolean completed;
        do
        {
        	current_level++;
        	completed = play_level(current_level);
        }
        while(completed);
        Dialogs.showInformationDialog("JavaFiller", "You lost on level "+current_level);
        System.exit(0);
    }
}