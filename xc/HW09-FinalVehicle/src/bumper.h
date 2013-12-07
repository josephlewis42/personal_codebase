/*
 * buttons.h - Don't push mine.
 *
 *  Created on: May 28, 2012
 *      Author: Joseph Lewis <joehms22@gmail.com>
 */

#ifndef BUMPER_H
#define BUMPER_H

void wait_left_bumper_press();
void wait_right_bumper_press();
void wait_either_bumper_press();
void wait_left_bumper_release();
void wait_right_bumper_release();
void wait_all_bumper_release();
void test_bumpers();
int left_is_hit();
int right_is_hit();
int bumper_is_hit();


#endif /* BUTTONS_H_ */
