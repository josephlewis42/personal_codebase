#ifndef UTILITY_H_
#define UTILITY_H_

#include <xs1.h>

#define TICKS_PER_US (XS1_TIMER_HZ/1000000)
#define TICKS_PER_MS (XS1_TIMER_HZ/1000)
#define TICKS_PER_SEC (XS1_TIMER_HZ)

#define MIN(x,y) (x > y ? y : x)
#define MAX(x,y) (x > y ? x : y)

#endif /* UTILITY_H_ */
