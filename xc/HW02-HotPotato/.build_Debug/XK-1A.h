#ifndef HAVE_PLATFORM_H
#define HAVE_PLATFORM_H

#include <xs1.h>

/*
 * Platform description header file.
 * Automatically generated from ".././XK-1A.xn".
 */

#ifdef __XC__
/* Core array declaration. */
extern core stdcore[1];
#endif

#ifdef __XC__
/* Service prototypes. */
/* none */
#endif

#if !defined(__ASSEMBLER__)
#define PORT_UART_RX on stdcore[0]: XS1_PORT_1I
#define PORT_UART_TX on stdcore[0]: XS1_PORT_1J
#define PORT_BUT_1 on stdcore[0]: XS1_PORT_1K
#define PORT_BUT_2 on stdcore[0]: XS1_PORT_1L
#define PORT_SPI_MISO on stdcore[0]: XS1_PORT_1M
#define PORT_SPI_SS on stdcore[0]: XS1_PORT_1N
#define PORT_SPI_CLK on stdcore[0]: XS1_PORT_1O
#define PORT_SPI_MOSI on stdcore[0]: XS1_PORT_1P
#define PORT_LED on stdcore[0]: XS1_PORT_4F
#else
#define PORT_UART_RX XS1_PORT_1I
#define PORT_UART_TX XS1_PORT_1J
#define PORT_BUT_1 XS1_PORT_1K
#define PORT_BUT_2 XS1_PORT_1L
#define PORT_SPI_MISO XS1_PORT_1M
#define PORT_SPI_SS XS1_PORT_1N
#define PORT_SPI_CLK XS1_PORT_1O
#define PORT_SPI_MOSI XS1_PORT_1P
#define PORT_LED XS1_PORT_4F
#endif


/* Reference frequency definition. */
#define PLATFORM_REFERENCE_HZ 100000000
#define PLATFORM_REFERENCE_KHZ 100000
#define PLATFORM_REFERENCE_MHZ 100

#endif /* HAVE_PLATFORM_H */

