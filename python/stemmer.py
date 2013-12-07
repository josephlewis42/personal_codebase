#!/usr/bin/env python
'''
An implementation of the PORTER2 algorithm for English stemming in 
Python. Implemented from:
http://snowball.tartarus.org/algorithms/english/stemmer.html

Copyright 2012 Joseph Lewis <joehms22@gmail.com> | <joseph@josephlewis.net>

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
import re


__author__ = "Joseph Lewis"
__copyright__ = "Copyright 2012, Joseph Lewis"
__license__ = "BSD"
__version__ = ""


VOWELS = ['a','e','i','o','u','y']
WXY = VOWELS + ['w','x','Y']
DOUBLES = ['bb','dd','ff','gg','mm','nn','pp','rr','tt']
VALID_LI = ['c','d','e','g','h','k','m','n','r','t']



def short_syllable(word):
	'''Define a short syllable in a word as either (a) a vowel 
	followed by a non-vowel other than w, x or Y and preceded by a 
	non-vowel, or * (b) a vowel at the beginning of the word 
	followed by a non-vowel. 
	
	RETURNS:
		All short syllables in word.
	'''
	
	regex = ur"([^aeiouy][aeiouy][^aeiouwxy])+?"
	
	shorts = re.findall(regex, word)
	
	if len(word) >= 2 and word[0] in VOWELS and word[1] not in VOWELS:
		shorts.append(word[:2])
	
	return shorts
			
def is_short(word, R1):
	 '''A word is called short if it ends in a short syllable, and if R1 is null
	 '''
	 
	 for short in short_syllable(word):
	 	if word.endswith(short) and R1 == None:
	 		return True
	 
	 return False

def replace_one_in_order(word, suffixes):
	
	for suffix, replacewith in suffixes.items():
		if word.endswith(suffix):
			return word[:-len(suffix)] + replacewith
	
	return word

def replace_if_in_order_and_in_r1(word, suffixes, r1):
	for suffix, replacewith in suffixes.items():
		if word.endswith(suffix) and suffix in word[r1:]:
			return word[:-len(suffix)] + replacewith
	return word
	
def delete_suffix(word, suffixes):
	for suffix in suffixes:
		if word.endswith(suffix):
			return word[:-len(suffix)]
	return word
	
def _setYs(word):
	word = [char for char in word]
	for i in range(len(word)):
		if i == 0 and word[0] == "y":
			word[0] = 'Y'
		elif word[i] == 'y' and word[i - 1] in VOWELS:
			word[i] = 'Y'
	return "".join(word)
			

def stem(word):
	'''
	R1 is the region after the first non-vowel following a vowel, or 
	the end of the word if there is no such non-vowel.
	'''
	
	word = word.lower()
	
	# if a word has 2 letters or less, leave it as it is
	if len(word) < 3:
		return word
		
	# remove initial ', if present
	if word.startswith("'"):
		word = word[1:]
	
	# set initiial y or y after vowel to Y
	word = _setYs(word)
	
	R1 = None
	for i in range(1, len(word)):
		if word[i] not in VOWELS and word[i - 1] in VOWELS:
			R1 = i + 1
			break
			
	R2 = None
	if R1:
		for i in range(R1, len(word)):
			if word[i] not in VOWELS and word[i - 1] in VOWELS:
				R2 = i + 1
				break
	
	short = is_short(word, R1)
	
	# Step 0: + Search for the longest among the suffixes,','s,'s' and remove if found.
	word = replace_one_in_order(word, {"'s'":"","'s":'',"'":''})
	
		
	''' Step 1a: Search for the longest among the following suffixes, and
	perform the action indicated. 
	'''
	if word.endswith('sses'):
		word = word[:-4] + "ss"
	elif word.endswith('ied') or word.endswith('ies'):
		if len(word) > 4:
			word = word[:-3] + "i"
		else:
			word = word[:-3] + "ie"
	elif word.endswith('s') and word[-2] not in VOWELS:
		word = word[:-1]
		
	# Step 1b
	if word.endswith("eedly") and R1 and "eedly" in word[R1:]:
		word = word[:-5] + "ee"
	elif word.endswith("eed") and R1 and "eed" in word[R1:]:
		word = word[:-3] + "ee"
	elif len([x for x in ['ed','edly','ing','ingly'] if word.endswith(x)]) > 0:
		word2 = replace_one_in_order(word, {'edly':'','ed':'','ingly':'','ing':''})
		
		for char in word2:
			# delete if the preceding word part contains a vowel, and after the deletion: 
			if char in VOWELS:
				word = word2
				
				#if the word ends at, bl or iz add e (so luxuriat -> luxuriate), or 
				word2 = replace_one_in_order(word, {'at':'ate','bl':'ble','iz':'ize'})
				if word2 is not word:
					word = word2
					break
					
				#if the word ends with a double remove the last letter (so hopp -> hop), or 
				for double in DOUBLES:
					if word.endswith(double):
						word = word[:-1]
						break
				#if the word is short, add e (so hop -> hope) 
				if is_short(word, word[R1:]):
					word = word + 'e'
	
	#replace suffix y or Y by i if preceded by a non-vowel which is not the first letter of the word (so cry -> cri, by -> by, say -> say) 
	elif len(word) > 2 and word[-1] in ['y','Y'] and word[-2] not in VOWELS:
		word = word[:-1] + 'i'
	
	
	# Step 2: Search for the longest among the following suffixes, and, if found and in R1, perform the action indicated. 
	word2 = replace_if_in_order_and_in_r1(word, {"tional":"tion",
												"enci":"ence",
												"anci":"ance",
												"abli":"able",
												"entli":"ent",
												"ization":"ize",
												"izer":"ize",
												"ational":"ate",
												"ation":"ate",
												"ator":"ate",
												"alism":"al",
												"aliti":"al",
												"alli":"al",
												'fulness':'ful',
												'ousli':'ous',
												'ousness':'ous',
												'iveness':'ive',
												'iviti':'ive',
												'biliti':'ble',
												'bli':'ble',
												'fulli':'ful',
												'lessi':'less',
												'logi':'ogi'}, R1)
	if word2 is not word:
		word = word2
	elif word.endswith('li') and word[-3] in VALID_LI and "li" in word[R1:]:
		word = word[:-2]
	
	# step 3
	word2 = replace_if_in_order_and_in_r1(word, {"ational":"ate",
												"tional":"tion",
												"alize":"al",
												"icate":"ic",
												"iciti":"ic",
												"ical":"ic",
												"ful":"",
												"ness":""}, R1)
	if word2 is not word:
		word = word2
	elif word.endswith('ative') and "ative" in word[R2:]:
		word = word[:-5]										
	
	# Step 4
	word2 = delete_suffix(word, ['al', 'ance', 'ence', 'er', 'ic', 'able', 'ible', 'ant', 'ement', 'ment', 'ent', 'ism', 'ate', 'iti', 'ous', 'ive', 'ize'])
	
	if word2 is not word:
		word = word2
	else:
		if word.endswith('ion') and word[:-4] in ['s','t']:
			word = word[:-3]
	
	# Step 5
	#Search for the the following suffixes, and, if found, perform the action indicated.

	#e - delete if in R2, or in R1 and not preceded by a short syllable 
	if word.endswith("e") and ((R2 and word[R2:].endswith("e")) or (R1 and word[R1:].endswith("e") and is_short(word[:-1], None))):
		word = word[:-1]
	#l - delete if in R2 and preceded by l 
	if word.endswith("l") and (R2 and word[-2] == 'l'):
		word = word[:-1]
	
	return word.lower()
	
		
	
