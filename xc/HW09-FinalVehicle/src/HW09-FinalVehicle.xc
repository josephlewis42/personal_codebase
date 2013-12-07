/*
 * FinalVehicle.xc
 *
 * The final vehicle driving mechanism.
 *
 *  Created on: May 17, 2012
 *      Author: Joseph Lewis <joehms22@gmail.com>
 */

//#define TESTING

#include <stdlib.h>
#include <assert.h>
#include <print.h>
#include <stdio.h>
#include "common_cmds.h"
#include "i2c.h"
#include "uart.h"


#include "lights.h"
#include "buttons.h"
#include "director.h"
#include "bfs.h"
#include "americus.h"
#include "servo.h"

// definitions
//#define TESTING // Define to start the tests and do them rather than the main loop


// declarations
const static int nServos = 2;
const static int servo_offsets[] = {0,-16}; // servo offsets


out port oServos[] = {XS1_PORT_1F, XS1_PORT_1E};

i2c_p i2c = {
	XS1_PORT_1A, 	// s c l
	XS1_PORT_1B, 	// sda
	0, 				// t
	0,				// tmr
	10000			// delay
};


// prototypes
void run_tests(chanend lightschan, chanend directions, chanend out_servo_cmd_chan);
void main_controller(chanend lightschan, chanend directions, chanend out_servo_cmd_chan);

// functions


int main()
{
	const int obstacles [ELEMENT_COUNT] = {
			0,0,1,0,1,0,
			0,0,1,0,0,1,
			0,1,1,1,0,1,
			0,1,0,0,0,1,
			0,1,0,1,1,0,
			0,1,0,1,0,0
	};

	int start_rank = RANK(5 , 2);
	int goal_rank = RANK(0 , 3);

	chan lightschan;
	chan out_servo_cmd_chan;
	chan directions;

	par
	{
		lights_thread(lightschan);
		directions_thread(directions, start_rank, goal_rank, obstacles);
		servo_task_multi(nServos, oServos, servo_offsets, out_servo_cmd_chan);

#ifdef TESTING
		run_tests(lightschan, directions,out_servo_cmd_chan);
#else
		main_controller(lightschan, directions,out_servo_cmd_chan);
#endif
	}
}


#ifdef TESTING
void run_tests(chanend lightschan, chanend directions, chanend out_servo_cmd_chan)
{
	test_navigation(lightschan, directions, out_servo_cmd_chan, i2c);


	// known good
	lights_test(lightschan);
	test_buttons();
	test_bfs();
	director_test(directions);

}
#else
void main_controller(chanend lightschan, chanend directions, chanend out_servo_cmd_chan)
{
	// Init
	i2c_init( i2c );

	// Blink LEDs at 1 Hz
	lightschan <: 1;

	// Wait for button press
	wait_either_button_press();
	wait_all_button_release();

	// Turn all LEDs on
	lightschan <: -1;

	// Search the maze for a solution
		// Done in another thread on demand
	// Set LEDs to 2 Hz
	lightschan <: 2;

	// Navigate the maze
	navigate_maze(lightschan, directions, out_servo_cmd_chan, i2c);

	debug("finished navigation\n");
	lightschan <: -1;
	// Finish.
}

#endif
