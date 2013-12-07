'''
Description Of Module
@Author = Joseph Lewis<joehms22@gmail.com>
@Date = 2010-2-24
@License = GPL
==Changelog==
2010-2-24 - First version made by Joseph Lewis
'''
#Import Statements

#Define Constants

#Define Functions
def isNum(var):
	if(type(var).__name__ == 'int' or type(var).__name__ == 'float'):
		return True
	else:
		return False