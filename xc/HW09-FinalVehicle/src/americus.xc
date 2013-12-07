/*
 * americus.xc - the navigator
 *
 *  Created on: May 29, 2012
 *      Author: Joseph Lewis <joehms22@gmail.com>
 */

// includes
#include <xs1.h>
#include <print.h>
#include "platform.h"
#include "math.h"
#include <stdio.h>

#include "servo.h"
#include "hmc6352.h"
#include "uart.h"
#include "director.h"
#include "americus.h"
#include "DistanceControlHelper.h"
#include "bumper.h"
#include "common_cmds.h"

#define SLOWDOWN_DIST_MM 50
#define DEGREES_TO_CORRECT 1

#define RIGHT_SERVO_INDEX 0
#define LEFT_SERVO_INDEX 1
#define HEADING_TOLEARANCE 5
#define TURN_HEADING_OFFSET 0
#define SLOWDOWN_SPEED_MID_OFFSET_MS 100
#define BACKUP_TIME_MS 250

#define CORRECT 0
#define RETURN 1
#define NOTHING 2

#define LEFT_FULL_SPEED 1900
#define LEFT_SLOW_SPEED 1100

static const int HEADING_CHECK_HZ = 20;
static const int MM_PER_UNIT = 178;


// prototypes
int straight_ui_task(chanend out_servo_cmd_t, unsigned int lpw, unsigned int rpw, unsigned int time_ms, int on_hit, i2c_p& i2c, const unsigned int initial_heading);
void turn_to_heading(chanend out_servo_cmd_chan, int wanted_heading, i2c_p& i2c);
void go_distance(chanend out_servo_cmd_chan, unsigned int distance_mm, i2c_p& i2c);


timer tmr;

void navigate_maze(chanend lightschan, chanend direction_input, chanend out_servo_cmd_chan, i2c_p& i2c)
{
	direction curr_dir;
	char output[64];

	// do complex tests
	do
	{
		direction_input :> curr_dir;
		switch(curr_dir.command)
		{
		case stop:
				debug("stopping");
				out_servo_cmd_chan <: default_servo_cmd();
				return;
			break;

		case forward:
				debug("going forward");
				go_distance(out_servo_cmd_chan, MM_PER_UNIT * curr_dir.param, i2c);
			break;

		case left_ninety:
				debug("left 90");
				turn_to_heading(out_servo_cmd_chan, hmc6352_get_heading_degrees(i2c) - 90, i2c);
			break;

		case right_ninety:
				debug("right 90");
				turn_to_heading(out_servo_cmd_chan, hmc6352_get_heading_degrees(i2c) + 90, i2c);
			break;
		}
	}while(curr_dir.command != stop);
}


void test_navigation(chanend lightschan, chanend directions, chanend out_servo_cmd_chan, i2c_p& i2c)
{
	servo_cmd_t m_command;
	timer t;

	m_command.pulse_width_us[LEFT_SERVO_INDEX] = 1900;
	m_command.pulse_width_us[RIGHT_SERVO_INDEX] = 1100;



	debug("Going forward, HIT BUMPER for correction!");
	straight_ui_task(out_servo_cmd_chan, 1900, 1100, 3000, CORRECT, i2c, hmc6352_get_heading_degrees(i2c));

	debug("Going forward, HIT BUMPER to die!\n");
	straight_ui_task(out_servo_cmd_chan, 1900, 1100, 3000, RETURN, i2c, hmc6352_get_heading_degrees(i2c));
	debug("Done bumper check\n");

	// test forward 1 unit
	debug("Going forward 1 unit\n");
	go_distance(out_servo_cmd_chan, MM_PER_UNIT * 1, i2c);


	// test forward 2 units
	debug("Going forward 2\n");
	go_distance(out_servo_cmd_chan, MM_PER_UNIT * 2, i2c);


	// test turn left
	debug("left 90\n");
	turn_to_heading(out_servo_cmd_chan, hmc6352_get_heading_degrees(i2c) - 90, i2c);

	// test turn right
	debug("right 90\n");
	turn_to_heading(out_servo_cmd_chan, hmc6352_get_heading_degrees(i2c) + 90, i2c);


	// test stopping
	debug("Stopping\n");
	out_servo_cmd_chan <: default_servo_cmd();
}






/**
 * Turns the closest way to get to the heading.
 */
void turn_to_heading(chanend out_servo_cmd_chan, int wanted_heading, i2c_p& i2c)
{
	unsigned int time;
	servo_cmd_t current_command = default_servo_cmd();
	int curr_heading;
	int headingdiffr, headingdiffl;


	wanted_heading = normalize_heading(wanted_heading);

	// wait 1 sec before turn
	wait_time(TICKS_PER_SEC, tmr);

	do
	{
		curr_heading = hmc6352_get_heading_degrees(i2c);

		headingdiffl = normalize_heading(wanted_heading - curr_heading);
		headingdiffr = normalize_heading(curr_heading - wanted_heading);

		if(headingdiffr < headingdiffl)
		{
			// Turn right
			current_command.pulse_width_us[RIGHT_SERVO_INDEX] = 1500 - (headingdiffr) - TURN_HEADING_OFFSET;
			current_command.pulse_width_us[LEFT_SERVO_INDEX] = 1500 - (headingdiffr) - TURN_HEADING_OFFSET;
		}
		else
		{
			// Turn left
			current_command.pulse_width_us[RIGHT_SERVO_INDEX] = 1500 + (headingdiffl) + TURN_HEADING_OFFSET;
			current_command.pulse_width_us[LEFT_SERVO_INDEX] = 1500 + (headingdiffl) + TURN_HEADING_OFFSET;
		}

		out_servo_cmd_chan <: current_command;

		// wait .2 sec before turn
		wait_time((TICKS_PER_SEC / HEADING_CHECK_HZ), tmr);

	} while(!( curr_heading < wanted_heading + HEADING_TOLEARANCE && curr_heading > wanted_heading - HEADING_TOLEARANCE));//(curr_heading > wanted_heading - 10) && (curr_heading < wanted_heading + 10) );

	// set back to neutral.
	out_servo_cmd_chan <: default_servo_cmd();
}




/**
 * Outputs directions to the out_servo_cmd_t, with the given default, for the given amount of time.
 * on_hit specifies what to do on a bumper hit, correct = 0; or return; returns a 1 if bumpers are hit
 */

int straight_ui_task(chanend out_servo_cmd_t, unsigned int lpw, unsigned int rpw, unsigned int time_ms, int on_hit, i2c_p& i2c, const unsigned int initial_heading)
{
	unsigned int current_heading, timer_tmp, start_time, headingdiffl, headingdiffr;
	servo_cmd_t cmds;


	debug("\tsetting up straight, getting heading.\n");
	//initial_heading = hmc6352_get_heading_degrees(i2c);
	debug("\t got heading.\n");
	tmr :> start_time;
	start_time += TICKS_PER_MS * time_ms;
	debug("\t got time.\n");



	while(1)
	{
		debug("1\n");
		select
		{
			case tmr when timerafter(start_time) :> void:
				out_servo_cmd_t <: default_servo_cmd();
				debug("\ttimeout\n");
				return 0;
			default:
				break;
		}
		debug("2\n");

		wait_time(TICKS_PER_SEC / HEADING_CHECK_HZ, tmr);

		debug("3\n");


		current_heading = hmc6352_get_heading_degrees(i2c);
		debug("4\n");

		cmds.pulse_width_us[LEFT_SERVO_INDEX] = lpw;
		cmds.pulse_width_us[RIGHT_SERVO_INDEX] = rpw;

		debug("5\n");

		headingdiffl = normalize_heading(initial_heading - current_heading);
		headingdiffr = normalize_heading(current_heading - initial_heading);
		debug("6\n");


		if(headingdiffr < headingdiffl)
		{
			// Turn right
			cmds.pulse_width_us[RIGHT_SERVO_INDEX] -= 10 * (headingdiffr);
			cmds.pulse_width_us[LEFT_SERVO_INDEX] -= 10 * (headingdiffr);
		}
		else
		{
			// Turn left
			cmds.pulse_width_us[RIGHT_SERVO_INDEX] += 10 * (headingdiffl);
			cmds.pulse_width_us[LEFT_SERVO_INDEX] += 10 * (headingdiffl);
		}

		debug("7\n");



		// check for bumper hits
		if(bumper_is_hit())
		{
			debug("8a\n");

			if(on_hit == RETURN)
			{
				debug("\tbumper hit, returning\n");
				out_servo_cmd_t <: default_servo_cmd();
				return 1;
			}

			if(on_hit == CORRECT)
			{
				// course correct by five degrees
				if(right_is_hit()) // we're going too far right, stop it!
				{
					debug("\tright hit, turning left\n");
					cmds.pulse_width_us[LEFT_SERVO_INDEX] = MID_SERVO_PULSE_US;
					//cmds.pulse_width_us[RIGHT_SERVO_INDEX] += 10 * TURN_HEADING_OFFSET;
				}
				if(left_is_hit()) // we're going too far left, stop it!
				{
					debug("\tleft hit, turning right\n");
					//cmds.pulse_width_us[LEFT_SERVO_INDEX] -= 10 * TURN_HEADING_OFFSET;
					cmds.pulse_width_us[RIGHT_SERVO_INDEX] = MID_SERVO_PULSE_US;
				}

			}
		}

		debug("8b\n");



		out_servo_cmd_t <: cmds;
	}

	// set back to neutral, control should never reach here...
	debug("\tError: control reached where it shouldn't\n");
	out_servo_cmd_t <: default_servo_cmd();

	return 0;
}

/**
 * Goes the amount of distance specified, forward, slows down until
 * obstacle hit, then stops and backs up.
 */
void go_distance(chanend out_servo_cmd_chan, unsigned int distance_mm, i2c_p& i2c)
{
	unsigned int curr_pulse_duration;
	timer tmr;

	// Go fast
	debug("Going forward\n");

	// Full Speed Ahead, using the compass to avoid obstacles
	curr_pulse_duration = (unsigned int) find_pulse_duration_ms(LEFT_FULL_SPEED, distance_mm - SLOWDOWN_DIST_MM);

	if(distance_mm - SLOWDOWN_DIST_MM  > 0)
		straight_ui_task(out_servo_cmd_chan, LEFT_FULL_SPEED, LEFT_SLOW_SPEED, curr_pulse_duration, CORRECT, i2c, hmc6352_get_heading_degrees(i2c));


	// Do slowdown
	debug("Slowing down\n");
	curr_pulse_duration = (unsigned int) find_pulse_duration_ms(MID_SERVO_PULSE_US + SLOWDOWN_SPEED_MID_OFFSET_MS,
																	SLOWDOWN_DIST_MM);

	while(1)
	{
		debug("trying to get bumper to hit.\n");
		if(straight_ui_task(out_servo_cmd_chan,
							MID_SERVO_PULSE_US + SLOWDOWN_SPEED_MID_OFFSET_MS,
							MID_SERVO_PULSE_US - SLOWDOWN_SPEED_MID_OFFSET_MS,
							//curr_pulse_duration,
							3000,
							RETURN, i2c,
							hmc6352_get_heading_degrees(i2c)) == 1)
			break;
	}
	debug("bumper finally hit, backing up.\n");

	// Back up 1/2 a sec.
	straight_ui_task(out_servo_cmd_chan,
					MID_SERVO_PULSE_US - SLOWDOWN_SPEED_MID_OFFSET_MS,
					MID_SERVO_PULSE_US + SLOWDOWN_SPEED_MID_OFFSET_MS,
					BACKUP_TIME_MS,
					NOTHING, i2c,
					hmc6352_get_heading_degrees(i2c));
}
