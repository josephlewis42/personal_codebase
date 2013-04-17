#!/usr/bin/env python
'''


A Pythagorean triplet is a set of three natural numbers, a < b < c, for which,
a2 + b2 = c2

For example, 32 + 42 = 9 + 16 = 25 = 52.

There exists exactly one Pythagorean triplet for which a + b + c = 1000.
Find the product abc.

'''
import pymath
trip = pymath.primitive_pythagorean_triples(1000)[0]
print trip[0] * trip[1] * trip[2]
