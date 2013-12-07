/*
 * lights.xc
 *
 *  Created on: May 28, 2012
 *      Author: Joseph Lewis <joehms22@gmail.com>
 */

// includes
#include "lights.h"
#include <xs1.h>
#include <print.h>
#include <string.h>
#include "platform.h"
#include "common_cmds.h"


// ports
out port oLEDs = PORT_LED;


// defns
void turn_on_leds();
void turn_off_leds();

// functions

void lights_thread(chanend c)
{
	int hz = 0;
	timer tmr;
	unsigned int on_period = 0;
	unsigned int off_period = XS1_TIMER_HZ;

	while(1)
	{
		turn_on_leds();
		wait_time(on_period, tmr);
		turn_off_leds();
		wait_time(off_period, tmr);


		select
		{
			case c :> hz:
				if(hz < 0)
				{
					on_period = XS1_TIMER_HZ;
					off_period = 0;
					break;
				}

				if(hz != 0)
				{
					on_period = (XS1_TIMER_HZ / (hz * 2));
					off_period = (XS1_TIMER_HZ / (hz * 2));
				}
				else
				{
					on_period = 0;
					off_period = XS1_TIMER_HZ;
				}
				break;
			default:
				break;
		}
	}
}

void turn_on_leds()
{
	oLEDs <: 0b1111;
}

void turn_off_leds()
{
	oLEDs <: 0b0000;
}


void lights_test(chanend lightschan)
{
	timer tmr;

	printstrln("==TESTING LIGHTS==");
	printstrln("0 HZ");
	lightschan <: 0;
	wait_time(XS1_TIMER_HZ, tmr);

	printstrln("1 HZ");
	lightschan <: 1;
	wait_time(XS1_TIMER_HZ, tmr);

	printstrln("2 HZ");
	lightschan <: 2;
	wait_time(XS1_TIMER_HZ, tmr);

	printstrln("3 HZ");
	lightschan <: 3;
	wait_time(XS1_TIMER_HZ, tmr);

	printstrln("Return to 0 HZ");
	lightschan <: 0;
	printstrln("==END TESTING LIGHTS==");

}

