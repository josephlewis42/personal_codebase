#!/usr/bin/env python

import re

ngrams = {}
word_scores = {}

with open("w2_.txt") as ngram:
	for line in ngram:
		nwords, w1, w2 = line.split()
		nwords = int(nwords)
		
		try:
			ngrams[w1].append((nwords, w2))
		except:
			ngrams[w1] = [(nwords, w2)]
	

start_words = ngrams.keys()

for key in start_words:
	ngrams[key] = sorted(ngrams[key], reverse=True)
	word_scores[key] = sum([tup[0] for tup in ngrams[key]])

def find_startword(regex):
	return sorted([(get_word_score(word), word) for word in start_words if re.match(regex, word) != None], reverse=True)

def find_matches(startword, regex):
	try:
		return [tup for tup in ngrams[startword] if re.match(regex, tup[1]) != None]
	except Exception, e:
		print(e)
		return []

def get_word_score(word):
	try:
		return word_scores[word]
	except KeyError:
		return 1
