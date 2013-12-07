/**
	Copyright 2012 Joseph Lewis <joehms22@gmail.com>
**/

// includes
#include <xs1.h>
#include <stdlib.h>
#include <stdio.h>
#include <print.h>
#include "platform.h"
#include "bfs.h"

// defines
#define TICKS_PER_SEC XS1_TIMER_HZ
#define TICKS_PER_MS (XS1_TIMER_HZ/1000)
#define TICKS_PER_US (XS1_TIMER_HZ/1000000)
#define TIMER_MAX_VALUE 0x7FFFFFFF
#define DEBUG

// ports


// prototypes


int main(void)
{
	test_main();
	return 0;
}
