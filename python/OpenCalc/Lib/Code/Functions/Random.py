'''
Random makes random numbers.
@Author = Joseph Lewis <joehms22@gmail.com> 
@Date = 2010-03-04
@License = GPL
==Changelog==
2010-03-04 - Module started.
'''
#Import Statements
import random as r
import time as t

#Define Constants


#Define Functions
def time():
    '''
    Return the current date.
    '''
    return t.asctime()

def seedrand(seed=time()):
    '''
    Seeds the number generator, if no input is provided the current time will be
    used.
    '''
    r.seed(seed)
    return "Seeded with %s." %(seed)

def random():
    '''
    Returns a random float between  0, and 1
    '''
    return r.random()

def randint(low = 0, high = 99):
    '''
    Returns a random number between the two specified, if none specified returns
    between 0 and 99
    '''
    return r.randint(low, high)
