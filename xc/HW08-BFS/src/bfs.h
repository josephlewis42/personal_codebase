/*
 * bfs.h
 *
 *  Created on: May 17, 2012
 *      Author: Joseph Lewis <joehms22@gmail.com>
 */

#ifndef BFS_H_
#define BFS_H_


# define MAZE_WIDTH 10
# define ELEMENT_COUNT (MAZE_WIDTH * MAZE_WIDTH)
# define RANK(row, col) ((row) * MAZE_WIDTH + (col))
# define ROW(rank) ((rank) / MAZE_WIDTH)
# define COL(rank) ((rank) % MAZE_WIDTH)


int test_main();

void find_shortest_path(int start_rank, int goal_rank, const int obstacles[]);

#endif /* BFS_H_ */
