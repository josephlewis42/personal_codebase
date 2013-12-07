/*
 * director.h - There are no small roles.
 *
 *  Created on: May 28, 2012
 *      Author: Joseph Lewis <joehms22@gmail.com>
 */

#ifndef DIRECTOR_H_
#define DIRECTOR_H_

#define GO_FORWARD 0
#define TURN_NINETY_LEFT 1
#define TURN_NINETY_RIGHT 2
#define STOP 3

enum driving_commands{
	forward,
	left_ninety,
	right_ninety,
	stop
};


struct direction_t;
typedef struct direction_t {
	int command; // GO_FORWARD, TURN_NINETY_LEFT, etc.
	int param; // PARAM, GO_FORWARD = num mm to go
} direction;


void directions_thread( chanend direction_output, int start_rank, int goal_rank, const int obstacles[]);
void director_test( chanend direction_input);

#endif /* DIRECTOR_H_ */
