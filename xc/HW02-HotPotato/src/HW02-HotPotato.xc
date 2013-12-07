#include <stdio.h>
#include <print.h>
#include "platform.h"

#define TICKS_PER_MICROS (XS1_TIMER_HZ/1000000)
#define TICKS_PER_MILLS (XS1_TIMER_HZ/1000)

#define BUTTON_TIMEOUT_MS 2
#define MAX_HOPS 10
#define PRINT_DELAY 10
#define BUTTON_SIMULATION_PRESS_TIME_US 1
#define BUTTON_SIMULATION_HOLD_TIME_US 1

void worker ( unsigned int workerid, chanend left , chanend right ) ;
int worker_fx(chanend tosend, int packet, timer t, char dir[], unsigned int worker);
void buttonlistenertask (chanend left, chanend right);
void btn_sim();


in port iButton1 = PORT_BUT_1;
out port oButtonDriver1 = XS1_PORT_1A;

int main()
{
	chan a;
	chan b;
	chan c;
	chan d;

	par
	{
			buttonlistenertask(c, d);
			worker(1, d, a);
			worker(2, a, b);
			worker(3, b, c);

			btn_sim();
	}
}


void worker( unsigned int workerid, chanend left, chanend right)
{
	timer t;
	int packet;
	unsigned int currtime;

	// If the worker ID of the process is 1, it should introduce, 1 new packet to the channel on the right.
	if(workerid == 1)
		right <: 1;

	// Use select to listen on both the left and the right channels simultaneously.
    //Return if the value of the token is greater than 10, or if the task has not received a token in 1 millisecond.
	while(1)
	{
		t :> currtime;
		currtime += TICKS_PER_MILLS;

		select
		{
				case left :> packet:
					if(worker_fx(right, packet, t, "left", workerid))
						return;
				break;
				case right :> packet:
					if(worker_fx(left, packet, t, "right", workerid))
						return;
				break;
				case t when timerafter(currtime) :> void:
					return;
				break;
		}
	}
}

// returns true if packet hops > MAX_HOPS
int worker_fx(chanend tosend, int packet, timer t, char dir[], unsigned int worker)
{
	char msg[64];
	unsigned int currtime;

	// Format message
	sprintf(msg, "Packet recieved on %i from %s, hop is: %i\n",worker, dir, packet);
	printstr(msg);

	// Increment token
	packet++;



	// Delay by X microseconds (10 is in the specs)
	t :> currtime;
	currtime += TICKS_PER_MICROS * PRINT_DELAY;
	t when timerafter(currtime) :> void;

	// Send the packet off.
	if(packet <= 10)
		tosend <: packet;

	// Return true if packet is > MAX_HOPS
	return (packet > MAX_HOPS);
}


/**
 * This task will function as follows:
• Initially (outside the loop) wait for the button pin to go high. This will help
   synchronize the simulation.
• Within an infinite loop, use select to monitor a button input pin, the two
     channels, and a timer.
• When the token comes in on one of the channels, this task does not change
   the value of the token, it simply passes it around the ring. When the button is
  depressed, and then released, this task will make sure to reverse the direction
 of the token the next time it is received.
• If this task receives no inputs from the channels or the button for 2 millisec-
   onds. it should terminate.
 */
void buttonlistenertask (chanend left, chanend right)
{
	timer t;
	unsigned int currtime;
	unsigned int reverse_next; // 1 if button pressed, 2 on release
	int packet;
	reverse_next = 0;

	// Wait for button to go high for synch.
	iButton1 when pinseq(1) :> void;

	// Within an infinite loop, use select to monitor a button input pin, the two channels, and a timer.
	while(1)
	{

		// SETUP CLOCK FOR TIMEOUT
		t :> currtime;
		currtime += TICKS_PER_MILLS * BUTTON_TIMEOUT_MS;


		select
		{
			case left :> packet:
				if(reverse_next)
				{
					left <: packet;
					reverse_next = 0;
				}
				else
					right <: packet;
			break;
			case right :> packet:
				if(reverse_next)
				{
					right <: packet;
					reverse_next = 0;
				}
				else
					left <: packet;
			break;

			case iButton1 when pinseq(0) :> void:
				if(!reverse_next)
					reverse_next = 2;
			break;

			case t when timerafter(currtime) :> void:
				return;
			break;
		}
	}
}


/**
 * Implement a button simulator task, similar to what was done in the in class sections.
 * This should do the following:
 * - Set the output pin to high (to help synchronize the simulation).
 * - It should then delay by one microsecond, simulate a button press,
 * - delay by another microsecond, simulate the button release, and then return.
 */
void btn_sim()
{
	timer t;
	unsigned int currtime;

	// Drive high.
	oButtonDriver1 <: 1;


	// Delay 1 microsecond
	t :> currtime;
	currtime += TICKS_PER_MICROS * BUTTON_SIMULATION_PRESS_TIME_US;
	t when timerafter(currtime) :> void;

	// button press
	oButtonDriver1 <: 0;

	// delay 1 microsecond
	t :> currtime;
	currtime += TICKS_PER_MICROS * BUTTON_SIMULATION_HOLD_TIME_US;
	t when timerafter(currtime) :> void;

	// button release
	oButtonDriver1 <: 1;

	// return
}
