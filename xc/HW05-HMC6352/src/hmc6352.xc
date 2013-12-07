/** Joseph Lewis **/
// includes
#include "hmc6352.h"
#include <xs1.h>
#include "servos.h"


// defines
#define HMC6352_ID_WRITE 0x42
#define HMC6352_ID_READ 0x43
#define HMC6352_READ_EEPROM 0x72
#define TICKS_PER_MS (XS1_TIMER_HZ/1000)
#define TICKS_PER_S XS1_TIMER_HZ
#define TICKS_PER_US (XS1_TIMER_HZ/1000000)


//
const unsigned char HMC6352_SLAVE_ADDRESS = (char) 0x00;
const unsigned char HMC6352_MAGNETOMETER_X_OFFSET_MSB = (char) 0x01;
const unsigned char HMC6352_MAGNETOMETER_X_OFFSET_LSB = (char) 0x02;
const unsigned char HMC6352_MAGNETOMETER_Y_OFFSET_MSB = (char) 0x03;
const unsigned char HMC6352_MAGNETOMETER_Y_OFFSET_LSB = (char) 0x04;
const unsigned char HMC6352_TIME_DELAY_MS = (char) 0x05;
const unsigned char HMC6352_NUM_SUMMED_MEASUREMENTS = (char) 0x06;
const unsigned char HMC6352_SOFTWARE_VERSION = (char) 0x07;
const unsigned char HMC6352_OPERATION_MODE = (char) 0x08;

// ports
unsigned char hmc6352_read_eeprom( i2c_p& i2c, unsigned char addr )
{
	unsigned char read_val;
	unsigned int t;
	timer tmr;

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

	// Delay so we don't overclock the whole thing
	tmr :> t;
	tmr when timerafter(t + 100 * TICKS_PER_MS) :> void;

	return read_val;
}


void hmc6352_write_eeprom(i2c_p& i2c, unsigned char eeprom_address, unsigned char value)
{
	// Tell device we want to read.
	i2c_start( i2c );
	i2c_write( i2c, HMC6352_ID_WRITE);
	i2c_write( i2c, 'w');
	i2c_write( i2c, eeprom_address );
	i2c_write( i2c, value );
	i2c_stop( i2c );
}




unsigned char hmc6352_read_ram( i2c_p& i2c, unsigned char addr )
{
	unsigned char read_val;
	unsigned int t;
	timer tmr;

	// Tell device we want to read.
	i2c_start( i2c );
	i2c_write( i2c, HMC6352_ID_WRITE);
	i2c_write( i2c, 'g'); // read from ram
	i2c_write( i2c, addr );
	i2c_stop( i2c );

	// Do the read
	i2c_start( i2c );
	i2c_write( i2c, HMC6352_ID_READ );
	read_val = i2c_read( i2c, 0 ); // do not send an ack
	i2c_stop( i2c );

	// Delay so we don't overclock the whole thing
	tmr :> t;
	tmr when timerafter(t + 100 * TICKS_PER_MS) :> void;

	return read_val;
}


void hmc6352_write_ram(i2c_p& i2c, unsigned char addr, unsigned char value)
{
	// Tell device we want to read.
	i2c_start( i2c );
	i2c_write( i2c, HMC6352_ID_WRITE);
	i2c_write( i2c, 'G'); // Write to RAM
	i2c_write( i2c, addr );
	i2c_write( i2c, value );
	i2c_stop( i2c );
}


void hmc6352_start_user_calibration(i2c_p& i2c)
{
	timer tmr;
	unsigned int t;

	// Tell device we want to start calibration
	i2c_start( i2c );
	i2c_write( i2c, HMC6352_ID_WRITE);
	i2c_write( i2c, 'C');
	i2c_stop( i2c );

	// Wait for calibration to be ready
	tmr :> t;
	tmr when timerafter(t + (TICKS_PER_US * 10)) :> void;
}

void hmc6352_stop_user_calibration(i2c_p& i2c)
{
	timer tmr;
	unsigned int t;

	// Tell device to stop calibration mode.
	i2c_start( i2c );
	i2c_write( i2c, HMC6352_ID_WRITE);
	i2c_write( i2c, 'E');
	i2c_stop( i2c );

	// Wait time for calculation.
	tmr :> t;
	tmr when timerafter(t + (TICKS_PER_US  * 14000)) :> void;
}

unsigned int hmc6352_get_heading_degrees(i2c_p& i2c)
{
	unsigned int total = 0;
	unsigned char msb, lsb;

	// Tell device we want to read a heading
	i2c_start( i2c );
	i2c_write( i2c, HMC6352_ID_WRITE);
	i2c_write( i2c, 'A'); // read a heading
	i2c_stop( i2c );

	// Do the read
	i2c_start( i2c );
	i2c_write( i2c, HMC6352_ID_READ );
	msb = i2c_read( i2c, 1 ); // send an ack
	lsb = i2c_read( i2c, 0 ); // do not send an ack
	i2c_stop( i2c );

	total = msb;
	total <<= 8;
	total += lsb;

	return total / 10;

}


void hmc6352_calibrate_compass(i2c_p& i2c)
{

	// Start calibration
	hmc6352_start_user_calibration(i2c);

	// Rotate vehicle for the proper amount of time
	// Left for sixty seconds
	left_forward(11);
	//right_stop();
	servo_task(30 * TICKS_PER_S);
	// Right for sixty seconds
	right_forward(11);
	left_stop();
	servo_task(30 * TICKS_PER_S);

	// Stop calibration
	hmc6352_stop_user_calibration(i2c);
}
