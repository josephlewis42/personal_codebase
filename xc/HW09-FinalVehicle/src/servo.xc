
#include "servo.h"
#include "utility.h"

#define SERVO_PERIOD (20 * TICKS_PER_MS)
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

			// do bounds checking on the servos...
			if(pulse_ticks > MAX_SERVO_PULSE_US)
				pulse_ticks = MAX_SERVO_PULSE_US;
			if(pulse_ticks < MIN_SERVO_PULSE_US)
				pulse_ticks = MIN_SERVO_PULSE_US;

			oServos[i] <: 1;
			tmr when timerafter(t2 + pulse_ticks * TICKS_PER_US) :> void;
			oServos[i] <: 0;
			// make sure the channels are spaced evenly, no matter what the pulse width was
			t2 += SERVO_CHANNEL_SPACING_US * TICKS_PER_US;
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

