/*
 * americus.h - The head of the navigator.
 *
 *  Created on: May 29, 2012
 *      Author: joseph
 */

#ifndef AMERICUS_H_
#define AMERICUS_H_

void navigate_maze(chanend lightschan, chanend directions, chanend out_servo_cmd_chan, i2c_p& i2c);
void test_navigation(chanend lightschan, chanend directions, chanend out_servo_cmd_chan, i2c_p& i2c);

#endif /* AMERICUS_H_ */
