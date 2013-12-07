/*
 * director.xc
 *
 * A breadth first search algorithm
 *
 *  Created on: May 17, 2012
 *      Author: Joseph Lewis <joehms22@gmail.com>
 */
#include "director.h"
#include "bfs.h"
#include "print.h"
#include <stdio.h>
#include "assert.h"

int direction_from_to(int curr_loc, int next_loc);


enum cardinal_directions
{
	north = 'n', south = 's', east = 'e', west = 'w'
};


// Outputs "direction" types
void directions_thread(chanend direction_output, int start_rank, int goal_rank, const int obstacles[])
{
	direction curr_dir;
	int next, curr;
	int last_direction = north, curr_direction;

	// Setup the search
	init_path(start_rank, goal_rank, obstacles);

	// clear the vars
	curr_dir.command = 0;
	curr_dir.param = 0;

	// Keep sending directions until all out
	next = next_rank();
	while(has_next())
	{
		curr = next;
		next = next_rank();

		curr_direction = direction_from_to(curr, next);

		curr_dir.param++;
		if(curr_direction == last_direction)
			continue;


		// we changed directions, must push commands and rotate!
		// go straight n positions
		curr_dir.command = forward;
		direction_output <: curr_dir;
		curr_dir.param = 0;

		// rotate!

		if(	curr_direction == north && last_direction == west ||
			curr_direction == east && last_direction == north ||
			curr_direction == south && last_direction == east ||
			curr_direction == west && last_direction == south )
			curr_dir.command = right_ninety;
		else
			curr_dir.command = left_ninety;
		direction_output <: curr_dir;

		last_direction = curr_direction;
	}

	// Write the final one.
	curr_dir.command = forward;
	direction_output <: curr_dir;

	// Buffer with completed directions
	while(1)
	{
		curr_dir.command = stop;
		direction_output <: curr_dir;
	}
}


int direction_from_to(int curr_loc, int next_loc)
{
	if( COL(curr_loc) + 1 == COL(next_loc))
		return east;
	if( COL(curr_loc) - 1  == COL(next_loc))
		return west;
	if( ROW(curr_loc) == ROW(next_loc) - 1)
		return south;
	if( ROW(curr_loc) == ROW(next_loc) + 1)
		return north;
}


void director_test( chanend direction_input)
{
	direction curr_dir;
	char output[64];

	// do simple tests
	assert(direction_from_to(RANK(0,0), RANK(0,1)) == east);
	assert(direction_from_to(RANK(0,1), RANK(0,0))  == west);
	assert(direction_from_to(RANK(0,0), RANK(1,0)) == south);
	assert(direction_from_to(RANK(1,0), RANK(0,0)) == north);


	// do complex tests
	do
	{
		direction_input :> curr_dir;
		switch(curr_dir.command)
		{
		case stop:
				printstrln("STOP");
			break;

		case forward:
				sprintf(output, "Forward %i", curr_dir.param);
				printstrln(output);
			break;

		case left_ninety:
				printstrln("Left 90*");
			break;

		case right_ninety:
				printstrln("Right 90*");
			break;
		}
	}while(curr_dir.command != stop);
}
