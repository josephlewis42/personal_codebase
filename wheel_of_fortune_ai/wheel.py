#!/usr/bin/env python

from __future__ import division
import common
import re
import ngram



# sort in to lengths

words = []
puzzle = []

guessed_letters = []
fullpuzzle = None

def setupPuzzle():
	global puzzle
	global guessed_letters
	global fullpuzzle
	
	print "To play, enter a full puzzle in lower case."
	print "The computer will output its best guesses for the puzzle."
	print "After that, input a letter, and the computer will guess again."
	
	tmp = raw_input("Enter Puzzle: ")
	if tmp == '':
		exit()
		
	fullpuzzle = None
	
	try:
		puzzle = [['.' for j in range(int(i))] for i in tmp.split()]
		guessed_letters = []
	except ValueError:
		puzzle = tmp.lower()
		fullpuzzle = tmp
		
		puzzle = [['.' for j in range(len(i))] for i in tmp.split()]

def format_output(grams):
	grams = sorted(grams, reverse=True)
	
	return ["%s (%s)" % (tup[1], tup[0]) for tup in grams]

def guess_ngram(location = 0, last=None,allstart=False):
	
	grams = []
	
	if len(guessed_letters) != 0:
		non_letters = "[^%s]" % ("".join(guessed_letters))
	else:
		non_letters = "."
	
	regex = ("^%s$" % ("".join(puzzle[location]))).replace(".",non_letters)
	
	
	if location == 0:
		words = ngram.find_startword(regex)
		
		if len(puzzle) == 1:
			return format_output(words)
		
		if not allstart:
			words = words[:10]
		else:
			words = words[:50]
	else:
		words = ngram.find_matches(last, regex)[:5]
	
	mult = 1
	if words == []:
		words = ngram.find_startword(regex)[:5]
		mult = .5
	
	if location == len(puzzle) - 1:
		return words
	
	for val, word in words:
		for tup in guess_ngram(location + 1, word)[:5]:
			grams.append(((tup[0] + val) * mult, word + " " + tup[1]))
	
	if location != 0:
		return grams
		
	if len(grams) == 0:
		return guess_ngram(0,None,0,True)
	
	return format_output(grams) 

def find_matching_words(location):
	wordlist = set()
	
	regex = "^%s$" % ("".join(puzzle[location]))
	
	desired_length = len(puzzle[location])
	
	for word in words:
		if(len(word) == desired_length):
			if(re.match(regex, word)):
				wordlist.add(word)
	
	return wordlist

def output_puzzle():
	print("Puzzle: %s" % (" ".join(["".join(puz) for puz in puzzle]),))
	if fullpuzzle != None:
		print("       (%s)" % (fullpuzzle,))

def update_puzzle():
	global puzzle
	
	if fullpuzzle == None:
		try:
			update = raw_input("Update puzzle <letter> [wordnum,loc ...] (blank to end): ").split()
	
			letter = update[0][0]
	
			for pos in update[1:]:
				wordnum, loc = map(int, pos.split(","))
		
				puzzle[wordnum - 1][loc - 1] = letter
			
			guessed_letters.append(letter)
			return False
		except IndexError:
			return True
	else:
		letter = 'blank'
		while len(letter) > 1:
			letter = raw_input("Update puzzle <letter> (blank to end): ")
		
		if letter == '':
			return True
		
		guessed_letters.append(letter)
		
		count = 0
		for word in puzzle:
			for pos in range(len(word)):
				if fullpuzzle[count] == letter:
					word[pos] = letter
				count += 1
			count += 1 # manage spaces
		
		return False


if __name__ == "__main__":
	while(True):
		setupPuzzle()
		
		puzzle_done = False
		while(not puzzle_done):
			print("\n".join(guess_ngram()[:10]))
			puzzle_done = update_puzzle()
			output_puzzle()
		
