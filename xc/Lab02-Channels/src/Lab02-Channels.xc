#include <print.h>
#include "platform.h"
#include <stdio.h>


#define NUM_PRESSES 3
#define TICKS_PER_MS (XS1_TIMER_HZ/1000)


in port iButton1 = PORT_BUT_1;
in port iButton2 = PORT_BUT_2;
out port oButtonDriver1 = XS1_PORT_1A;
out port oButtonDriver2 = XS1_PORT_1B;

void display_output(chanend c);
void monitor_buttons(chanend c);
void button_simulator();

int main()
{
	chan c;
	par{
		display_output(c);
		monitor_buttons(c);
		button_simulator();
	}
}

void display_output(chanend c)
{
	char buffer[64];
	int channel_read;

	for(int i = 0; i < NUM_PRESSES; ++i)
	{
		c :> channel_read;

		sprintf(buffer, "Button %i was pressed.\n", channel_read);
		printstr(buffer);
	}
}


void monitor_buttons(chanend c)
{
	// For num presses
	for(int i = 0; i < NUM_PRESSES; ++i)
	{
		// Wait for both buttons to go high.
		iButton1 when pinseq(1) :> void;
		iButton2 when pinseq(1) :> void;

		select
		{
			case iButton1 when pinseq(0) :> void:
				c <: 1;
			break;
			case iButton2 when pinseq(0) :> void:
				c <: 2;
			break;
		}
	}
}

timer t2;
void button_simulator()
{
	unsigned int currtime;

	oButtonDriver1 <: 1;
	oButtonDriver2 <: 1;

	t2 :> currtime;
	currtime += TICKS_PER_MS;
	t2 when timerafter(currtime) :> void;

	for(int i = 0; i < NUM_PRESSES; ++i)
	{
		if((i % 2) == 0) // i is even
		{
			oButtonDriver2 <: 0;
		} else {
			oButtonDriver1 <: 0;
		}

		// Wait 1 ms
		t2 :> currtime;
		currtime += TICKS_PER_MS;
		t2 when timerafter(currtime) :> void;

		// Set both ports to HIGH
		oButtonDriver1 <: 1;
		oButtonDriver2 <: 1;
	}

}

