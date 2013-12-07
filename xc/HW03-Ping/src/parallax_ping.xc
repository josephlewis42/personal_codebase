#include <xs1.h>

#define TICKS_PER_SEC XS1_TIMER_HZ
#define TICKS_PER_MICRO (XS1_TIMER_HZ/1000000)

// Parallax PING (p/n 28015) sensor providing the pulse width etc.
void ping_simulator(port prt, const unsigned int mms[], unsigned int n_mms, unsigned int mm_per_second)
{
	timer tmr;
	unsigned int i, t, ticks;

	for(i=0; i<n_mms; ++i){
		// factor of two is because the sound waves have to
		// travel both directions.
		ticks = 2 * mms[i] * (TICKS_PER_SEC / mm_per_second);

		// wait for the high trigger pulse from the host
		prt when pinseq(1) :> void;

		// wait for the low and timestamp
		prt when pinseq(0) :> void;
		tmr :> t;

		// wait the 750 us T_holdoff period
		t += 750*TICKS_PER_MICRO;
		tmr when timerafter(t) :> void;

		// start the returned pulse
		prt <: 1;

		// wait the specified amount of time
		t += ticks;
		tmr when timerafter(t) :> void;

		// go low
		prt <: 0;
	}
}
