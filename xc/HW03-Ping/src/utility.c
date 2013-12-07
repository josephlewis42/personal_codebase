/*
 * utility.c
 *
 *  Created on: Apr 12, 2012
 *      Author: joseph
 */

#include "utility.h"

int ticks_to_mm(unsigned int ticks, unsigned int mm_per_sec, unsigned int ticks_per_sec)
{
	double tks = ticks;
	//double seconds = ticks;

	// How many seconds did this last?
	tks /= ticks_per_sec;

	// How many mm are there in the sec?
	tks *= mm_per_sec;

	// Being we're doing sonar, the wave must travel there *and* back, so divide by 2
	tks /= 2;

	return (int) tks;
}
