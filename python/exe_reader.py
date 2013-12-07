#!/usr/bin/env python
'''
A program that extracts strings from binary files.

Usage: reader.py path/to/file

Apache License Joseph Lewis <joehms22@gmail.com> 2011
'''

import sys

numstrs = 0
with open(sys.argv[1]) as j:
	j = j.read()
	mystr = ""
	for i in range(0,len(j)):
		if 31 < ord(j[i]) < 127:
			mystr += j[i]
		else:
			if len(mystr) > 4:  # If the string isn't that long, then discard it, we don't care.
				uniqs = set()
				for char in mystr:
					uniqs.add(char)
				
				if len(uniqs) > .5 * len(mystr): # If duplicate chars are less than half the string	
					print mystr
					numstrs += 1
				
			mystr = ""
			
print "==========\n\nOutput: %s strings" % numstrs
