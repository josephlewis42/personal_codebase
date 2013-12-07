/**
	Copyright 2012 Joseph Lewis <joehms22@gmail.com>
**/

// includes
#include <xs1.h>
#include <stdlib.h>
#include <stdio.h>
#include <print.h>
#include "platform.h"
#include "i2c.h"

// defines
#define TICKS_PER_SEC XS1_TIMER_HZ
#define TICKS_PER_MS (XS1_TIMER_HZ/1000)
#define TICKS_PER_US (XS1_TIMER_HZ/1000000)
#define TIMER_MAX_VALUE 0x7FFFFFFF
#define DEBUG
#define HMC6352_ID_WRITE 0x42
#define HMC6352_ID_READ 0x43
#define HMC6352_READ_EEPROM 0x72

// ports


// prototypes
int read_EEPROM( i2c_p &i2c, unsigned char addr );
int read_RAM( i2c_p &i2c, unsigned char addr );

i2c_p i2c = {
	XS1_PORT_1A, 	// s c l
	XS1_PORT_1B, 	// sda
	0, 				// t
	0,				// tmr
	10000			// delay
};



int main(void)
{
	int read_val;
	char buff[64];
	timer tmr;
	int t;

	i2c_init( i2c );

	// EEPROM Read
	for(int i = 0x00; i < 0x0e; i++)
	{
		// (Command ASCII Byte) (Argument Binary MS Byte) (Argument Binary LS Byte)
		read_val = read_EEPROM( i2c, i );


		// Do buffer.
		sprintf(buff, "EEPROM: 0x%x Response val: 0x%x", i, read_val);
		printstrln(buff);

		// wait
		tmr :> t;
		tmr when timerafter(t + 100 * TICKS_PER_MS) :> void;
	}

	for(int i = 0x00; i < 0xFF; i++)
	{
		read_val = read_RAM( i2c, i );

		sprintf(buff, "%2x|",  read_val);
		if(i % 10 == 9)
			printstrln(buff);
		else
			printstr(buff);

		// wait
		tmr :> t;
		tmr when timerafter(t + 20 * TICKS_PER_MS) :> void;
	}

	return 0;
}


int read_EEPROM( i2c_p &i2c, unsigned char addr )
{
	int read_val;

	// Tell device we want to read.
	i2c_start( i2c );
	i2c_write( i2c, HMC6352_ID_WRITE);
	i2c_write( i2c, 'r');
	i2c_write( i2c, addr );
	i2c_stop( i2c );

	// Do the read
	i2c_start( i2c );
	i2c_write( i2c, HMC6352_ID_READ );
	read_val = i2c_read( i2c, 0 ); // do not send an ack
	i2c_stop( i2c );

	return read_val;
}

int read_RAM( i2c_p &i2c, unsigned char addr )
{
	int read_val;

	// Tell device we want to write.
	i2c_start( i2c );
	i2c_write( i2c, HMC6352_ID_WRITE);
	i2c_write( i2c, 'g');
	i2c_write( i2c, addr );
	i2c_stop( i2c );

	// Tell device we want to read.
	i2c_start( i2c );
	i2c_write( i2c, HMC6352_ID_READ );
	read_val = i2c_read( i2c, 0 ); // do not send an ack
	i2c_stop( i2c );

	return read_val;
}
