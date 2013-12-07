'''
Description Of Module
@Author = Joseph Lewis<joehms22@gmail.com>
@Date = 2010-2-24
@License = GPL
==Changelog==
2010-2-24 - First version made by Joseph Lewis
2010-03-04 - Abs fixed so it will not return a string, and print an error Joseph Lewis
2010-03-17 - Abs fixed from a prior error, in which it didn't work (abs used instead of fabs)
'''
#Import Statements
import math
import OpenCalc
#Define Constants

#Define Functions
def abs(num):
	return math.fabs(num)
