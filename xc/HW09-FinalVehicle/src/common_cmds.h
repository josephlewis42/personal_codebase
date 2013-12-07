/*
 * common_cmds.h - Useful commands that are used everywhere.
 *
 *  Created on: May 28, 2012
 *      Author: joseph
 */

#ifndef COMMON_CMDS_H_
#define COMMON_CMDS_H_

#include <xs1.h>

#define TICKS_PER_SEC XS1_TIMER_HZ
#define TICKS_PER_MS (XS1_TIMER_HZ/1000)
#define TICKS_PER_US (XS1_TIMER_HZ/1000000)
#define TIMER_MAX_VALUE 0x7FFFFFFF

// Waits the given number of ticks.
void wait_time(unsigned int time, timer tmr);

// Converts numbers to wherever they are on a circle, even negative and those over 360*
int normalize_heading(int heading);

#endif /* COMMON_CMDS_H_ */
