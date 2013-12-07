'''
Works with fractions
@Author = Joseph Lewis
@Date = 2/19/2010
@License = GPL
==Changelog==
2/19/2010 - Original Built by Joseph Lewis <joehms22@gmail.com>
2/23/2010 - Changed caps to lower case for ease of typing, added fareyLimit var, and added function simplify so it will be easier for users.
'''
#Import Statements
import math
#Define Constants
fareyLimit = 1000 # The number of times farey executes until it chooses the  most correct answer
#Define Functions
def simplify(num):
	return farey(num,fareyLimit)

def farey(v, lim):
	'''
	Taken From http://code.activestate.com/recipes/52317/
	PSF License Scott David Daniels 
	'''
	if v < 0:
		n,d = FAREY(-v, lim)
		return -n,d
	z = lim-lim	# get 0 of right type for denominator
	lower, upper = (z,z+1), (z+1,z)
	while 1:
		mediant = (lower[0] + upper[0]), (lower[1]+upper[1])
		if v * mediant[1] > mediant[0]:
			if lim < mediant[1]: return upper
			lower = mediant
		elif v * mediant[1] == mediant[0]:
			if lim >= mediant[1]: return mediant
			if lower[1] < upper[1]: return lower
			return upper
		else:
			if lim < mediant[1]: return lower
			upper = mediant