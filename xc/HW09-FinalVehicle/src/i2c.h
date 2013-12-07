#ifndef I2C_H_INCLUDED
#define I2C_H_INCLUDED

#include <xs1.h>
typedef struct
{
	port scl; // clock port
	port sda; // data port
	unsigned t; // timestamp
	timer tmr; // timer
	unsigned delay; // delay on clock edges (in ticks)
} i2c_p;

void i2c_delay(i2c_p &i2c); // delays by i2c_p.delay ticks
void i2c_init(i2c_p &i2c); // sets the initial state on the SCL and SDA lines
void i2c_start(i2c_p &i2c); // sends the start bit sequence
void i2c_stop(i2c_p &i2c); // sends the stop bit sequence
int i2c_read(i2c_p &i2c, int ack); // reads a byte from the slave, the 'ack' flag determines if a master->slave is sent.  This should be 1 after bytes in the middle of a multi-byte response, 0 otherwise
int i2c_write(i2c_p &i2c, unsigned data); // writes a byte to the slave.

#endif
