'''
Collatz sequence

The following iterative sequence is defined for the set of positive integers:

n -> n/2 (n is even)
n -> 3n + 1 (n is odd)

Using the rule above and starting with 13, we generate the following sequence:

13 -> 40 -> 20 -> 10 -> 5 -> 16 -> 8 -> 4 -> 2 -> 1
It can be seen that this sequence (starting at 13 and finishing at 1) contains 10 terms. Although it has not been proved yet (Collatz Problem), it is thought that all starting numbers finish at 1.

Which starting number, under one million, produces the longest chain?

NOTE: Once the chain starts the terms are allowed to go above one million.

'''

import pymath
sequences = {}


def find_next_number(n):
	if n % 2 == 0:
		return n / 2
	else:
		return 3 * n + 1

def get_collatz_sequence(n):
	''' Use some dynamic programming here to speed things up!
	'''
	
	if n == 1:
		return [1]
	
	if n in sequences:
		return sequences[n]
	
	return [n] + get_collatz_sequence(find_next_number(n))
	

for i in range(1,1000000):
	seq =  get_collatz_sequence(i)
	sequences[i] = seq


largestValue = 0
largestKey = 0
for key, value in sequences.items():
	if len(value) > largestValue:
		largestValue = len(value)
		largestKey = key

print largestKey
