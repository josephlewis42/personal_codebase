'''
A small, general-purpose math library for Python

- Joseph Lewis
'''
import math

def factor(n):
	''' Finds the factors of the given number.'''	
	result = set()
	for i in range(1, int(n ** 0.5) + 1):
		div, mod = divmod(n, i)
		if mod == 0:
			result |= {i, div}
	return result

def prime(n):
	''' Finds if n is a prime number. Optionally n can be a set, will
	return a set containing all primes in that list.'''
	try:
		return n == 1 or len(factor(n)) == 2
	except Exception:
		return [x for x in n if prime(x)]
		
def prime_factors(n):
	'''Returns the prime factors of the given number.'''
	return prime(factor(n))

def has_multiple(i, multiples):
	'''True if i is divisible by any number in the array multiples an
	even number of times.
	'''
	for p in multiples:
		if i == p or i % p:
			return True
	return False


def gen_fib(largest, last = 2, prev = 1, li = [1,2]):
	''' Generates the fibonacci numbers up to the largest given.'''
	if last + prev > largest:
		return li
	li.append(last + prev)
	return gen_fib(largest, last+prev, last, li)
	
def palindrome(number):
	'''Returns true if the number is a palindrome'''
	backwards = "".join(reversed(str(number)))
	return backwards == str(number)
	
def gcd(a, b):
	'''Returns the greatest common divisor of the two numbers.
	Using the Euclidian method.'''
	mod = 1
	while mod != 0:
		div,mod = divmod(a,b)
		a = b
		b = mod
	return a

def lcm(a, b):
	'''Returns the leaste common multiple of the two numbers.'''
	return abs(a * b) / gcd(a, b)
	
def lcm_array(nums):
	''' Returns the least common multiple of a list of numbers.'''
	return reduce(lambda x, y: lcm(x,y), nums)


def sum_of_squares(nums):
	return sum([x ** 2 for x in nums])
	
def square_of_sum(nums):
	return sum(nums) ** 2

def n_primes(n):
	'''Returns the first n primes.'''
	i = 0
	primes = set()
	while len(primes) != n:
		i += 1
		if prime(i):
			primes.add(i)
	return primes
	
def primes_below(n):
	'''Finds a list of all primes below the given number. Using 
	Sieve's Algorithm.'''
	if n < 2: 
		return []
	
	if n == 2:
		return [2]
		
	n = n + 1 # find the primes below n
	
	marked = set()
	primes = []
	
	for x in range(2, n):
		if not x in marked:
			primes.append(x)
			for y in range(x, n, x):
				marked.add(y)
	
	return primes
	
def quadratic(a, b, c, x=0):
	'''Returns the values for c such that the quadratic equation is 
	solved. Only returns real solutions. Returns None for
	complex numbers.'''
	
	c = c - x
	sltns = b**2 - 4 * a * c
	
	if sltns > 0:
		sltn1 = (-b + math.sqrt(sltns))/(2.0 * a)
		sltn2 = (-b - math.sqrt(sltns))/(2.0 * a)
		return (sltn1, sltn2)
	if sltns == 0:
		sltn1 = (-b + math.sqrt(sltns))/(2.0 * a)
		return (sltn1, sltn1)
		
	return None
	

def pythagorean_triple(perim):
	'''Returns a pythagorean triple such that the sum of a,b,c is 
	the given number. The triples won't be primitive.'''
	#perim = 2n + 1 + 2n(n+1) + 2n(n+1) + 1
	#perim = 4n**2 + 6n + 2
	
	# n = 15
	
	q = quadratic(4, 6, 2, perim)
	
	n = q[0] if q[0] > q[1] else q[1]
	
	a = 2 * n + 1
	b = 2 * n * (n + 1)
	c = 2 * n * (n + 1) + 1
	
	return (a,b,c)
	
def are_coprime(a,b):
	'''Determines if the two numbers are coprime.'''
	return gcd(a,b) == 1
	
def is_pythagorean(a,b,c):
	return (a**2 + b**2) == c**2
	
def primitive_pythagorean_triples(perim):
	'''Returns a pythagorean triple such that the sum of a,b,c is the given 
	number. Returns none if it does not exist.
	'''
	results = []
	
	for c in range(2, perim):
		for b in range(1, perim - c):
			a = perim - b - c
			if a > b:
				continue
			if is_pythagorean(a,b,c):
				results.append([a,b,c])
	return results
	
def split_2d_array_to_1d(array, up=False, down=False, left=False, right=True, diagonal_up=False, diagonal_down=False):
	'''
	Splits a 2d array in to a bunch of 1d arrays, the array should be in the format [row][col]
	'''
	result = []
	
	if up:
		for col in range(len(array)):
			tmp = []
			row = 0
			try:
				tmp.append(array[row][col])
				row += 1
			except IndexError:
				result.append(tmp)
	if down:
		for col in range(len(array)):
			tmp = []
			row = 0
			try:
				tmp.append(array[row][col])
				row += 1
			except IndexError:
				result.append([x for x in reversed(tmp)])
	
	if left:
		for a in array:
			result.append([x for x in reversed(a)])
	if right:
		for a in array:
			result.append(a)
	
	if diagonal_up:
		maxrow = len(array)
		maxcol = len(array[1])
		# try going down
		for row in range(len(array)):
			tmp = []
			col = 0
			try:
				while row >= 0 and col >= 0 and row < maxrow and col < maxcol:
					tmp.append(array[row][col])
					row -= 1
					col += 1
			except IndexError:
				pass
			result.append(tmp)
		
		# then across
		for col in range(1,len(array[len(array) - 1])):
			tmp = []
			row = len(array) - 1
			try:
				while row >= 0 and col >= 0 and row < maxrow and col < maxcol:
					tmp.append(array[row][col])
					row -= 1
					col += 1
			except IndexError:
				pass	
			result.append(tmp)
	
			
	if diagonal_down:
		maxrow = len(array)
		maxcol = len(array[1])
		# try going down
		for row in range(maxrow):
			tmp = []
			col = 0
			try:
				while row >= 0 and col >= 0 and row < maxrow and col < maxcol:
					tmp.append(array[row][col])
					row += 1
					col += 1
			except IndexError:
				pass
			result.append(tmp)
		
		# then across
		for col in range(1,maxcol):
			tmp = []
			row = 0
			try:
				while row >= 0 and col >= 0 and row < maxrow and col < maxcol:
					tmp.append(array[row][col])
					row += 1
					col += 1
			except IndexError:
				pass	
			result.append(tmp)
	return result
		
	
	
def greatest_product(numbers, length_of_chain):
	'''Finds the greatest product that can be found in the list of
	numbers.
	'''
	
	largest = None
	for i in range(len(numbers) - length_of_chain + 1):
		num = numbers[i]
		for k in range(1,length_of_chain):
			num *= numbers[i + k]
		if num > largest or i == 0:
			largest = num
	
	return largest
