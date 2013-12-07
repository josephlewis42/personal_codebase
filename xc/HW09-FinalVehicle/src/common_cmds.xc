/*
 * common_cmds.xc
 *
 *  Created on: May 28, 2012
 *      Author: joseph
 */

#include <xs1.h>
#include "platform.h"
#include "common_cmds.h"

void wait_time(unsigned int time, timer tmr)
{
	unsigned int t;
	tmr :> t;
	t += time;
	tmr when timerafter (t) :> void;
}


int normalize_heading(int heading)
{
	while(heading < 0)
		heading += 360;
	return heading % 360;
}
