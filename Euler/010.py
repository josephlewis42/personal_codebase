#!/usr/bin/env python
'''
The sum of the primes below 10 is 2 + 3 + 5 + 7 = 17.

Find the sum of all the primes below two million.
'''
import pymath
primes = pymath.primes_below(2000000)
print sum(primes)
