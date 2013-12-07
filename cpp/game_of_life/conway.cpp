 /**
  * 
  * Copyright 2012-01-15 Joseph Lewis <joehms22@gmail.com>
  * 
  * Conway's game of life in cpp. The world is looped (life at top can 
  * move to bottom &c.)
  * 
  * Apache 2.0 License
  * 
  */
#include <iostream>
#include <cstdlib>
#include <ctime>
#include <time.h>

using namespace std;

const int COLS = 80;
const int ROWS = 23;

bool alive [ROWS][COLS];
int num [ROWS][COLS];

int boardnum = 0; // number of boards run by the game
int iteration = 0; // current round in the current board

int numberAround(int row, int col);

/**
 * Sets the numbers array to all 0s
 */
void blank_num()
{
	for(int i = 0; i < ROWS; i++)
		for(int j = 0; j < COLS; j++)
			num[i][j] = 0;
}

/**
 * Sets the alive array to all falses.
 */
void blank_alive()
{
	for(int i = 0; i < ROWS; i++)
		for(int j = 0; j < COLS; j++)
			alive[i][j] = false;
}

/**
 * Inits the alive array with the simplest gosper gun known to man 
 * (so far)
 */
void gosper_gun()
{
	blank_alive();
	bool gosper [10][38] =
	{//  1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6
		{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}, //0
		{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0}, 
		{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0}, 
		{0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0}, //3
		{0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0}, 
		{0,1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}, 
		{0,1,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0}, //6
		{0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0}, 
		{0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0},
		{0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}  //9
	};
	
	for(int r = 0; r < 10; r ++)
		for(int c = 0; c < 38; c ++)
			alive[r][c] = gosper[r][c];
}

/**
 * Writes output to the console.
 */
void do_output()
{
	cout << "\nBoard: "<< boardnum << " Iteration: " << iteration << "\n";

	for(int i = 0; i < ROWS; i++)
	{

		for(int j = 0; j < COLS; j++)
		{
			// WIDTH, HEIGHT
			if(alive[i][j])
				cout << "0";
			else
				cout << " ";
		}
		if(i != ROWS -1)
			cout <<"\n";
		else
			cout << flush;
	}

}

/**
 * Randomly fills the grid with alive cells after blanking.
 */
void random_fill()
{
	blank_alive();
	srand(time(0));
	
	// Fill 30% of the cells
	int numToFill = (ROWS * COLS) * 30 / 100 ;
	
	for(int r = 0; r < numToFill; r ++)
	{
		int row = rand() % ROWS;
		int col = rand() % COLS;
		
		alive[row][col] = true;
	}
}

/**
 * Returns the index of the row below the current one.
 */
int rowBelow(int row)
{
	return (row + 1 < ROWS) ? row + 1 : 0;
}

/**
 * Returns the index of the row above the given one
 */
int rowAbove(int row)
{
	return (row > 0) ? row - 1 : ROWS - 1;
}

/** Returns the index of the col to the right of this one */
int colRight(int col)
{
	return (col + 1 < COLS) ? col + 1 : 0;
}

/** Returns the index of the col to the left of this one */
int colLeft(int col)
{
	return (col > 0) ? col - 1 : COLS -1;
}

/** true if the cell to the left is alive*/
bool left(int row, int col)
{
	col = colLeft(col);
	return alive[row][col];
}

/** true if the cell to the right is alive*/
bool right(int row, int col)
{
	col = colRight(col);
	return alive[row][col];
}

/** true if the cell above is alive*/
bool above(int row, int col)
{
	row = rowAbove(row);
	return alive[row][col];
}

/** true if the cell below is alive*/
bool below(int row, int col)
{
	row = rowBelow(row);
	return alive[row][col];
}

/** true if the cell NE is alive*/
bool aboveright(int row, int col)
{
	row = rowAbove(row);
	col = colRight(col);
	return alive[row][col];
}

/** true if the cell SE is alive*/
bool belowright(int row, int col)
{
	row = rowBelow(row);
	col = colRight(col);
	return alive[row][col];
}

/** true if the cell NW is alive*/
bool aboveleft(int row, int col)
{
	row = rowAbove(row);
	col = colLeft(col);
	return alive[row][col];
}

/** true if the cell SW is alive*/
bool belowleft(int row, int col)
{
	row = rowBelow(row);
	col = colLeft(col);
	return alive[row][col];
}

/**Returns the number of living cells sorrounding this one.*/
int numberAround(int row, int col)
{
	int around = 0;
	if(left(row,col))
		around++;

	if(right(row,col))
		around++;

	if(above(row,col))
		around++;

	if(below(row,col))
		around++;

	if(aboveright(row,col))
		around++;

	if(aboveleft(row,col))
		around++;

	if(belowright(row,col))
		around++;
	
	if(belowleft(row,col))
		around++;	
	
	return around;
}

/**
 * Moves all of the cells
 */
void move()
{
	blank_num();

	for(int i = 0; i < ROWS; i++)
		for(int j = 0; j < COLS; j++)
			num[i][j] = numberAround(i,j);

	
	for(int i = 0; i < ROWS; i++)
		for(int j = 0; j < COLS; j++)
			if((num[i][j] == 2 && alive[i][j]) || num[i][j] == 3)
				alive[i][j] = true;
			else
				alive[i][j] = false;
}


int main()
{
	while(true)
	{
		boardnum++;
		random_fill();
	
		for(iteration = 0;iteration < 200; iteration++)
		{
			do_output();
			move();	
			timespec d;
			d.tv_sec=0, d.tv_nsec=500000000;
			nanosleep( &d, &d );
		}
		
		boardnum++;
		gosper_gun();
		for(iteration = 0;iteration < 200; iteration++)
		{
			do_output();
			move();	
			timespec d;
			d.tv_sec=0, d.tv_nsec=500000000;
			nanosleep( &d, &d );
		}
	}

	return 0; // implicit by gcc, so not really needed.
}
