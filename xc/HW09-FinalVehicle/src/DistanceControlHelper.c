#include "DistanceControlHelper.h"

float find_velocity_mm_per_ms(int width)
{
	return -.0000009948052591 * width * width + .00367823322 * width - 3.246861274;
}

int find_pulse_duration_ms(int width, int dist_mm)
{
	return (int) ((float) dist_mm / find_velocity_mm_per_ms(width));
}
