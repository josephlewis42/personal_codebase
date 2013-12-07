/**
 *
 * Copyright 2012-05-10 Joseph Lewis <joehms22@gmail.com>
 *
 * BSD LICENSE
 *
 */
// includes
#include <xs1.h>
#include <stdlib.h>
#include <stdio.h>
#include <print.h>
#include "platform.h"
#include "math.h"

#include "servo.h"
#include "hmc6352.h"
#include "uart.h"

// defines
#define TICKS_PER_SEC XS1_TIMER_HZ
#define TICKS_PER_MS (XS1_TIMER_HZ/1000)
#define TICKS_PER_US (XS1_TIMER_HZ/1000000)
#define TIMER_MAX_VALUE 0x7FFFFFFF
#define DEBUG

#define RIGHT_SERVO_INDEX 0
#define LEFT_SERVO_INDEX 1
#define ROTATE_HZ 5
#define HEADING_TOLEARANCE 2


// ports
// ports Left 1E Right 1F
out port oServos[] = {XS1_PORT_1F, XS1_PORT_1E};
in port leftButton = PORT_BUT_1;
in port rightButton = PORT_BUT_2;

// prototypes
void turn90_task(in port iLeftButton,
		in port iRightButton,
		chanend out_servo_cmd_chan);


// variables
const static int offsets[] = {0,-16}; // servo offsets

i2c_p i2c = {
	XS1_PORT_1A, 	// s c l
	XS1_PORT_1B, 	// sda
	0, 				// t
	0,				// tmr
	10000			// delay
};


int main(void)
{
	chan cmd_chan;

	par
	{
		servo_task_multi(2, oServos, offsets, cmd_chan);
		turn90_task(leftButton, rightButton, cmd_chan);
	}

	return 0;
}


/**
 * Turns the closest way to get to the heading.
 */

#define LEFT 0
#define RIGHT 1
void turn_to_heading(chanend out_servo_cmd_chan, int wanted_heading)
{
	timer t;
	unsigned int time;
	servo_cmd_t current_command = default_servo_cmd();

	int curr_heading;
	char words[64];
	int headingdiffr, headingdiffl;


	while(wanted_heading < 0)
		wanted_heading += 360;

	wanted_heading %= 360;

	// wait 1 sec before turn
	t :> time;
	t when timerafter(time + TICKS_PER_SEC) :> void;

	do
	{
		curr_heading = hmc6352_get_heading_degrees(i2c);

		headingdiffl = ((wanted_heading - curr_heading) + 360 ) % 360;
		headingdiffr = ((curr_heading - wanted_heading) + 360 ) % 360;

		sprintf(words, "%3i\r\n", curr_heading);
		debug(words, 6);
#ifdef DEBUG
		sprintf(words, "%3i lheadr %3i\r\n", headingdiffl, headingdiffr);
		debug(words,17);
#endif

		if(headingdiffr < headingdiffl)
		{
#ifdef DEBUG
//			sprintf(words, "%3i wanted %3i\r\n", curr_heading, wanted_heading);
//			debug(words,17);
#endif
			// Turn right
			current_command.pulse_width_us[RIGHT_SERVO_INDEX] = 1500 - (headingdiffr);
			current_command.pulse_width_us[LEFT_SERVO_INDEX] = 1500 - (headingdiffr);
		}
		else
		{
#ifdef DEBUG
			sprintf(words, "%3i wanted %3i\r\n", curr_heading, wanted_heading);
			debug(words,17);
#endif
			// Turn left
			current_command.pulse_width_us[RIGHT_SERVO_INDEX] = 1500 + (headingdiffl);
			current_command.pulse_width_us[LEFT_SERVO_INDEX] = 1500 + (headingdiffl);
		}

		out_servo_cmd_chan <: current_command;

		// wait .2 sec before turn
		t :> time;
		t when timerafter(time + (TICKS_PER_SEC / ROTATE_HZ) ) :> void;

	} while(!( curr_heading < wanted_heading + HEADING_TOLEARANCE && curr_heading > wanted_heading - HEADING_TOLEARANCE));//(curr_heading > wanted_heading - 10) && (curr_heading < wanted_heading + 10) );

	// set back to neutral.
	out_servo_cmd_chan <: default_servo_cmd();

#ifdef DEBUG
	sprintf(words, "done\r\n");
	debug(words,7);
#endif
}


void turn90_task(in port iLeftButton,
		in port iRightButton,
		chanend out_servo_cmd_chan)
{
	int wanted_degrees = hmc6352_get_heading_degrees(i2c) + 90;

	select
	{
		case iLeftButton when pinseq(0) :> void:
			turn_to_heading(out_servo_cmd_chan, hmc6352_get_heading_degrees(i2c) - 90);
			break;

		case iRightButton when pinseq(0) :> void:
			turn_to_heading(out_servo_cmd_chan, hmc6352_get_heading_degrees(i2c) + 90);
			break;
	}
}
