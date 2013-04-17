#!/usr/bin/env python
'''
2520 is the smallest number that can be divided by each of the numbers from 1 to 10 without any remainder.

What is the smallest positive number that is evenly divisible by all of the numbers from 1 to 20?
'''
import pymath

# Know it must at least be a multiple of 20
print pymath.lcm_array(range(1,21))
