 /**
  * 
  * Copyright 2012-02-26 Joseph Lewis <joehms22@gmail.com>
  * 
  * Conway's game of life in cpp. The world is looped (life at top can 
  * move to bottom &c.) Built to run on the Arduino with the TVout
  * library.
  * 
  * Apache 2.0 License
  *
  * http://code.google.com/p/arduino-tvout/
  * 
  */

#include "TVout.h"
#include "fontALL.h"
TVout TV;

const int COLS = 29;
const int ROWS = 15;

// The "Alive" cells on the board.
uint32_t alive[ROWS] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};


bool isAlive(int row, int col)
{
	return alive[row] & (1<<(col));
}

void setAlive(int row, int col)
{
	alive[row] |= 1 << col;
}

int boardnum = 0; // number of boards run by the game
int iteration = 0; // current round in the current board

int numberAround(int row, int col);

/**
 * Sets the alive array to all falses.
 */
void blank_alive()
{
	for(int i = 0; i < ROWS; ++i)
		alive[i] = 0;
}

/**
 * Writes output to the console.
 */
void do_output()
{
				TV.clear_screen();
		TV.print("Board: ");
		TV.print(boardnum);
		TV.print(" Iteration: ");
		TV.println(iteration);

	for(int i = 0; i < ROWS; i++)
	{

		for(int j = 0; j < COLS; j++)
		{
			// WIDTH, HEIGHT
			if(isAlive(i,j))
				TV.print("0");
			else
				TV.print(" ");
		}
		if(i != ROWS -1)
			TV.print("\n");
	}

}

/**
 * Randomly fills the grid with alive cells after blanking.
 */
void random_fill()
{
	blank_alive();
	randomSeed(analogRead(0));
	
	// Fill 30% of the cells
	int numToFill = (ROWS * COLS) * 30 / 100 ;
	
	for(int r = 0; r < numToFill; r ++)
	{
		int row = rand() % ROWS;
		int col = rand() % COLS;
		
		setAlive(row,col);
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
	return isAlive(row,col);
}

/** true if the cell to the right is alive*/
bool right(int row, int col)
{
	col = colRight(col);
	return isAlive(row,col);
}

/** true if the cell above is alive*/
bool above(int row, int col)
{
	row = rowAbove(row);
	return isAlive(row,col);
}

/** true if the cell below is alive*/
bool below(int row, int col)
{
	row = rowBelow(row);
	return isAlive(row,col);
}

/** true if the cell NE is alive*/
bool aboveright(int row, int col)
{
	row = rowAbove(row);
	col = colRight(col);
	return isAlive(row,col);
}

/** true if the cell SE is alive*/
bool belowright(int row, int col)
{
	row = rowBelow(row);
	col = colRight(col);
	return isAlive(row,col);
}

/** true if the cell NW is alive*/
bool aboveleft(int row, int col)
{
	row = rowAbove(row);
	col = colLeft(col);
	return isAlive(row,col);
}

/** true if the cell SW is alive*/
bool belowleft(int row, int col)
{
	row = rowBelow(row);
	col = colLeft(col);
	return isAlive(row,col);
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
	uint32_t nextRows[ROWS] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0};
	

	for(int i = 0; i < ROWS; i++)
	{
		for(int j = 0; j < COLS; j++)
		{
			int na = numberAround(i,j);
			if((na == 2 && isAlive(i,j)) || na == 3)
				nextRows[i] |= 1 << j;
		}
	}

	
	for(int i = 0; i < ROWS; i++)
		alive[i] = nextRows[i];
}

void setup()
{
	TV.begin(NTSC,120,96);
	TV.select_font(font4x6);
}

void loop() {
	boardnum++;

	TV.println("Conways game of life for Arduino, Copyright 2012 Joseph Lewis <joehms22@gmail.com>");
	TV.delay(2000);
	
	random_fill();
	
	TV.print("Doing iterations");
	
	for(iteration = 0;iteration < 50; iteration++)
	{
		do_output();
		move();	
		TV.delay(500);
	}
}
