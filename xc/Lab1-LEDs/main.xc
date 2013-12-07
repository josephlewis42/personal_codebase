/*
 * main.xc
 *
 *  Created on: Mar 29, 2012
 *      Author: joseph
 */

#include <xs1.h>
#include "platform.h"
#define FLASH_DELAY (XS1_TIMER_HZ/10)


out port oLEDs = PORT_LED;

int main()
{
	timer tmr;
	unsigned int t;
	unsigned pattern = 0b0110;

	tmr :> t;
	while(1)
	{
		oLEDs <: pattern;

		t += FLASH_DELAY;
		tmr when timerafter (t) :> void;
		pattern = ~pattern;
	}
	return 0;
}
