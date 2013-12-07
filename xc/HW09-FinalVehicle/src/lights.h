/*
 * lights.h - Pretty Lights
 *
 *  Created on: May 28, 2012
 *      Author: Joseph Lewis <joehms22@gmail.com>
 */

#ifndef LIGHTS_H_
#define LIGHTS_H_

// chanend c takes an int as the number of hz to flash at, 0 is off, < 0 is full on
void lights_thread(chanend c);

// Blinks at 0 hz for 1 sec, 2 hz for 1 sec, 3 hz for 1 sec, then 4 hz for 1 sec
void lights_test(chanend c);

#endif /* LIGHTS_H_ */
