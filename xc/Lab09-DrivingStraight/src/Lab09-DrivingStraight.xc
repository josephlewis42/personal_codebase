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
#define HEADING_CHECK_HZ 10


// ports
// ports Left 1E Right 1F
out port oServos[] = {XS1_PORT_1F, XS1_PORT_1E};
in port leftButton = PORT_BUT_1;
in port rightButton = PORT_BUT_2;

const static int nServos = 2;

// prototypes
void turn90_task(in port iLeftButton,
		in port iRightButton,
		chanend out_servo_cmd_chan);

void straight_ui_task(in port iButton, chanend out_servo_cmd_t);


// variables
const static int servo_offsets[] = {0,-16}; // servo offsets

i2c_p i2c = {
	XS1_PORT_1A, 	// s c l
	XS1_PORT_1B, 	// sda
	0, 				// t
	0,				// tmr
	10000			// delay
};


int main(void)
{
	chan servoChan;
	par{
		straight_ui_task(leftButton, servoChan);
		servo_task_multi(
				nServos,
				oServos,
				servo_offsets,
				servoChan);
	}
	return 0;
}




void straight_ui_task(in port iButton, chanend out_servo_cmd_t)
{
	unsigned int initial_heading, current_heading;
	timer tmr;
	unsigned int timer_tmp;
	unsigned int drive_time_ticks;
	unsigned int finished_flag = 0;
	unsigned int speed = 250;
	unsigned int headingdiffl, headingdiffr;
	unsigned int secs_to_run = 5;
	unsigned int iterations = 0;
	servo_cmd_t cmds;
	char debug_info[64];

	cmds.pulse_width_us[0] = MID_SERVO_PULSE_US;
	cmds.pulse_width_us[1] = MID_SERVO_PULSE_US;

	// initially the vehicle is stopped waiting for a button press
	out_servo_cmd_t <: cmds;
	iButton when pinseq(0) :> void;
	iButton when pinseq(1) :> void;

	// when the button is pressed the vehicle should sample the compass
	// to get the current heading then sleep for a second
	initial_heading = hmc6352_get_heading_degrees(i2c);

	tmr :> timer_tmp;
	tmr when timerafter(timer_tmp + TICKS_PER_SEC) :> void;


	tmr :> drive_time_ticks;


	while(iterations < secs_to_run * HEADING_CHECK_HZ)
	{
		iterations++;

		tmr :> timer_tmp;
		tmr when timerafter(timer_tmp + (TICKS_PER_SEC / HEADING_CHECK_HZ)) :> void;

		// vehicle should drive for five seconds at med speed +/- 250
		// microseconds forom neutral

		// sample the compass while driving at 10 hz,adjust for deviation from initial
		// heading
		current_heading = hmc6352_get_heading_degrees(i2c);

		sprintf(debug_info, "curr: %u wanted: %u\r\n", current_heading, initial_heading);
		debug(debug_info);

		cmds.pulse_width_us[0] = MID_SERVO_PULSE_US - speed;
		cmds.pulse_width_us[1] = MID_SERVO_PULSE_US + speed;

		headingdiffl = ((initial_heading - current_heading) + 360 ) % 360;
		headingdiffr = ((current_heading - initial_heading) + 360 ) % 360;

		#ifdef DEBUG
				sprintf(debug_info, "%3i lheadr %3i\r\n", headingdiffl, headingdiffr);
				debug(debug_info);
		#endif

				if(headingdiffr < headingdiffl)
				{
		#ifdef DEBUG
					sprintf(debug_info, "%3i wanted %3i\r\n", current_heading, initial_heading);
					debug(debug_info);
		#endif
					// Turn right
					cmds.pulse_width_us[RIGHT_SERVO_INDEX] -= 10 * (headingdiffr);
					cmds.pulse_width_us[LEFT_SERVO_INDEX] -= 10 * (headingdiffr);
				}
				else
				{
		#ifdef DEBUG
					sprintf(debug_info, "%3i wanted %3i\r\n", current_heading, initial_heading);
					debug(debug_info);
		#endif
					// Turn left
					cmds.pulse_width_us[RIGHT_SERVO_INDEX] += 10 * (headingdiffl);
					cmds.pulse_width_us[LEFT_SERVO_INDEX] += 10 * (headingdiffl);
				}
		out_servo_cmd_t <: cmds;
	}

	cmds.pulse_width_us[0] = MID_SERVO_PULSE_US;
	cmds.pulse_width_us[1] = MID_SERVO_PULSE_US;
	out_servo_cmd_t <: cmds;

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
		debug(words);
#ifdef DEBUG
		sprintf(words, "%3i lheadr %3i\r\n", headingdiffl, headingdiffr);
		debug(words);
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
			debug(words);
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
	debug(words);
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
