#!/usr/bin/env python
# Apache License 2011-11 Joseph Lewis <joehms22@gmail.com>
import re

while True:
	f_name = raw_input("Enter the name of the file or q to quit: ")
	
	if f_name == 'q':
		exit()
	
	with open(f_name) as f:
		tmp = map(float, re.sub('[^0-9 -.]','',f.read()).split(' ')) # Read the file (removing garbage), split it, and turn it to a list of floats. n
		
		distance = tmp[0]
		nums = sorted(tmp[1:])  # nlg(n) running time, as per Python Documentation
		
		sets = []
			
		for i in nums:
			if not sets:
				sets.append([i])
			else:
				for s in sets:
					if s[len(s) - 1] + distance < i:
						s.append(i)
						break
				else: # The for-else loop only runs if the for loop falls off the end rather than being broken.
					sets.append([i])
					
		print "%s sets returned with distance %s\n" % (len(sets), distance)
		
		for s in range(len(sets)):
			print "\n== Set %s ==\n%s" % (s+1, sets[s])
