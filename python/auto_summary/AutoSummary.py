#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Provides An Automated Summary of a document.

Copyright 2011 Joseph Lewis <joehms22 [at] gmail com>

Originally Made: 2011-09-21

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

* Redistributions of source code must retain the above copyright
  notice, this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above
  copyright notice, this list of conditions and the following disclaimer
  in the documentation and/or other materials provided with the
  distribution.
* Neither the name of the  nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

import sys
import re
import argparse

__author__ = "Joseph Lewis"
__copyright__ = "Copyright 2011, Joseph Lewis"
__license__ = "BSD"

TOP_HUNDRED_SCORE = 0
EN_TOP = '''the be to of and a in that have i it for not on with he as you do at 
this but his by from they we say her she or an will my one all would 
there their what so up out if about who get which go me when make can 
like time no just him know take person into year your good some could 
them see other than then now look only come its over think also back 
after use two how our work first well way even new want because any 
these give day most us'''



def chars_per_word(sentence):
	'''Returns the average characters per word.'''
	return float(len(sentence)) / float(len(sentence.split(' '))) 

def clean_text(text,leavepunct=False):
	# Strip to a-z A-Z (TODO: I18N).
	text = text.replace("\n", " ")
	if leavepunct:
		return re.sub("[^a-z.!\? ]", " ", text.strip().lower())
	return re.sub("[^a-z ]", " ", text.strip().lower())

def word_frequency(text):
	'''Counts the frequenc of words in the piece of text, and returns
	a dict for each word (a-z) lowercased where the key represents the 
	word and the number of times the word is found the value.
	
	'''
	words = {}
	
	
	tmp = clean_text(text)

	# Cut to words.
	for word in tmp.split():
		if word in words:
			words[word] += 1
		else:
			words[word] = 1
			
	return words
	
def set_words_to_value(word_dict, top=EN_TOP, value=TOP_HUNDRED_SCORE):
	'''Sets the given words to the given value in the given word_dict.
	The default is to set the top hundred words in english to the 
	TOP_HUNDRED_SCORE.
	
	'''
	
	j = word_frequency(top).keys() # get the words in the top hundred text.
	# remove the top 100 words
	for w in j:
		words[w] = value
		
def sentences_in(text):
	'''Returns a list of sentences in the text.
	
	'''
	text = text.replace("\n", " ")
	return re.split('[\?.!]', text)
	
	
def score_sentence(sentence, words):
	'''The scoring function, given a dictoinary of word:value pairs, 
	creates a score for each sentence.
	
	'''
	# Score value based upon words and frequencies of those words.
	tmp = clean_text(sentence)
	total = 0
	
	for word in tmp.split():
		if word in words:
			total += words[word]
			
	# Make the total in to a percentage.
	try:
		total /= float(len(tmp.split()))
	
		# Secret ingredient, higher characters per word generally means 
		# more important sentence.
		total *= chars_per_word(tmp)
		
		return total
	except ZeroDivisionError:
		return -100


def top_sentences(text, word_freq_dict):
	'''Returns a sorted list with the top rated sentences first, that 
	contains the tuples (score, sentence_location, sentence_text)
	
	For example, the sentence "Call me Ishmael" would come back:
		(1.8304283, 0, "Call me Ishmael.")
	
	0 would mean it was the first sentence in the text, and it had a 
	score of 1.83...
	
	'''
	sentences = [] # array of tuples (total score, sentence num, sentence text)
	known_sentences = set()
	currs = 0
	for s in sentences_in(text):
		currs += 1 # Increment the current sentence.
		total = score_sentence(s, words) # Don't add duplicate sentences.

		s = s.strip()
		if s not in known_sentences:
			sentences.append((total, currs, s+"."))
			known_sentences.add(s)
		
	# Sort highest rated sentences to lowest.
	sentences = sorted(sentences)
	sentences.reverse()
	
	return sentences
	
	
def __combine_summary(summary):
	'''Combines a summary in to a meaningful paragraph. A summary is an 
	array of tuples with values of (position of sentence, text). This
	creates better summary paragraphs by ordering important sentences
	in the order they were originally.
	
	'''
	summary = sorted(summary)
	
	paragraph = ""
	for l, s in summary:
		paragraph += s + " "
		
	return paragraph

def percentage_top(percentage, sorted_sentences):
	'''Returns the top rated percentage of the given sentences, in 
	paragraph form.
	
	i.e. to get the top 25 percent of a text, call with:
		percentage_top(25, <list from top_sentences>)
	
	'''
	
	percentage = percentage / 100.0
	
	num_sentences = int(len(sorted_sentences)*percentage) + 1
	
	if num_sentences >= len(sorted_sentences):
		num_sentences = len(sorted_sentences)
	
	# Create summary (top x sentences)
	summary = []
	for j in range(num_sentences):
		t,l,s = sorted_sentences[j]
		summary.append((l,s))
	
	
	return __combine_summary(summary)
	
	

def top_words(num_words, sorted_sentences):
	'''Returns x number of words from the top sentences.'''
	
	summary = []
	words = 0
	try:
		for t,l,s in sorted_sentences:
			if words >= num_words:
				break
			
			words += len(s.split())
			summary.append((l,s))
		
		
	except IndexError:
		pass
	
	return __combine_summary(summary)


if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description='Creates summaries from documents by magic.')
	parser.add_argument('-p','--percent', type=int, default=None,
					   help='the percent of the original document to give as a summary')
	parser.add_argument('-w', '--words', type=int, default=None,
					   help='the number of words to output as a summary')
					   
	parser.add_argument('PATH', help='the path of the textfile to read from')

	args = parser.parse_args()
	
	try:
		if args.PATH:
			text = open(args.PATH).read()
			words = word_frequency(text)
			
			set_words_to_value(words)
			sentences = top_sentences(text, words)
			
			if args.words:
				print top_words(args.words, sentences)
			if args.percent:
				if args.words:
					print "\n\n"
				print percentage_top(args.percent, sentences)

	except IOError:
		print "File given can't be found."
