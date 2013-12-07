
#include "servo.h"
#include "utility.h"

#define SERVO_PERIOD (20*TICKS_PER_MS)
#define SERVO_CHANNEL_SPACING_US 2100

servo_cmd_t default_servo_cmd()
{
	servo_cmd_t sc;
	unsigned int i;
	for(i=0; i<MAX_NUM_SERVOS; i++){
		sc.pulse_width_us[i] = MID_SERVO_PULSE_US;
	}
	return sc;
}

void servo_task_multi(
		unsigned int nServos,
		out port oServos[],
		const int servo_offsets[],
		chanend in_servo_cmd_chan)
{
	timer tmr;
	unsigned int t, timed_out, i, t2, pulse_ticks;
	servo_cmd_t servo_cmd;

	// initialize
	for(i=0; i<nServos; i++){
		servo_cmd.pulse_width_us[i] = MID_SERVO_PULSE_US;
		oServos[i] <: 0;
	}

	tmr :> t;
	while(1){
		t2 = t;
		for(i = 0; i < nServos; i++){
			pulse_ticks = servo_cmd.pulse_width_us[i] + servo_offsets[i];
			oServos[i] <: 1;
			tmr when timerafter(t2 + pulse_ticks*TICKS_PER_US) :> void;
			oServos[i] <: 0;
			// make sure the channels are spaced evenly, no matter what the pulse width was
			t2 += SERVO_CHANNEL_SPACING_US*TICKS_PER_US;
			tmr when timerafter(t2) :> void;
		}

		// calculate start of next frame
		t += SERVO_PERIOD;

		// wait repeatedly for servo cmd until timeout
		while(1){
			timed_out = 0;
			select {
				case tmr when timerafter(t) :> void:
					timed_out = 1;
					break; // break select

				case in_servo_cmd_chan :> servo_cmd:
					break; // break select
			}
			if(timed_out == 1){
				break; // break the while loop
			}
		}
	}
}
/**
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
				if(t > frame + (m_command.pulse_width_us[i] + servo_offsets[i]) * TICKS_PER_US)
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
}**/

