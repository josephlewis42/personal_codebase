/**
	Copyright 2012 Joseph Lewis <joehms22@gmail.com>
**/

// includes
#include <xs1.h>
#include <stdlib.h>
#include <stdio.h>
#include <print.h>
#include "platform.h"
#include "hmc6352.h"

#include "servos.h"

// defines
#define TICKS_PER_S XS1_TIMER_HZ
#define TICKS_PER_MS (XS1_TIMER_HZ/1000)
#define TICKS_PER_US (XS1_TIMER_HZ/1000000)
#define TIMER_MAX_VALUE 0x7FFFFFFF

// ports
in port set_heading = PORT_BUT_1;

// prototypes
void test_hmc6352_read_eeprom();
void test_hmc6352_write_eeprom();
void test_hmc6352_read_ram();
void test_hmc6352_write_ram();
void test_hmc6352_get_heading_degrees();
void test_compass_calibration();


i2c_p i2c = {
	XS1_PORT_1A, 	// s c l
	XS1_PORT_1B, 	// sda
	0, 				// t
	0,				// tmr
	10000			// delay
};



int main(void)
{
	i2c_init( i2c );

	// CALIBRATION MODE NEED TO PRESS BUTTON FOR IT TO WORK.
	//test_compass_calibration();


	// EEPROM Read Test
	test_hmc6352_read_eeprom();
	//test_hmc6352_write_eeprom();

	// RAM TEST
	//test_hmc6352_write_ram();
	//test_hmc6352_read_ram();
/**
	hmc6352_write_eeprom( i2c, HMC6352_MAGNETOMETER_X_OFFSET_MSB, 0);
	hmc6352_write_eeprom( i2c, HMC6352_MAGNETOMETER_X_OFFSET_LSB, 0);
	hmc6352_write_eeprom( i2c, HMC6352_MAGNETOMETER_Y_OFFSET_MSB, 0);
	hmc6352_write_eeprom( i2c, HMC6352_MAGNETOMETER_Y_OFFSET_LSB, 0);

	//hmc6352_write_eeprom( i2c, HMC6352_TIME_DELAY_MS );
	//	hmc6352_write_eeprom( i2c, HMC6352_NUM_SUMMED_MEASUREMENTS, 1);
	hmc6352_write_eeprom( i2c, HMC6352_OPERATION_MODE, 4);
	hmc6352_write_eeprom( i2c, HMC6352_OPERATION_MODE, 0x50);

	test_hmc6352_read_eeprom();
**/

	test_compass_calibration();

	test_hmc6352_get_heading_degrees();


	return 0;
}



void test_hmc6352_read_eeprom()
{
	unsigned char ret_val;
	char buff[64];

	ret_val = hmc6352_read_eeprom( i2c, HMC6352_SLAVE_ADDRESS );
	sprintf(buff, "Slave Address: 0x%x", ret_val);
	printstrln(buff);

	ret_val = hmc6352_read_eeprom( i2c, HMC6352_MAGNETOMETER_X_OFFSET_MSB );
	sprintf(buff, "Magnetometer X Offset MSB: %i", ret_val);
	printstrln(buff);

	ret_val = hmc6352_read_eeprom( i2c, HMC6352_MAGNETOMETER_X_OFFSET_LSB);
	sprintf(buff, "Magnetometer X Offset LSB: %i", ret_val);
	printstrln(buff);

	ret_val = hmc6352_read_eeprom( i2c, HMC6352_MAGNETOMETER_Y_OFFSET_MSB );
	sprintf(buff, "Magnetometer Y Offset MSB: %i", ret_val);
	printstrln(buff);

	ret_val = hmc6352_read_eeprom( i2c, HMC6352_MAGNETOMETER_Y_OFFSET_LSB);
	sprintf(buff, "Magnetometer Y Offset LSB: %i", ret_val);
	printstrln(buff);

	ret_val = hmc6352_read_eeprom( i2c, HMC6352_TIME_DELAY_MS );
	sprintf(buff, "Time Delay (ms): %i", ret_val);
	printstrln(buff);

	ret_val = hmc6352_read_eeprom( i2c, HMC6352_NUM_SUMMED_MEASUREMENTS);
	sprintf(buff, "Number of Summed measurements(1-16): %i", ret_val);
	printstrln(buff);


	ret_val = hmc6352_read_eeprom( i2c, HMC6352_SOFTWARE_VERSION);
	sprintf(buff, "Software Version Number ( >1 ): %i", ret_val);
	printstrln(buff);

	ret_val = hmc6352_read_eeprom( i2c, HMC6352_OPERATION_MODE);
	sprintf(buff, "Operation Mode Byte ( DEFAULT: 50 ): 0x%x", ret_val);
	printstrln(buff);

}


void test_hmc6352_write_eeprom()
{
	unsigned char ret_val;
	char buff[64];

	hmc6352_write_eeprom(i2c, HMC6352_NUM_SUMMED_MEASUREMENTS, 1);

	ret_val = hmc6352_read_eeprom( i2c, HMC6352_NUM_SUMMED_MEASUREMENTS);
	sprintf(buff, "Number of Summed measurements(1-16): %i", ret_val);
	printstrln(buff);

	hmc6352_write_eeprom(i2c, HMC6352_NUM_SUMMED_MEASUREMENTS, 0x04); // revert to factory default

	ret_val = hmc6352_read_eeprom( i2c, HMC6352_NUM_SUMMED_MEASUREMENTS);
	sprintf(buff, "Number of Summed measurements(1-16): %i", ret_val);
	printstrln(buff);
}

void test_hmc6352_write_ram()
{
	unsigned char orig_val;
	unsigned char ret_val;
	unsigned char ADDR = 0x4E;
	char buff[64];

	orig_val = hmc6352_read_ram( i2c, ADDR );
	sprintf(buff, "Ram is originally: %i", orig_val);
	printstrln(buff);

	hmc6352_write_ram(i2c, ADDR, 0x04); // change

	ret_val = hmc6352_read_ram( i2c, ADDR);
	sprintf(buff, "Ram is now: %i\nReverting...", ret_val);
	printstrln(buff);

	hmc6352_write_ram(i2c, ADDR, orig_val); // revert to original
}

void test_hmc6352_read_ram()
{
	unsigned char read_val;
	char buff[64];

	for(int i = 0x00; i < 0xFF; i++)
	{
		read_val = hmc6352_read_ram( i2c, i );

		sprintf(buff, "%2x|",  read_val);
		if(i % 10 == 9)
			printstrln(buff);
		else
			printstr(buff);
	}
}

void test_compass_calibration()
{
	timer tmr;
	unsigned int t;

	// Wait for the start_signal to go on
	set_heading when pinseq(0) :> void;

	// Wait for 2 seconds for area to clear
	tmr :> t;
	tmr when timerafter(t + TICKS_PER_S * 2) :> void;
	hmc6352_calibrate_compass(i2c);
}

void test_hmc6352_get_heading_degrees()
{
	unsigned int heading;
	char buff[64];


	while(1)
	{
		heading = hmc6352_get_heading_degrees(i2c);
		sprintf(buff, "Heading: %u", heading);
		printstrln(buff);
	}


}

