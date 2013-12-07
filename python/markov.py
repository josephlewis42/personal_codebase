#!/usr/bin/env python3
'''
Provides common functions used through the similarity engines.

Copyright 2012 Joseph Lewis <joseph@josephlewis.net> | <joehms22@gmail.com>

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

    Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.
    
    Redistributions in binary form must reproduce the above 
    copyright notice, this list of conditions and the following disclaimer 
    in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
 ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED 
 WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
 DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
 FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
 DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
 SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
 CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
 OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
 OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

2012-10-28 - Initial Work
'''
import random
import pickle
import re

START_WORD = "<START>"
TERMINAL_WORD = "<END>"

def document_to_terms(doc):
	'''Parses a document in to a list of strings.'''
	doc = doc.lower()
	doc = re.sub(r"""[^\w\s]+""", '', doc)
	return doc.split()

class TwoGramCorpus():
	words = None
	def __init__(self, fp=None):
		if fp:
			self.words = pickle.load(fp)
		else:
			self.words = {}
	
	def save(self, fp):
		pickle.dump(self.words, fp, 1)
		
	def load_file(self, fp):
		for sentence in fp.read().split("."):
			self.load_line(document_to_terms(sentence))
			
	def load_line(self, line):
		if len(line) == 0:
			return
		
		line.append(TERMINAL_WORD)
		
		lastword = START_WORD
		for word in line:
			self.add_2gram(lastword, word)
			lastword = word
	
	def add_2gram(self, first, second):
		firstlist = None
		try:
			firstlist = self.words[first]
		except KeyError:
			self.words[first] = {second : 1}
			return
		try:
			firstlist[second] += 1
		except KeyError:
			firstlist[second] = 1
	
	def __str__(self):
		return str(self.words)
	
	def __unicode__(self):
		return str(self.words)
		
	def _random_prob_word(self, start):
		''' chooses a random word that follows the given one 
		with the probability of the frequency it occurs.
		'''
		
		rest = self.words[start]
		total_possible = sum(rest.values())
		
		chosen = random.randint(1,total_possible)
		
		for word, value in rest.items():
			chosen -= value
			
			if chosen <= 0:
				return word
		
		return None
			
		
		
	def generate_sentence(self):
		# choose a random start word.
		sentence = []
		lastword = self._random_prob_word(START_WORD)
		
		while lastword != TERMINAL_WORD:
			sentence.append(lastword)
			lastword = self._random_prob_word(lastword)
		
		return " ".join(sentence) + "."
	
	
	def generate(self, num_sentences):
		sentences = []
		for i in range(num_sentences):
			sentences.append(self.generate_sentence())
			
		return " ".join(sentences)

if __name__ == "__main__":
	tgc = TwoGramCorpus()
	tgc.load_file(open('/home/joseph/Desktop/books2/pg2.txt'))
	print(tgc.generate(3))
