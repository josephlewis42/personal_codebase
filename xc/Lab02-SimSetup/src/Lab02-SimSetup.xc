#include <xs1.h>
#include <print.h>
#include "utility.h"
#include <stdio.h>
#include "platform.h"

#define TICKS_PER_MS (XS1_TIMER_HZ/1000)
#define NUM_PRESSES 3

in port iButton = PORT_BUT_1;
out port oButtonDriver = XS1_PORT_1A;
timer tmr;
timer t2;

void monitor_button();
void button_simulator();

int main()
{
	char buffer[64];

	// BEGIN TEST CASES
	/**
	format_message(buffer, TICKS_PER_MS, 50*TICKS_PER_MS);
	printstr(buffer);

	format_message(buffer, 800*TICKS_PER_MS, TICKS_PER_MS);
	printstr(buffer);
	 */
	//END TEST CASES

	par {
		monitor_button();
		button_simulator();
	}
}


void monitor_button()
{
	char buffer[64];
	unsigned int begin, end;

	// Wait for defulat state of unpressed
	iButton when pinseq(1) :> void;

	for(int i = 0; i < NUM_PRESSES; ++i)
	{
		iButton when pinseq(0) :> void;
		tmr :> begin;

		iButton when pinseq(1) :> void;
		tmr :> end;

		format_message(buffer, begin, end);
		printf(buffer);
	}
}

unsigned int currtime;
unsigned int wantedtime;
void button_simulator()
{
	oButtonDriver <: 1;

	for(int i = 0; i < NUM_PRESSES; ++i)
	{
		oButtonDriver <: 0;

		t2 :> currtime;
		wantedtime = currtime + (i * TICKS_PER_MS);

		t2 when timerafter(wantedtime) :> void;

		oButtonDriver <: 1;

		t2 :> currtime;
		wantedtime = currtime + (TICKS_PER_MS / 2);
		t2 when timerafter(wantedtime) :> void;
	}
}


