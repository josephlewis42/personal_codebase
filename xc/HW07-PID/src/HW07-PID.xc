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

#define RIGHT_SERVO_INDEX 0
#define LEFT_SERVO_INDEX 1
#define ROTATE_HZ 10
#define NUM_SAME_HEADINGS_UNTIL_DONE 8
#define HEADING_TOLERANCE_TENTHS_DEGREE 10

#define DEBUG

#define LEFT 0
#define RIGHT 1


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

	// Boost the number of signals to take by the hmc6352
	// and averaged so we don't get so much variance
	hmc6352_write_eeprom(i2c, NUM_SUMMED_MEASUREMENTS, 0x04); // Can go up to 16

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
void turn_to_heading(chanend out_servo_cmd_chan, int wanted_heading)
{
	timer t;
	unsigned int time;
	servo_cmd_t current_command = default_servo_cmd();
	int curr_heading = hmc6352_get_heading_tenth_degrees(i2c);
	int num_same = 0; // The number of headings that are the same
	char words[64];
	int headingdiffr, headingdiffl;
	int last_heading = curr_heading;
	int differential;
	int tmp;

	// Normalize the wanted heading
	while(wanted_heading < 0)
		wanted_heading += 3600;
	wanted_heading %= 3600;

	sprintf(words, "%i\r\n", wanted_heading);
	debug(words);

	// wait 1 sec before turn
	t :> time;
	t when timerafter(time + TICKS_PER_SEC) :> void;

	do
	{
		// Check the current heading
		last_heading = curr_heading;
		curr_heading = hmc6352_get_heading_tenth_degrees(i2c);

		differential = (last_heading - curr_heading) / ROTATE_HZ;

#ifdef DEBUG
		sprintf(words, "curr: %i wanted: %i num:%1i\r\n", curr_heading, wanted_heading, num_same);
		debug(words);
#endif


		// If it is the same as the last one, within a tolerance.
		if(curr_heading + HEADING_TOLERANCE_TENTHS_DEGREE >= wanted_heading &&
		   curr_heading - HEADING_TOLERANCE_TENTHS_DEGREE <= wanted_heading)
			num_same += 1;
		else
			num_same = 0;


		headingdiffl = ((wanted_heading - curr_heading) + 3600 ) % 3600;
		headingdiffr = ((curr_heading - wanted_heading) + 3600 ) % 3600;


#ifdef DEBUG
		sprintf(words, "right: %i left: %i diff: %i\r\n", headingdiffr, headingdiffl, differential);
		debug(words);
#endif

		if(headingdiffr < headingdiffl)
		{
			// Turn right
			tmp = 1500 - (3 * (headingdiffr / 10)) + (3 * differential);
			current_command.pulse_width_us[RIGHT_SERVO_INDEX] = tmp;
			current_command.pulse_width_us[LEFT_SERVO_INDEX] = tmp;
		}
		else
		{
			// Turn left
			tmp = 1500 + (3 * (headingdiffr / 10)) + (3 * differential);
			current_command.pulse_width_us[RIGHT_SERVO_INDEX] = tmp;
			current_command.pulse_width_us[LEFT_SERVO_INDEX] = tmp;
		}

		out_servo_cmd_chan <: current_command;

		// wait .2 sec before turn
		t :> time;
		t when timerafter(time + (TICKS_PER_SEC / ROTATE_HZ) ) :> void;

	} while(num_same < NUM_SAME_HEADINGS_UNTIL_DONE);

	// set back to neutral.
	out_servo_cmd_chan <: default_servo_cmd();
}


void turn90_task(in port iLeftButton, in port iRightButton, chanend out_servo_cmd_chan)
{
	while(1)
	{
		select
		{
			case iLeftButton when pinseq(0) :> void:
				iLeftButton when pinseq(1) :> void;
				turn_to_heading(out_servo_cmd_chan, hmc6352_get_heading_tenth_degrees(i2c) - 900);
				break;

			case iRightButton when pinseq(0) :> void:
				iRightButton when pinseq(1) :> void;
				turn_to_heading(out_servo_cmd_chan, hmc6352_get_heading_tenth_degrees(i2c) + 900);
				break;
		}
	}
}
