'''
Holds Logarithmic and Exponential Functions
@Author = Joseph Lewis <joehms22@gmail.com>
@Date = 2010-03-03 (Originally)
@License = GPL
==Changelog==
2010-03-03 - Original of this document, so far it is a wrapper for the python log and exponential math functions, soon I hope it to be more
'''
#Import Statements
import math

#Define Constants
E = math.e

#Define Functions
def exp(base, exp):
	'''
	Raise the base to the exponent
	'''
	return base**exp

def log(num, base=10):
	'''
	Return the log of x to given base if no base is provided, use 10
	'''
	return math.log(num,base)

def natlog(num):
	'''
	Return the natural log of a number
	'''
	return math.log(num)
def ln(num):
	'''
	Return the natrual log of a number (TI-83)
	'''
	return math.log(num)

def sqrt(num):
	'''
	Return the square root of a number
	'''
	return math.sqrt(num)

def root(num, root):
	'''
	Return a root of the number:
	Original Code
	'''
	x = num**(1.0/root)
	return x
