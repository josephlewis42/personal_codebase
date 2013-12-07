
#include <xs1.h>
#include <xclib.h>
#include "i2c.h"

void i2c_delay(i2c_p &i2c)
{
	i2c.t += i2c.delay;
	i2c.tmr when timerafter(i2c.t) :> void;
}

void i2c_init(i2c_p &i2c)
{
	i2c.sda <: 1;
	i2c.scl <: 1;
}

void i2c_start(i2c_p &i2c)
{
	i2c.tmr :> i2c.t;
	i2c.sda <: 0;
	i2c_delay(i2c);
	i2c.scl <: 0;
}

void i2c_stop(i2c_p &i2c)
{
	i2c.sda <: 0;
	i2c_delay(i2c);
	i2c.scl <: 1;
	i2c_delay(i2c);
	i2c.sda <: 1;
	i2c_delay(i2c);
	i2c_delay(i2c);
}

int i2c_read(i2c_p &i2c, int ack)
{
	int data = 0;
	for(int i = 0; i < 8; i++)
	{
		i2c.sda :> void;
		i2c_delay(i2c);
		i2c.scl <: 1;
		i2c.scl when pinseq(1) :> void;
		i2c.sda :> >> data;
		i2c_delay(i2c);
		i2c.scl <: 0;
	}
	i2c.sda <: !ack;
	i2c_delay(i2c);
	i2c.scl <: 1;
	i2c.scl when pinseq(1) :> void;
	i2c_delay(i2c);
	i2c.scl <: 0;
	return bitrev(data);
}

int i2c_write(i2c_p &i2c, unsigned data)
{
	int ack;
	data = byterev(bitrev(data));
	for(int i = 0; i < 8; i++)
	{
		i2c.sda <: >> data;
		i2c_delay(i2c);
		i2c.scl <: 1;
		i2c.scl when pinseq(1) :> void;
		i2c_delay(i2c);
		i2c.scl <: 0;
	}
	i2c.sda :> void;
	i2c_delay(i2c);
	i2c.scl <: 1;
	i2c.scl when pinseq(1) :> void;
	i2c.sda :> ack;
	i2c_delay(i2c);
	i2c.scl <: 0;
	return !ack;
}
