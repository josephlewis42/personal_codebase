/*
 * bfs.h - Not to be confused with BFF
 *
 *  Created on: May 17, 2012
 *      Author: Joseph Lewis <joehms22@gmail.com>
 */

#ifndef BFS_H_
#define BFS_H_

#include <xs1.h>
#include "platform.h"

#define MAZE_WIDTH 6
# define ELEMENT_COUNT (MAZE_WIDTH * MAZE_WIDTH)
# define RANK(row, col) ((row) * MAZE_WIDTH + (col))
# define ROW(rank) ((rank) / MAZE_WIDTH)
# define COL(rank) ((rank) % MAZE_WIDTH)

int init_path(int start_rank, int goal_rank, const int obstacles[]);
int next_rank();
int has_next();


int test_bfs();


#endif /* BFS_H_ */
