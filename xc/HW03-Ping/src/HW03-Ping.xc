/**
	Copyright 2012 Joseph Lewis <joehms22@gmail.com>
**/

// includes
#include <xs1.h>
#include <stdio.h>
#include <print.h>
#include "platform.h"
#include "utility.h"

// defines
#define TICKS_PER_SEC XS1_TIMER_HZ
#define TICKS_PER_MS (XS1_TIMER_HZ/1000)
#define TICKS_PER_MICRO (XS1_TIMER_HZ/1000000)
#define TIMER_MAX_VALUE 0x7FFFFFFF
#define DEBUG
#define BAUDRATE 96000

// constants
const unsigned int NUMSAMPLES = 3;
const unsigned int SAMPLES_MM[] = {1000,5000,10000};
// speed of sound at sea level: 340.29 m/s
const unsigned int SOUND_MM_PER_SECOND = 340290;

const unsigned int TOUT_US = 5;
const unsigned int THOLDOFF_US = 750;
const unsigned int TIN_MIN_US = 115;
const unsigned int TIN_MAX_US = 18500;


// ports
port ioPingPort = XS1_PORT_1A;
port ioPingSimulator = XS1_PORT_1B;


// prototypes (alphabetical)
void distance_consumer(chanend c);
void ping_task(port p, chanend c);
void ping_task_timeout(port p, chanend c, unsigned int timeout_ticks);
void ping_simulator(
		port p,
		const unsigned int mms[],
		unsigned int n_mms,
		unsigned int mm_per_second);

int main(void)
{
	chan c;
	par {
		//ping_task(ioPingPort, c);
		ping_task_timeout(ioPingPort, c, TIN_MAX_US * TICKS_PER_MICRO);

		distance_consumer(c);
		ping_simulator(ioPingSimulator,
				SAMPLES_MM,
				NUMSAMPLES,
				SOUND_MM_PER_SECOND);
	}
	return 0;
}



void distance_consumer(chanend c)
{
	int val;
	char buffer[64];

	for(int i = 0; i < NUMSAMPLES; ++i)
	{
		c :> val;
		sprintf(buffer, "Distance is: %i\n", val);
		printstrln(buffer);
	}
}

/**
 * Returns the # of ticks a ping takes.
 */
unsigned int do_ping(port p)
{
	unsigned int diststart;
	unsigned int distend;
	unsigned int time;
	timer t;
	t :> time;

	// Set output to low.
	p <: 0;

	// Set output to high for tout
	time += TOUT_US * TICKS_PER_MICRO;
	p <: 1;
	t when timerafter(time) :> void;

	// Set output to low for holdoff
	p <: 0;

	// Wait for half of holdoff
	time += (THOLDOFF_US / 2) * TICKS_PER_MICRO;
	t when timerafter(time) :> void;

	// Wait for pull up
	p when pinseq(1) :> void;

	// Start timer
	t :> diststart;

	// Wait for drop
	p when pinseq(0) :> void;
	t :> distend;

	return distend - diststart;

}

/**
 * Safely does a ping, with a timeout for possible holdups
 * returns a 0 if a timeout occcured.
 */
unsigned int do_safe_ping(port p, unsigned int timeout_ticks)
{
	unsigned int diststart;
	unsigned int distend;
	unsigned int time;
	timer t;
	t :> time;

	// Set output to low.
	p <: 0;

	// Set output to high for tout
	time += TOUT_US * TICKS_PER_MICRO;
	p <: 1;
	t when timerafter(time) :> void;

	// Set output to low for holdoff
	p <: 0;

	// Wait for half of holdoff
	time += (THOLDOFF_US / 2) * TICKS_PER_MICRO;
	t when timerafter(time) :> void;

	// Wait for pull up
	t :> time;
	time += timeout_ticks;
	select
	{
		case p when pinseq(1) :> void:

			break;
		case t when timerafter(time) :> void:
			return 0;
			break;
	}

	// Start timer
	t :> diststart;

	// Wait for drop
	t :> time;
	time += timeout_ticks;
	select
	{
		case p when pinseq(0) :> void:
			t :> distend;
			break;
		case t when timerafter(time) :> void:
			return 0;
			break;
	}

	return distend - diststart;

}

void ping_task(port p, chanend c)
{
	unsigned int time;

	for(int i = 0; i < NUMSAMPLES; ++i)
	{
		time = do_ping(p);
		c <: ticks_to_mm(time, SOUND_MM_PER_SECOND, TICKS_PER_SEC);
	}
}


void ping_task_timeout(port p, chanend c, unsigned int timeout)
{
	unsigned int time;

	for(int i = 0; i < NUMSAMPLES; ++i)
	{
		time = do_safe_ping(p, timeout);
		if(time == 0)
			c <: -1;
		else
			c <: ticks_to_mm(time, SOUND_MM_PER_SECOND, TICKS_PER_SEC);
	}
}
