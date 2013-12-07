/**
	Copyright 2012 Joseph Lewis <joehms22@gmail.com>
**/

// includes
#include <xs1.h>
#include <stdlib.h>
#include <stdio.h>
#include <print.h>
#include "platform.h"

// defines
#define TICKS_PER_SEC XS1_TIMER_HZ
#define TICKS_PER_MS (XS1_TIMER_HZ/1000)
#define TICKS_PER_MICRO (XS1_TIMER_HZ/1000000)
#define TIMER_MAX_VALUE 0x7FFFFFFF

//constants
const int FRAME_WIDTH = 20 * TICKS_PER_MS;


// Ports
// Left = XS1_PORT_1E | Right = XS1_PORT_1F
port out left = XS1_PORT_1E;
port out right = XS1_PORT_1F;


unsigned int l_command;
unsigned int r_command;


void left_forward(int pct)
{
	if(pct > 100 || pct < 0)
		return;

	l_command = 1500 + (5 * pct);
}

void left_reverse(int pct)
{
	if(pct > 100 || pct < 0)
			return;

	l_command = 1500 - (5 * pct);
}

void right_forward(int pct)
{
	if(pct > 100 || pct < 0)
			return;

	r_command = 1500 - (5 * pct);
}

void right_reverse(int pct)
{
	if(pct > 100 || pct < 0)
			return;

	r_command = 1500 + (5 * pct);
}

void right_stop()
{
	r_command = 1490;
}

void left_stop()
{
	l_command = 1500;
}





void servo_task(unsigned int timeout_ticks)
{
	timer tmr;
	unsigned int frame, end_time, t;

	tmr :> frame;


	// Set up the end of the line for us.
	tmr :> end_time;
	end_time += timeout_ticks;

	while(1)
	{
		if(timeout_ticks != 0)
		{
			tmr :> t;
			if(t > end_time)
				return;
		}

		frame += FRAME_WIDTH;


		// Turn the servos pulses on
		left <: 1;
		right <: 1;


		// Turn them off one by one
		tmr :> t;

		/**
		printchar('L');
		printuintln(l_command);
		printchar('R');
		printuintln(r_command);
		**/

		if(l_command < r_command)
		{
			tmr when timerafter(t + l_command * TICKS_PER_MICRO) :> void;
			left <: 0;

			tmr when timerafter(t + r_command * TICKS_PER_MICRO) :> void;
			right <: 0;
		}
		else
		{
			tmr when timerafter(t + r_command * TICKS_PER_MICRO) :> void;
			right <: 0;

			tmr when timerafter(t + l_command * TICKS_PER_MICRO) :> void;
			left <: 0;
		}


		tmr when timerafter(t + FRAME_WIDTH) :> void;
	}


	left <: 0;
	right <: 0;
}
