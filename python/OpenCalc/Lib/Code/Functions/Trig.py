'''
Basic Trig Stuff
@Author = Joseph Lewis
@Date = Friday, Feb. 19, 2010
==Changelog==
2010-2-25 - Added the boolean that changes if you want radians or degrees
2010-02-27 - Fixed a problem with the basic trigonometric functions that was 
causing improper numbers to be returned. Also added the functions that set the
want_deg variable, so the user can do this from now on easily.s
'''

import math

PI = math.pi

pie = "()()() \n|\\   3\n\\ \\  .\n \\ \\ 1\n  \\_\\4"
PIE = pie

want_deg = True #Used to tell the system to use radians or degrees
#Conversion
def useradians():
    global want_deg
    want_deg = False
    return "Now using Radians"
def usedegrees():
    global want_deg
    want_deg = True
    return "Now using Degrees"
#Basic
def sin(num):
	if want_deg == True:
		return math.sin(torad(num))
	else:
		return math.sin(num)
		
def cos(num):
	if want_deg == True:
		return math.cos(torad(num))
	else:
		return math.cos(num)

def tan(num):
	if want_deg == True:
		return math.tan(torad(num))
	else:
		return math.tan(num)


#Arc
def asin(num):
	if want_deg == True:
		return math.asin(torad(num))
	else:
		return math.asin(num)
		
def acos(num):
	if want_deg == True:
		return math.acos(torad(num))
	else:
		return math.acos(num)
		
def atan(num):
	if want_deg == True:
		return math.atan(torad(num))
	else:
		return math.atan(num)
		

#Conversions
def todeg(num):
	return num*(180.0/PI)
def torad(num):
	return num*(PI/180.0)
