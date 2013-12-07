#!/usr/bin/env python
'''A simple spell checker for Python, modified version of Peter Norvig's
http://norvig.com/spell-correct.html

Created by: Joseph Lewis <joehms22 [at] gmail [dot] com> 2012-09-19
'''
import re
import collections

DICTIONARY_FILE = "american-english"

class Checker:
	known_words = set()
	check_cache = {}
	alphabet = 'abcdefghijklmnopqrstuvwxyz'
	
	def __init__(self):
		''' Sets up the checker. '''
		with open(DICTIONARY_FILE) as fp:
			self.populate_dict(fp)
		
	def populate_dict(self, fp):
		''' Populates the known-words dictionary. '''
		
		# normalize everything in the aspell dict
		doc = fp.read()
		doc = doc.lower()
		doc = re.sub(r'[^\w\s]+', '', doc) 
		
		for word in doc.split():
			self.known_words.add(word)
			
	
	def get_doc_dict(self, document_words_list):
		'''Gets a word->frequency dict for the words in the given doc.'''
		model = collections.defaultdict(lambda: 1)
		for f in features:
			model[f] += 1
		return model
		
	
	def check_word(self, word, doc_dict={}):
		''' Checks the given word against the dictionary, returns a "corrected" 
		one. '''
		
		word = word.lower()
		
		try:
			return self.check_cache[word]
		except KeyError:
			pass # faster than if in
		
		if word in self.known_words:
			return word
		
		candidates = self.known([word]) or self.known(self.edits1(word)) or self.known_edits2(word) or [word]
		nuword = max(candidates, key=doc_dict.get)
		if len(candidates) == 1:
			self.check_cache[word] = nuword
		return nuword
		
		
	twitterizations = {"":"", "4":"for", "2":"to", "txt":"text"}
	
	def edits1(self, word):
		twitterizations = [word.replace(k,v) for k,v in self.twitterizations.items()]
		splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
		deletes    = [a + b[1:] for a, b in splits if b]
		transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
		replaces   = [a + c + b[1:] for a, b in splits for c in self.alphabet if b]
		inserts    = [a + c + b     for a, b in splits for c in self.alphabet]
		return set(deletes + transposes + replaces + inserts + twitterizations)

	def known_edits2(self, word):
		return set(e2 for e1 in self.edits1(word) for e2 in self.edits1(e1) if e2 in self.known_words)

	def known(self, words): 
		return set(w for w in words if w in self.known_words)
