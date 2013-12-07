// includes
#include <xs1.h>
#include <print.h>
#include <string.h>
#include "platform.h"

// constants
const unsigned int BAUDRATE = 115200; //57600;

// ports
out port oUartTx = PORT_UART_TX; // this will send the messaging over the UART line

// prototypes
int main_array();
int main_single();
void uart_transmit_bytes(out port oPort, const char values[], unsigned int n, unsigned int baudrate);
void uart_transmit_byte(out port oPort, char value, unsigned int baudrate);


void debug(const char values[], unsigned int n)
{
	uart_transmit_bytes(oUartTx,values, n, BAUDRATE);
}

void uart_transmit_bytes(out port oPort, const char values[], unsigned int n, unsigned int baudrate)
{
	unsigned int i = 0;
	for(int i=0; i<n; i++){
		uart_transmit_byte(oPort, values[i], baudrate);
	}
}

void uart_transmit_byte(out port oPort, char value, unsigned int baudrate)
{
	timer tmr;
	unsigned int t, j;
	const unsigned int bit_time = XS1_TIMER_HZ / baudrate;
	unsigned int byte = value;

	tmr :> t; // timestamp

	// Output the start bit
	oPort <: 0;
	t += bit_time; tmr when timerafter(t) :> void;

	// Output data bits
	for(j=0; j<8; j++){
		oPort <: (byte & 0x1);
		byte >>= 1;
		t += bit_time; tmr when timerafter(t) :> void;
     }

     // Output the Stop Bit
     oPort <: 1;
     t += bit_time; tmr when timerafter(t) :> void;
}
