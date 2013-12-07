#!/usr/bin/env python
''' Conway's game of life in python.

Copyright 2011-09-30 Joseph Lewis <joehms22@gmail.com> MIT License

   1. Any live cell with fewer than two live neighbours dies.
   2. Any live cell with two or three live neighbours lives.
   3. Any live cell with more than three live neighbours dies.
   4. Any dead cell with exactly three live neighbours becomes alive.
   -- Wikipedia.
'''

import random
import time


ROWSCOLS = None  # Number of rows and columns in the game.
grid = None  # A grid with 0s and 1s, 0 is no cell, 1 is a cell.

def printgrid():
	'''Prints out the given grid after blanking the screen.'''
	
	print 10 * "\n"
	print "+"+ "-" * ROWSCOLS + "+"  # Border top
	
	for r in grid:
		line = "|"  # Border Left
		for c in r:
			if c:
				line += "0"  # Cell
			else:
				line += " "
		print line + "|"  # Border Right
	
	print "+"+ "-" * ROWSCOLS + "+"  # Border Bottom


def do_life():
	'''calculates the next grid'''
	
	grid_len = range(0,ROWSCOLS)
	grid2 = [[0 for i in grid_len] for i in grid_len]
	
	for r in grid_len:
		for c in grid_len:
			if grid[r][c]:
				increment(grid2, r, c)
	
	for r in grid_len:
		for c in grid_len:
			g = grid2[r][c]
			if g < 2 or g > 3:
				grid[r][c] = 0
			elif g == 3:
				grid[r][c] = 1 


def increment(grid, row, col):
	'''Increments the life count for all cells around this one.'''
	for r,c in [(row, col+1), (row, col-1),
				(row+1, col), (row-1, col),
				(row+1, col+1), (row-1, col-1),
				(row+1, col-1), (row-1, col+1)]:
		grid[r % ROWSCOLS][c % ROWSCOLS] += 1
	

def start_life():
	'''Randomly fills the game.'''
	for i in range(0, ROWSCOLS**2 / 4):
		r = random.randint(0, ROWSCOLS-1)
		c = random.randint(0, ROWSCOLS-1)
		grid[r][c] = 1
		
		
if __name__ == "__main__":	
	try:
		print("=Conways Game of Life=")
		k = int(input("How many turns should I run before I reset (200 is nice)? "))
		ROWSCOLS = int(input("How many rows and columns of life should there be (35 is nice)? "))
		t = float(input("How many frames per secould should I run (10 is nice)? "))
		
	except Exception:
		print("Hey! Play nice, enter a number!")
		exit(1)
	
	grid = [[0 for i in range(0, ROWSCOLS)] for i in range(0, ROWSCOLS)]

	j = 0
	while True:
		if not j:
			start_life()
			j = k # Number of turns to run before restart.
		j -= 1
		do_life()
		printgrid()
		time.sleep(1/t)
