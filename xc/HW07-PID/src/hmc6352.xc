// includes
#include "hmc6352.h"

// constants
#define TICKS_PER_MS (XS1_TIMER_HZ/1000)
#define TICKS_PER_MICRO (XS1_TIMER_HZ/1000000)

#define HMC6352_ID_WRITE 0x42
#define HMC6352_ID_READ 0x43

#define HMC6352_GET_HEADING_CMD 0x41
#define HMC6352_GET_HEADING_DELAY (6000*TICKS_PER_MICRO)

#define HMC6352_READ_EEPROM_CMD 0x72
#define HMC6352_READ_EEPROM_DELAY (70*TICKS_PER_MICRO)

#define HMC6352_READ_RAM_CMD 0x67
#define HMC6352_READ_RAM_DELAY (70*TICKS_PER_MICRO)

#define HMC6352_START_USER_CALIBRATION_CMD 0x43
#define HMC6352_START_USER_CALIBRATION_DELAY (10*TICKS_PER_MICRO)

#define HMC6352_STOP_USER_CALIBRATION_CMD 0x45
#define HMC6352_STOP_USER_CALIBRATION_DELAY (14000*TICKS_PER_MICRO)

#define HMC6352_WRITE_EEPROM_CMD 0x77
#define HMC6352_WRITE_EEPROM_DELAY (70*TICKS_PER_MICRO)

#define HMC6352_WRITE_RAM_CMD 0x47
#define HMC6352_WRITE_RAM_DELAY (70*TICKS_PER_MICRO)

unsigned int hmc6352_get_heading_tenth_degrees(i2c_p& i2c)
{
	timer tmr;
	unsigned int t;
	unsigned int value;

	i2c_start(i2c);
	i2c_write(i2c, HMC6352_ID_WRITE);
	i2c_write(i2c, HMC6352_GET_HEADING_CMD);
	i2c_stop(i2c);

	// wait appropriate amout of time for the command
	tmr :> t; tmr when timerafter(t += HMC6352_GET_HEADING_DELAY) :> void;

	// read Response
	i2c_start(i2c);
	i2c_write(i2c, HMC6352_ID_READ);
	value = (i2c_read(i2c, 1) << 8);
	value |= i2c_read(i2c, 0);
	i2c_stop(i2c);

	return value;
}


unsigned int hmc6352_get_heading_degrees(i2c_p& i2c)
{
	return hmc6352_get_heading_tenth_degrees(i2c)/10;
}

unsigned char hmc6352_read_eeprom( i2c_p& i2c, hmc6352_eeprom_address_t eeprom_address)
{
	timer tmr;
	unsigned int t;
	unsigned char value;

	i2c_start(i2c);
	i2c_write(i2c, HMC6352_ID_WRITE);
	i2c_write(i2c, HMC6352_READ_EEPROM_CMD);
	i2c_write(i2c, eeprom_address);
	i2c_stop(i2c);

	// wait appropriate amout of time for the command
	tmr :> t; tmr when timerafter(t += HMC6352_READ_EEPROM_DELAY) :> void;

	// read Response
	i2c_start(i2c);
	i2c_write(i2c, HMC6352_ID_READ);
	value = i2c_read(i2c, 0);
	i2c_stop(i2c);

	return value;
}

unsigned char hmc6352_read_ram(i2c_p& i2c, unsigned char ram_address)
{
	timer tmr;
	unsigned int t;
	unsigned char value;

	i2c_start(i2c);
	i2c_write(i2c, HMC6352_ID_WRITE);
	i2c_write(i2c, HMC6352_READ_RAM_CMD);
	i2c_write(i2c, ram_address);
	i2c_stop(i2c);

	// wait appropriate amout of time for the command
	tmr :> t;
	t += HMC6352_READ_RAM_DELAY;
	tmr when timerafter(t) :> void;

	// read Response
	i2c_start(i2c);
	i2c_write(i2c, HMC6352_ID_READ);
	value = i2c_read(i2c, 0);
	i2c_stop(i2c);

	return value;
}

void hmc6352_start_user_calibration(i2c_p& i2c)
{
	timer tmr;
	unsigned int t;

	i2c_start(i2c);
	i2c_write(i2c, HMC6352_ID_WRITE);
	i2c_write(i2c, HMC6352_START_USER_CALIBRATION_CMD);
	i2c_stop(i2c);

	// wait appropriate amout of time for the command to finish
	tmr :> t;
	t += HMC6352_START_USER_CALIBRATION_DELAY;
	tmr when timerafter(t) :> void;
}

void hmc6352_stop_user_calibration(i2c_p& i2c)
{
	timer tmr;
	unsigned int t;

	i2c_start(i2c);
	i2c_write(i2c, HMC6352_ID_WRITE);
	i2c_write(i2c, HMC6352_STOP_USER_CALIBRATION_CMD);
	i2c_stop(i2c);

	// wait appropriate amout of time for the command to finish
	tmr :> t;
	t += HMC6352_STOP_USER_CALIBRATION_DELAY;
	tmr when timerafter(t) :> void;
}

void hmc6352_write_eeprom(i2c_p& i2c, hmc6352_eeprom_address_t eeprom_address, unsigned char value)
{
	timer tmr;
	unsigned int t;

	i2c_start(i2c);
	i2c_write(i2c, HMC6352_ID_WRITE);
	i2c_write(i2c, HMC6352_WRITE_EEPROM_CMD);
	i2c_write(i2c, eeprom_address);
	i2c_write(i2c, value);
	i2c_stop(i2c);

	// wait appropriate amout of time for the command to finish
	tmr :> t;
	t += HMC6352_WRITE_EEPROM_DELAY;
	tmr when timerafter(t) :> void;
}

void hmc6352_write_ram(i2c_p& i2c, unsigned char ram_address, unsigned char value)
{
	timer tmr;
	unsigned int t;

	i2c_start(i2c);
	i2c_write(i2c, HMC6352_ID_WRITE);
	i2c_write(i2c, HMC6352_WRITE_RAM_CMD);
	i2c_write(i2c, ram_address);
	i2c_write(i2c, value);
	i2c_stop(i2c);

	// wait appropriate amout of time for the command to finish
	tmr :> t;
	t += HMC6352_WRITE_RAM_DELAY;
	tmr when timerafter(t) :> void;
}
