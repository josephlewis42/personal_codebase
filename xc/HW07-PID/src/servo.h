#ifndef SERVO_H_
#define SERVO_H_

// constants
#define MIN_SERVO_PULSE_US 1000
#define MID_SERVO_PULSE_US 1500
#define MAX_SERVO_PULSE_US 2000
#define MAX_NUM_SERVOS 8

// types
typedef struct {
	unsigned int pulse_width_us[MAX_NUM_SERVOS];
} servo_cmd_t;

// prototypes
servo_cmd_t default_servo_cmd();

void servo_task_multi(
		unsigned int nServos,
		out port oServos[],
		const int servo_offsets[],
		chanend in_servo_cmd_chan);

#endif
