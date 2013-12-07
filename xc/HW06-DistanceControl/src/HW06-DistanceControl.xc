/**
	Copyright 2012 Joseph Lewis <joehms22@gmail.com>
**/

// includes
#include <xs1.h>
#include <stdlib.h>
#include <stdio.h>
#include <print.h>
#include "platform.h"
#include "DistanceControlHelper.h"

// defines
#define TICKS_PER_SEC XS1_TIMER_HZ
#define TICKS_PER_MS (XS1_TIMER_HZ/1000)
#define TICKS_PER_MICRO (XS1_TIMER_HZ/1000000)
#define TIMER_MAX_VALUE 0x7FFFFFFF

#define SERVO_MIDWAY_PULSE_WIDTH_US 1500
#define MAX_SERVO_WIDTH_US 2000
#define MIN_SERVO_WIDTH_US 1000
#define RIGHT_SERVO_INDEX 0
#define LEFT_SERVO_INDEX 1
#define MAX_NUM_SERVOS 2
#define BUMPER_START_DELAY (XS1_TIMER_HZ)

#define SLOWDOWN_DIST_MM 100
#define SLOWDOWN_STEPS 10

// ports Left 1E Right 1F
out port oServos[] = {XS1_PORT_1F, XS1_PORT_1E};

in port plusButton = PORT_BUT_1;
in port minusButton = PORT_BUT_2;
in port iRightBumper = XS1_PORT_1H;
in port iLeftBumper = XS1_PORT_1G;

// prototypes
void servo_task_multi(unsigned int nServos,
							out port oServos[],
							const int servo_offsets[],
							chanend in_servo_cmd_chan);

void velocity_ui_task(unsigned int increment_us,
						in port iPlusButton,
						in port iMinusButton,
						in port iRightBumper,
						in port iLeftBumper,
						chanend out_servo_cmd_t);

void distance_control_task(in port iButton,
							unsigned int distance_mm,
							chanend out_servo_cmd_chan);

typedef struct
{
	unsigned int pulse_width_us[MAX_NUM_SERVOS];
} servo_cmd_t;

unsigned int velocity_ui_task_timer(in port iRightBumper,
										in port iLeftBumper,
										chanend out_servo_cmd_t,
										servo_cmd_t m_command);





int main()
{
	chan cmd_chan;
	const int offsets[] = {0,-11};

	par
	{
		servo_task_multi(2, oServos, offsets, cmd_chan);
		//velocity_ui_task(100, plusButton, minusButton, iRightBumper, iLeftBumper, cmd_chan);
		distance_control_task(plusButton, 100, cmd_chan);
	}
	return 0;
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

void servo_task_multi(unsigned int nServos,
							out port oServos[],
							const int servo_offsets[],
							chanend in_servo_cmd_chan)
{
	timer tmr;
	unsigned int frame;
	unsigned int smallest_finished;
	unsigned int smallest_tmp;
	unsigned int t;
	int finishedservos [MAX_NUM_SERVOS];
	int finished, numdone;
	servo_cmd_t m_command;
	int num_finished;

	tmr :> frame;

	for(int i = 0; i < nServos; ++i)
		m_command.pulse_width_us[i] = 1500;

	while(1)
	{

		// Turn the servos pulses on
		for(int i = 0; i < nServos; ++i)
		{
			finishedservos[i] = 0;
			oServos[i] <: 1;
		}

		// Turn them off one by one
		numdone = 0;
		while(numdone != nServos)
		{
			tmr :> t;
			for(int i = 0; i < nServos; ++i)
			{
				if(t > frame + (m_command.pulse_width_us[i] + servo_offsets[i]) * TICKS_PER_MICRO)
				{
					oServos[i] <: 0;
					if(! finishedservos[i])
					{
						finishedservos[i] = 1;
						numdone++;
					}
				}
			}
		}

		frame += 20 * TICKS_PER_MS;

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

unsigned int velocity_ui_task_timer(in port iRightBumper,
										in port iLeftBumper,
										chanend out_servo_cmd_t,
										servo_cmd_t m_command)
{
	timer tmr;
	unsigned int t, t0, t1;
	int finished = 0;
	servo_cmd_t stop_command;
	stop_command.pulse_width_us[RIGHT_SERVO_INDEX] = SERVO_MIDWAY_PULSE_WIDTH_US;
	stop_command.pulse_width_us[LEFT_SERVO_INDEX] = SERVO_MIDWAY_PULSE_WIDTH_US;

	// Wait for 1 second
	tmr :> t;
	tmr when timerafter(t + BUMPER_START_DELAY) :> void;

	// Send cmd
	out_servo_cmd_t <: m_command;

	// Take timestamp
	tmr :> t0;

	// Wait for either bumper to trigger
	while(! finished){
		select
		{
			case iRightBumper when pinseq(1) :> void:
				finished = 1;
				break;
			case iLeftBumper when pinseq(1) :> void:
				finished = 1;
				break;
		}
	}

	// Take second timestamp
	tmr :> t1;


	out_servo_cmd_t <: stop_command;


	// Print console
	printuintln(t1 - t0);

	// Wait for 1 second to kill bounce.
	tmr :> t;
	tmr when timerafter(t + BUMPER_START_DELAY) :> void;
	iRightBumper when pinseq(0) :> void;
	iLeftBumper when pinseq(0) :> void;

	return t1 - t0;
}


void velocity_ui_task(unsigned int increment_us,
						in port iPlusButton,
						in port iMinusButton,
						in port iRightBumper,
						in port iLeftBumper,
						chanend out_servo_cmd_t)
{

	servo_cmd_t m_command;
	int finished;


	m_command.pulse_width_us[RIGHT_SERVO_INDEX] = SERVO_MIDWAY_PULSE_WIDTH_US;
	m_command.pulse_width_us[LEFT_SERVO_INDEX] = SERVO_MIDWAY_PULSE_WIDTH_US;

	while(1)
	{
		printcharln('n');
		select
		{
			//
			case iPlusButton when pinseq(0) :> void:
				m_command.pulse_width_us[RIGHT_SERVO_INDEX] += increment_us;
				m_command.pulse_width_us[LEFT_SERVO_INDEX]  -= increment_us;
				iPlusButton when pinseq(1) :> void;
				break;

			case iMinusButton when pinseq(0) :> void:
				m_command.pulse_width_us[RIGHT_SERVO_INDEX] -= increment_us;
				m_command.pulse_width_us[LEFT_SERVO_INDEX]  += increment_us;
				iMinusButton when pinseq(1) :> void;
				break;

			case iRightBumper when pinseq(1) :> void:
				// Wait for release
				iRightBumper when pinseq(0) :> void;

				velocity_ui_task_timer(iRightBumper, iLeftBumper, out_servo_cmd_t, m_command);
				break;

			case iLeftBumper when pinseq(1) :> void:
				// Wait for release
				iLeftBumper when pinseq(0) :> void;

				velocity_ui_task_timer(iRightBumper, iLeftBumper, out_servo_cmd_t, m_command);
				break;
		}
	}
}



void distance_control_task(in port iButton,
							unsigned int distance_mm,
							chanend out_servo_cmd_chan)
{
	const int distance_mm_fullspeed = distance_mm - SLOWDOWN_DIST_MM;
	const int distance_mm_slowdown_step = SLOWDOWN_DIST_MM / SLOWDOWN_STEPS;
	unsigned int curr_pulse_duration;
	servo_cmd_t m_command;
	timer tmr;
	unsigned int t;
	const int servo_slowdown_step = (MAX_SERVO_WIDTH_US - SERVO_MIDWAY_PULSE_WIDTH_US) / SLOWDOWN_STEPS;

	while(1)
	{
		// Pause the servos
		m_command.pulse_width_us[RIGHT_SERVO_INDEX] = SERVO_MIDWAY_PULSE_WIDTH_US;
		m_command.pulse_width_us[LEFT_SERVO_INDEX] = SERVO_MIDWAY_PULSE_WIDTH_US;

		// Wait for button press and release
		iButton when pinseq(0) :> void;
		iButton when pinseq(1) :> void;


		// Go fast

		// Full Speed Ahead
		m_command.pulse_width_us[LEFT_SERVO_INDEX] = 2000;
		m_command.pulse_width_us[RIGHT_SERVO_INDEX] = 1000;

		if(distance_mm_fullspeed > 0)
		{
			curr_pulse_duration = find_pulse_duration_ms(2000, distance_mm_fullspeed);


			out_servo_cmd_chan <: m_command;

			// Wait for the specified time
			tmr :> t;
			tmr when timerafter(t + (TICKS_PER_MS * curr_pulse_duration)) :> void;
		}

		// Do slowdown
		for(int i = 0; i < 5; ++i)
		{
			m_command.pulse_width_us[LEFT_SERVO_INDEX] -= 100;
			m_command.pulse_width_us[RIGHT_SERVO_INDEX] += 100;

			curr_pulse_duration = (unsigned int) find_pulse_duration_ms(m_command.pulse_width_us[LEFT_SERVO_INDEX], 20);

			out_servo_cmd_chan <: m_command;

			// Wait for the specified time
			if(curr_pulse_duration > 500)
				continue;

			tmr :> t;
			tmr when timerafter(t + (TICKS_PER_MS * curr_pulse_duration)) :> void;
		}
	}
}
