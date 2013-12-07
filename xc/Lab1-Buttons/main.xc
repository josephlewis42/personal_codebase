#include <xs1.h>
#include "platform.h"
#include <stdio.h>

in port iButton =  PORT_BUT_1;
out port oLeds = PORT_LED;

unsigned int compute_difference(unsigned int t0, unsigned int t1);

int main()
{
	timer tmr;
	unsigned int begin;
	unsigned int end;

	while(1)
	{
		iButton when pinseq(0) :> void;
		tmr :> begin;
		printf("Pressed: %d\n", begin);

		iButton when pinseq(1) :> void;
		tmr :> end;
		printf("Unpressed: %d\n", end);

		printf("Diff: %d\n", compute_difference(begin, end));


		/**iButton when pinseq(0) :> void;
		oLeds <: 0b1111;

		iButton when pinseq(1) :> void;
		oLeds <: 0b0000;
		**/

		/**
		 *
		 int value;
		iButton :> value;
		if(! value)
		{
			oLeds <: 0b1111;
		}
		else
		{
			oLeds <: 0;
		}
		*/

	}
	return 0;
}


unsigned int compute_difference(unsigned int t0, unsigned int t1)
{

	if(t1 < t0)
	{
		return (XS1_TIMER_HZ - t0) + t1;
	}

	return t1 - t0;
}
