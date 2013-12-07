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
//#define DEBUG
#define NUM_SERVOS 2

// ports
//out port toLeftServo = XS1_PORT_1E;
//out port toRightServo = XS1_PORT_1F;
out port oServos[] = {XS1_PORT_1E, XS1_PORT_1F};
//out port oServos[] = {XS1_PORT_1F};

// prototypes
void driver_task (chanend out_servo_cmd_chan , int pulse_increment, unsigned int delay_ticks);
void servo_task_multi(out port oServos[], chanend in_servo_cmd_chan);
void square_task (chanend out_servo_cmd_chan);

typedef struct {
	unsigned int pulse_width_us[NUM_SERVOS];
} servo_cmd_t;


int main()
{
	chan servo_cmd_chan;

	/**
	par {
		servo_task_multi(oServos, servo_cmd_chan);
		driver_task(servo_cmd_chan, 50, 750*TICKS_PER_MS);
	}**/

	par {
		servo_task_multi(oServos, servo_cmd_chan);
		square_task(servo_cmd_chan);
	}

	return 0;
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
	unsigned int curr_value =  min_value;
	int going_up = 1;
	servo_cmd_t m_command;

	while(1)
	{
		// Delay before sending command.
		tmr :> curr_time;
		tmr when timerafter(curr_time + delay_ticks) :> void;

		for(int i = 0; i < NUM_SERVOS; ++i)
			m_command.pulse_width_us[i] = curr_value;

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
	}
}


void square_task (chanend out_servo_cmd_chan)
{
	servo_cmd_t m_command;
	timer tmr;
	unsigned int time;

	// Pause for 3 sec so we can get the vehicle on the ground.
	m_command.pulse_width_us[0] = 1490;
	m_command.pulse_width_us[1] = 1500;
	out_servo_cmd_chan <: m_command;
	tmr :> time;
	time += 3000 * TICKS_PER_MS;
	tmr when timerafter(time) :> void;

	// Do the sides of a square.

	for(int i = 0; i < 4; ++i)
	{

		#ifdef DEBUG
		printstrln("Full speed");
		#endif

		// FULL SPEED AHEAD!
		m_command.pulse_width_us[0] = 1990;
		m_command.pulse_width_us[1] = 1000;
		out_servo_cmd_chan <: m_command;
		tmr :> time;

		time += 1500 * TICKS_PER_MS;
		tmr when timerafter(time) :> void;

		#ifdef DEBUG
		printstrln("Iceberg");
		#endif

		// ICEBERG
		// A full roatation with R off, L full took 3.49 secs to go 360degrees, or
		// 0.00969444444 secs/degree. That is
		m_command.pulse_width_us[0] = 2000;
		m_command.pulse_width_us[1] = 1500;
		out_servo_cmd_chan <: m_command;
		tmr :> time;

		time += 872500 * TICKS_PER_MICRO;
		tmr when timerafter(time) :> void;
	}


	//STOP!
	m_command.pulse_width_us[0] = 1490;
	m_command.pulse_width_us[1] = 1500;
	out_servo_cmd_chan <: m_command;
}


/** http://www.algorithmist.com/index.php/Bubble_sort.c **/
void bubbleSort(unsigned int numbers[], int array_size)
{
	unsigned int i, j, temp;

	for (i = (array_size - 1); i > 0; i--)
	{
		for (j = 1; j <= i; j++)
		{
			if (numbers[j-1] > numbers[j])
			{
				temp = numbers[j-1];
				numbers[j-1] = numbers[j];
				numbers[j] = temp;
			}
		}
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

void servo_task_multi(out port oServos[], chanend in_servo_cmd_chan)
{
	timer tmr;
	unsigned int frame;
	unsigned int widths[NUM_SERVOS];
	unsigned int smallest_finished;
	unsigned int smallest_tmp;
	unsigned int t;
	int finished;
	servo_cmd_t m_command;
	int num_finished;

	tmr :> frame;

	for(int i = 0; i < NUM_SERVOS; ++i)
		m_command.pulse_width_us[i] = 1500;

	while(1)
	{
		frame += 20 * TICKS_PER_MS;

		// Set up the widths
		for(int i = 0; i < NUM_SERVOS; ++i)
			widths[i] = m_command.pulse_width_us[i];


		// Sort them.
		bubbleSort(widths, NUM_SERVOS);


		// Turn the servos pulses on
		for(int i = 0; i < NUM_SERVOS; ++i)
			oServos[i] <: 1;


		// Turn them off one by one
		tmr :> t;
		for(int i = 0; i < NUM_SERVOS; ++i)
		{
			tmr when timerafter(t + (widths[i] * TICKS_PER_MICRO)) :> void;

			for(int j = 0; j < NUM_SERVOS; ++j)
				if(widths[i] >= m_command.pulse_width_us[j])
						oServos[j] <: 0;
		}

		finished = 0;
		while(! finished)
		{
			select
			{
				case tmr when timerafter(frame) :> void:
					finished = 1;
					break;

				// Commands are lowest priority
				case in_servo_cmd_chan :> m_command:
					break;
			}
		}
	}
}
