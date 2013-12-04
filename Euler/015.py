'''Starting in the top left corner of a 2x2 grid, and only being able to move to
the right and down, there are exactly 6 routes to the bottom right corner.


How many such routes are there through a 20x20 grid?
'''

# there are a total of n * 2 steps you must take where n is length of a side,
# therefore let's say you choose only the down steps, leaving the rest to be 
# across:

import pymath

print(pymath.choose(40,20))
