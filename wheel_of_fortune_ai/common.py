#!/usr/bin/env python3
'''
Provides common functions used through the similarity engines.

Author: Joseph Lewis <joseph@josephlewis.net> | <joehms22@gmail.com>
Copyright 2012, All Rights Reserved

2012-10-27 - Initial Work
'''
import re
import unittest


def document_to_terms(doc):
	'''Parses a document in to a list of strings.'''
	doc = doc.lower()
	doc = re.sub(r"""[^\w\s]+""", '', doc)
	return doc.split()

def map_item_frequency(initial_list):
	''' Maps each item in the initial list to
	the number of times it occurs in that list.
	'''
	output = {}
	
	for item in initial_list:
		try:
			output[item] += 1
		except KeyError:
			output[item] = 1
	
	return output


class TestCommon(unittest.TestCase):
       	
    def test_map_item_frequency(self):
    	self.assertEqual(map_item_frequency([1,2,3]), {1:1,2:1,3:1})
    	self.assertEqual(map_item_frequency([1,2,1]), {1:2,2:1})
    	#self.assertEqual(" hello","world")
        #self.assertRaises(TypeError, random.shuffle, (1,2,3))
        #self.assertTrue(element in self.seq)
        
    def test_document_to_terms(self):
    	doc = "Hello, world! Quoth Joe."
    	self.assertTrue(len(document_to_terms(doc)) == 4)
    	self.assertEqual(document_to_terms(doc), ["hello","world","quoth","joe"])

if __name__ == '__main__':
    unittest.main()

