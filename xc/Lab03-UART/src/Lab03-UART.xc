/**
	Copyright 2012 Joseph Lewis <joehms22@gmail.com>
**/

// includes
#include <xs1.h>
#include <stdlib.h>
#include <stdio.h>
#include <print.h>
#include "platform.h"
#include <string.h>

// defines
#define TICKS_PER_SEC XS1_TIMER_HZ
#define TICKS_PER_MS (XS1_TIMER_HZ/1000)
#define TICKS_PER_MICRO (XS1_TIMER_HZ/1000000)
#define TIMER_MAX_VALUE 0x7FFFFFFF
#define DEBUG
#define BAUDRATE 96000

// ports
in port iUartRx = PORT_UART_RX;
out port oUartTx = PORT_UART_TX;

// prototypes
void uart_transmit_byte(out port oPort, char value, unsigned int baudrate);
char uart_receive_byte(in port iPort, unsigned int baudrate);
int main_single();
int main_array();

void uart_transmit_bytes(out port oPort, const char values[], unsigned int n, unsigned int baudrate);
void uart_receive_bytes(in port iPort, char values[], unsigned int n, unsigned int baudrate);



int main(void)
{
	main_array();
	return main_single();
}

int main_single()
{
	char value;
	oUartTx <: 1; // helps with the simulator.

	par
	{
		uart_transmit_byte(oUartTx, 'H', BAUDRATE);
		value = uart_receive_byte(iUartRx, BAUDRATE);
	}

	printcharln(value);

	return 0;
}

int main_array()
{
	const char message[] = "Hello, Cleveland.";
	char buffer[64];
	oUartTx <: 1;
	par
	{
		uart_transmit_bytes(oUartTx, message, (strlen(message)+1),BAUDRATE);
		uart_receive_bytes(iUartRx, buffer, (strlen(message)+1), BAUDRATE);
	}

	printstrln(buffer);
	return 0;
}



unsigned int compute_delay_ticks(unsigned int t0, unsigned int t1)
{
	if(t1 > t0)
		return t1-t0;

	return (TIMER_MAX_VALUE - t0) + t1;
}



void toggle_port(out port oPort, unsigned int count,
				unsigned int hz, unsigned int pattern)
{
	unsigned int i,t;
	const unsigned int half_period = XS1_TIMER_HZ / (2*hz);
	timer tmr;

	tmr :> t;
	for(i = 0; i < 2*count; i++)
	{
		oPort <: pattern;

		t += half_period;
		tmr when timerafter(t) :> void;

		pattern = ~pattern;
	}
}



void uart_transmit_byte(out port oPort, char value, unsigned int baudrate)
{
	unsigned int bit_time = 100000000 / baudrate;
	timer t;
	unsigned int time;

	t :> time;

	/** output start bit **/
	oPort <: 0;
	time += bit_time;
	t when timerafter(time) :> void;

	/** output data bits **/
	for( int i = 0; i < 8; ++i)
	{
		oPort <: >> value;
		time += bit_time;
		t when timerafter(time) :> void;
	}

	/** output stop bit **/
	oPort <: 1;
	time += bit_time;
	t when timerafter(time) :> void;

}

char uart_receive_byte(in port iPort, unsigned int baudrate)
{
	unsigned int bit_time = 100000000 / baudrate;
	unsigned int time;
	timer t;
	char value;

	/** wait for start bit **/
	iPort when pinseq(0) :> void;
	t :> time;
	time += bit_time / 2;

	/** input data bits **/
	for( int i = 0; i < 8; i++) {
		time += bit_time;
		t when timerafter(time) :> void;
		iPort :> >> value;
	}

	/** input stop bit **/
	time += bit_time;
	t when timerafter(time) :> void;
	return value;

}


void uart_transmit_bytes(out port oPort, const char values[], unsigned int n, unsigned int baudrate)
{
	for(int i = 0; i < n; i++)
	{
		uart_transmit_byte(oPort, values[i], baudrate);
	}
}


void uart_receive_bytes(in port iPort, char values[], unsigned int n, unsigned int baudrate)
{
	for(int i = 0; i < n; i++)
	{
		values[i] = uart_receive_byte(iPort, baudrate);
	}
}
