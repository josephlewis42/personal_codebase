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

// ports
out port toLeftServo = XS1_PORT_1E;
out port toRightServo = XS1_PORT_1F;

// prototypes
void servo_task_static (out port oServo , unsigned int pulse_width_us);
void driver_task (chanend out_servo_cmd_chan , int pulse_increment, unsigned int delay_ticks);
void servo_task (out port oServo, chanend in_servo_cmd_chan);

typedef struct {
	unsigned int pulse_width_us;
} servo_cmd_t;


/**
int main ()
{
	par
	{
		//servo_task_static(toRightServo, 2000);
		servo_task_static(toLeftServo, 1250); // gt med is forward, lt is back
	}

	return 0;
}
**/

int main()
{
	chan servo_cmd_chan;

	par {
		servo_task(toLeftServo, servo_cmd_chan);
		driver_task(servo_cmd_chan, 50, 750*TICKS_PER_MS);
	}

	return 0;
}

/**
The first parameter is the output port that corresponds to one of the servos.
The second parameter is the pulse width of the servo signal in microseconds. Valid
values for this are between 1000 − 2000 inclusive.
This task will repeatedly send the specified pulse to the servo. On continuous rotation
servos, this affects both the speed and direction of rotation.
This task will have an infinite while loop, and will repeatedly send the servo frames
with the timing that corresponds to the pulse width.
 */
void servo_task_static (out port oServo , unsigned int pulse_width_us)
{
	timer tmr;
	unsigned int width, frame;
	tmr :> frame;

	while(1)
	{
		width = frame + (pulse_width_us * TICKS_PER_MICRO);
		frame += 20 * TICKS_PER_MS;

		// make servo high to start timing the servo.
		oServo <: 1;

		// When width of pulse reached, send to low.
		tmr when timerafter(width) :> void;
		oServo <: 0;

		// Wait for timeout on frame.
		tmr when timerafter(frame) :> void;
	}
}


/**

This task will cycle back and forth (infinitely) between the minimum and maximum
servo pulse values incrementing (or decrementing when it is heading down) the amount
specified by the pulse increment parameter each time.

The channel is going to be connected to a servo task, you will send microsecond
values along it (as unsigned ints).
It will send the command along the channel, and then pause delay ticks ticks at
each level.

*/
void driver_task (chanend out_servo_cmd_chan, int pulse_increment, unsigned int delay_ticks)
{
	timer tmr;
	unsigned int curr_time;
	unsigned int min_value = 1000;
	unsigned int max_value = 2000;
	unsigned int curr_value =  1500; // start from a stop to be nice to the servo.
	int going_up = 1;
	servo_cmd_t m_command;

	while(1)
	{
		m_command.pulse_width_us = curr_value;
		out_servo_cmd_chan <: m_command;


		// Incrment or decrement between the min and max values.
		if(going_up)
			curr_value += pulse_increment;
		else
			curr_value -= pulse_increment;

		if(curr_value < min_value)
		{
			curr_value = min_value;
			going_up = 1;
		}

		if(curr_value > max_value)
		{
			curr_value = max_value;
			going_up = 0;
		}

		// Delay after sending command.
		tmr :> curr_time;
		tmr when timerafter(curr_time + delay_ticks) :> void;
	}
}



/**

The first parameter is an output port connected to one of the servos.
The second parameter is the channel that is connected to the driver task.
Use your original “static” servo code as a model for this (i.e., copy that code into here
initially).

The task should start off driving the servo with a “neutral” signal (1500 microsec-onds).
It should take care to honor the timing of the servo frame as its highest priority.
During the “downtime” of the servo protocol, it should monitor the channel in such a
way that it can receive zero, one, or multiple commands during the waiting stage. If it
receives multiple commands, it will just keep the last one.

 */

void servo_task(out port oServo, chanend cmds)
{
	timer tmr;
	unsigned int width, frame;
	int finished;
	servo_cmd_t m_command;

	tmr :> frame;

	m_command.pulse_width_us = 1500;

	while(1)
	{
		width = frame + (m_command.pulse_width_us * TICKS_PER_MICRO);
		frame += 20 * TICKS_PER_MS;

		oServo <: 1; // make servo high
		finished = 0;

		tmr when timerafter(width) :> void;
		oServo <: 0;

		while(! finished)
		{
			select
			{
				case tmr when timerafter(frame) :> void:
					finished = 1;
					break;

				// Commands are lowest priority
				case cmds :> m_command:
					break;
			}
		}
	}
}
