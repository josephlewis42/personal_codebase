/*
 * utility.c
 *
 *  Created on: Apr 5, 2012
 *      Author: joseph
 */
#include <xs1.h>
#include "utility.h"
#include <stdio.h>


float timer_diff(unsigned int t0, unsigned int t1)
{
	if(t1 < t0)
	{
		return ((float)((XS1_TIMER_HZ - t0) + t1)) / XS1_TIMER_HZ;
	}

	return ((float)(t1 - t0)) / XS1_TIMER_HZ;
}


void format_message(char buffer[], unsigned int t0, unsigned int t1)
{
	sprintf(buffer, "Difference was %f seconds\n", timer_diff(t0,t1));
}
