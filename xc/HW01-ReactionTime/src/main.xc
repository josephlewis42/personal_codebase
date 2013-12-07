/**
 * Reaction time tester.
 */

#include <xs1.h>
#include <stdio.h>

#include "platform.h"
#include "stdlib.h"

#define FLASH_ON_PERIOD XS1_TIMER_HZ / 2
#define NUM_FLASHES 3
#define NUM_SAMPLES_BEFORE_STATS 10
#define TICKS_PER_US (XS1_TIMER_HZ / 1000000)
//#define TICKS_PER_US (XS1_TIMER_HZ / 1)


void wait_time(unsigned int time);
void turn_on_leds();
void turn_off_leds();
void do_stats();
void add_to_array(unsigned int k, int cnitems);
unsigned int compute_difference(unsigned int t0, unsigned int t1);

timer tmr;
out port oLEDs = PORT_LED;
in port iButton =  PORT_BUT_1;

unsigned int begin_time;
unsigned int end_time;
unsigned int diff;
unsigned int samples [NUM_SAMPLES_BEFORE_STATS];
int curr_iteration;

int main(void)
{
	curr_iteration = 0;

	while(1)
	{
		// Flash 3 times with period 1 sec
		for(int i = 0; i < NUM_FLASHES; i++)
		{
			wait_time(FLASH_ON_PERIOD);
			turn_on_leds();

			wait_time(XS1_TIMER_HZ - FLASH_ON_PERIOD);
			turn_off_leds();
		}

		// Delay 1 sec
		wait_time(XS1_TIMER_HZ);

		// Delay up to 1 more sec
		wait_time(XS1_TIMER_HZ + rand() % XS1_TIMER_HZ);

		// Illuminate all 4 LEDs
		turn_on_leds();

		// Wait until button is pressed
		tmr :> begin_time;
		iButton when pinseq(0) :> void;
		tmr :> end_time;
		// Turn off LEDs
		turn_off_leds();

		// Compute difference
		diff = compute_difference(begin_time, end_time);

		// Record in array
		add_to_array(diff, curr_iteration);

		// Increase the loop counter
		curr_iteration ++;

		// If enough samples taken, print out stats
		if(curr_iteration == NUM_SAMPLES_BEFORE_STATS)
		{
			curr_iteration = 0;
			do_stats();
		}

		// Delay 1 second
		wait_time(XS1_TIMER_HZ);

	}
}


void wait_time(unsigned int time)
{
	unsigned int t;
	tmr :> t;
	t += time;
	tmr when timerafter (t) :> void;
}

void turn_on_leds()
{
	oLEDs <: 0b1111;
}

void turn_off_leds()
{
	oLEDs <: 0b0000;
}

unsigned int compute_difference(unsigned int t0, unsigned int t1)
{

	if(t1 < t0)
	{
		return ((XS1_TIMER_HZ - t0) + t1) / TICKS_PER_US;
	}

	return (t1 - t0) / TICKS_PER_US;
}

void add_to_array(unsigned int k, int cnitems)
{
	unsigned int curr_item = k;

	for(int i = 0; i < cnitems; i++)
	{
		if(curr_item < samples[i])
		{
			unsigned int tmp = samples[i];
			samples[i] = curr_item;
			curr_item = tmp;
		}
	}

	samples[cnitems] = curr_item;
}

void do_stats()
{
	unsigned int avg = 0;

	// Print min
	printf("Min: %u\n", samples[0]);

	// Print max
	printf("Max: %u\n", samples[NUM_SAMPLES_BEFORE_STATS - 1]);

	// Print avg
	for(int i = 0; i < NUM_SAMPLES_BEFORE_STATS; ++i)
		avg += samples[i] ;
	printf("Avg: %u\n", avg / NUM_SAMPLES_BEFORE_STATS);

	// Print median
	printf("Med: %u\n", samples[NUM_SAMPLES_BEFORE_STATS / 2]);

	/**
	printf("[");
	for(int i = 0; i < NUM_SAMPLES_BEFORE_STATS; i++)
		printf("%u,", samples[i]);
	printf("]\n\n");
	**/
}
