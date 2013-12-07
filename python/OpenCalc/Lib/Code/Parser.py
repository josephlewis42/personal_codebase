'''
This module takes care of doing math for the program.

@Author = Joseph Lewis
@Date = Friday, Feb. 19, 2010
@License = GPL
==Changelog==
2/19/2010 - Original Built by Joseph Lewis <joehms22@gmail.com>
2/23/2010 - Added simple fixes for floating point errors, added ^ ** replace
2/25/2010 - Added a fix for division of two ints for versions before 3.0
2/28/2010 - Added support for variables a-z
2010-03-14 - Added another parse method, and cleaned up the original parse
'''
from __future__ import division #Do division like humans do in old python versions
import sys
from numpy import array
#Check what version python is:
#If less than 2.2 will not work properly
if sys.hexversion < 0x020200F0:
    print >> sys.stderr, "Your python is too old for division to work natrually. OPENCALC ERR:0001"
#If 2.2 to 3 then will work with import statment
elif sys.hexversion >= 0x020200F0 and sys.hexversion <0x030000F0:
    print >> sys.stderr, "Importing future so division will work right. OPENCALC NOT:0001"
#If 3 or beyond remove the unneeded and possibly hazardous import
elif sys.hexversion >= 0x030000F0:
    del  division

#Import all functions from the functions library, in their native form so eval can use them
from Functions import *
#Import Variables
from Variables import *
ans = 0 #The answer from the last problem (easy reference)

def parse(user_input):
    '''
    Parse user input, by first cleaning it up so the machine can read what the 
    user put in, then run the input to set any vars it used, then execute it to
    use as the new ans variable, then fix it's type, and send it on it's way.
    '''
    #Import all global variables the user has access to
    global ans,a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z
    
    #Clean up user input
    user_input = user_input.replace("^", "**")
    
    #Execute code (if any) like y = 3*3, this will set y
    exec "%s" % (user_input) in globals()
    
    #Set the ans variable.
    ans = eval(user_input)
    
    #Solve rounding errors (Floating Point Arithmatic)
    if isinstance(ans, (int, long, float, complex)):
        ans = float("%.8f" % ans)# Change to float with 8 places, if a number
    return ans

def clean_parse(machine_input, x = x):
	'''
	This parse method is used for internal parsing, of things like arrays
	by modules like Graph, everything should be allready evaluated.
	
	If you want to replace the variable x with one of your own then do so,
	otherwise the global x will be used.
	'''
	global ans,a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,y,z
	return eval(machine_input)
