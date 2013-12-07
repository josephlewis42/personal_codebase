
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

#define SERVO_MIDWAY_PULSE_WIDTH_US 1500
#define MAX_SERVO_WIDTH_US 2000
#define MIN_SERVO_WIDTH_US 1000
//#define DEBUG
#define MAX_NUM_SERVOS 2

// ports Left 1E Right 1F
//out port oServos[] = {XS1_PORT_1E, XS1_PORT_1F};
out port oServos[] = {XS1_PORT_1F, XS1_PORT_1E};

in port plusButton = PORT_BUT_1;
in port minusButton = PORT_BUT_2;

// prototypes
void servo_task_multi(unsigned int nServos,
							out port oServos[],
							const int servo_offsets[],
							chanend in_servo_cmd_chan);

void neutral_ui_task(unsigned int increment_us,
						in port iPlusButton,
						in port iMinusButton,
						chanend out_servo_cmd_t);

typedef struct {
	unsigned int pulse_width_us[MAX_NUM_SERVOS];
} servo_cmd_t;



int main()
{
	chan cmd_chan;
	const int offsets[] = {0,-16};

	par
	{
		servo_task_multi(2, oServos, offsets, cmd_chan);
		neutral_ui_task(1, plusButton, minusButton, cmd_chan);
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
			oServos[i] <: 1;


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
					numdone++;
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


void neutral_ui_task(unsigned int increment_us,
						in port iPlusButton,
						in port iMinusButton,
						chanend out_servo_cmd_t)
{
	servo_cmd_t m_command;

	m_command.pulse_width_us[0] = SERVO_MIDWAY_PULSE_WIDTH_US;

	while(1)
	{
		printintln(m_command.pulse_width_us[0]);
		out_servo_cmd_t <: m_command;

		select
		{
			case iPlusButton when pinseq(0) :> void:
				m_command.pulse_width_us[0] += 1;
				if(m_command.pulse_width_us[0] > MAX_SERVO_WIDTH_US)
					m_command.pulse_width_us[0] = MAX_SERVO_WIDTH_US;
				iPlusButton when pinseq(1) :> void;
				break;

			case iMinusButton when pinseq(0) :> void:
				m_command.pulse_width_us[0] -= 1;
				if(m_command.pulse_width_us[0] < MIN_SERVO_WIDTH_US)
					m_command.pulse_width_us[0] = MIN_SERVO_WIDTH_US;
				iMinusButton when pinseq(1) :> void;
				break;
		}
	}
}
