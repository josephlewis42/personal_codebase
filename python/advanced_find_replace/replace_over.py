#!/usr/bin/env python
# -*- coding: latin-1 -*-
'''A handy little script that replaces files in a directory with 


Copyright 2011 Joseph Lewis <joehms22 [at] gmail com>

Originally Made: 2012-06-12

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


Potential improvements:
Allow the regex rules to also be applied only to documents with a certain structure.
Allow rules to only be done once/based upon expressions
Allow the choice of files by either entering one, or a list
'''

import os, os.path
import difflib
import webbrowser
import re
import string
import argparse
import json
import codecs

__author__ = "Joseph Lewis"
__copyright__ = "Copyright 2012, Joseph Lewis"
__license__ = "BSD"


# {string_doc_must_contain_to_do_replacement : {orig_text : replacement}
rep_rules = {}
# {string_line_must_contain_to_do_replacement : {orig_text : replacement}
line_rep_rules = {}
regx_rules = {}
changed_files = []
doc_vars = []
universal_diff = ""


# CLI vars
verbose = True
accept_all = False
show_summary = True
print_diff = False

def print_verbose(to_print):
	if verbose:
		print to_print

def do_diff(name_a, name_b, str_a, str_b):
	''' Create a diff of the given two strings, seperated based on 
	the character provided. Returns True if the revision was accepted, 
	false otherwise.
	'''
	
	global universal_diff
	
	if print_diff:
		for line in difflib.unified_diff(str_a.split('\n'), str_b.split('\n'), name_a, name_a):
			universal_diff += line + "\n"
		return True
	
	if accept_all:
		return True
	
	with codecs.open("/tmp/difflib.tmp.html",'w', encoding='utf-8') as dlt:
		dlt.write(difflib.HtmlDiff().make_file(str_a.split("\n"),str_b.split("\n"),name_a,name_b))
	
	webbrowser.open("file:///tmp/difflib.tmp.html")

	j = raw_input("Keep current? (Y|N) ")
	if len(j) > 0 and j.upper()[0] == 'Y':
		return True
	return False
 
       
check_file_prepped = False


def check_file(f, name):
	'''Checks the file for lines and replaces them.
	'''

	
	document_variables = {}
	orig_doc = f.read()
	changed_doc = orig_doc
	


	# Find variables for the document
	for match in doc_vars:
		tmp = re.finditer(match, changed_doc)
		for t in tmp:
			document_variables.update(t.groupdict())
			break
	if document_variables:
		print_verbose("Found vars: %s" % str(document_variables))
	
	# Simple replacement
	for check, replace_dict in rep_rules.items():
		if not check in orig_doc:
			continue
		
		for to_replace, replace_with in replace_dict.items():
			changed_doc = changed_doc.replace(to_replace, replace_with)
		
	# Regex dict replacement. e.g.
	# Orig: "    print "Hello: " + itema.firstname
	#			 print "From: " + itemb.fistname
	# torep: "(?P<itemname>\w+).firstname"
	# repwith: "${itemname}.lastname"
	# new:  "    print "Hello: " + itema.lastname
	#			 print "From: " + itemb.lastname"
	for to_replace, replace_with in regx_rules.items():
		try:
			to_replace = to_replace % document_variables

			for match in re.finditer(to_replace, changed_doc):
				temp_dict = match.groupdict()
				temp_dict.update(document_variables)
				
				changed_doc = changed_doc.replace(match.group(), replace_with % temp_dict)
		except KeyError:
			continue
		except Exception, ex:
			print str(ex)
			print to_replace

	# Simple replacement (lines)
	for check, replace_dict in line_rep_rules.items():
		tmpdoc = []
		for line in changed_doc.split("\n"):
			if not check in line:
				tmpdoc.append(line)
				continue
			
			for to_replace, replace_with in replace_dict.items():
				line = line.replace(to_replace, replace_with)

			tmpdoc.append(line)
		changed_doc = "\n".join(tmpdoc)


	
	if orig_doc != changed_doc:
		if do_diff(name, "Changed Version", orig_doc, changed_doc):
			return changed_doc 
	return None
	
def summarize():
	''' Shows a summary of the changed documents.'''
	if print_diff:
		print "== Diff =="
		print universal_diff
		return
	
	if not show_summary:
		return
	
	print "== Summary of Changed Files =="
	for tmp in changed_files:
		print "\t%s" % (tmp)
		
	
def save_file(location, content):
	''' Saves a file to the given location with the given content and updates
	the list of changed files.
	
	'''
	with codecs.open(location, 'w', encoding='utf-8') as curr_file:
		curr_file.write(content)
	
	changed_files.append(location)
	
			
def check_diff_dirs(dir_to_check):
	for root, dirs, files in os.walk(dir_to_check):
		for f in files:
			fullpath = os.path.join(root, f)
			print "Checking: " + fullpath
			
			ret = None
			try:
				with codecs.open(fullpath, encoding='utf-8') as curr_file:
					ret = check_file(curr_file, fullpath)
			
				if ret and not print_diff:
					save_file(fullpath, ret)
			
			except UnicodeDecodeError, ex:
				print fullpath
				print ex
				continue
	summarize()
	
def validate_regex(regex):
	'''Validates a regex, if valid return true, else false.
	
	'''
	try:
		re.compile(regex)
		return True
	except Exception, ex:
		print "Error in your REGEX: %s \n\t%s" % (regex, ex)
		return False


def load_expressions(path_to_file):
	''' The replacement filter file is in a JSON format:
	[file_version, rep_rules, regex_rules]
	
	file_version = 2.0
	rep_rules = {string_doc_must_contain_to_do_replacement : {orig_text : replacement, ...}, ...}
	regex_rules = {orig_text : replacement, ...}
	
	e.g. A file looking like:
	{
		"version":2.0, 
		"replace":{"":{"Hello":"Hola"}},
		"regex":{"(?P<greeting>\\w+), world!":"%(greeting)s, Joseph!"},
		"variables":["Hello, (?P<OrigName>\\w+)"],
		"lines":{"linecontains":{"toreplace":"replacewith"}}
	}
		
	Would produce:
		Hello, world! --> Hola, Joseph!
	
	Note: You may use variables in the regex output, and regex inputs, and replace
	input strings by including them using string vars: %(varname)s, any var not 
	found will be left.
	
	'''
	global rep_rules
	global line_rep_rules
	global regx_rules
	global doc_vars
	
	is_valid_regex = True
	
	try:
		with codecs.open(path_to_file, encoding='utf-8') as f:
			tmp_array = json.load(f)
			file_version = tmp_array['version']
			rep_rules = tmp_array['replace']
			regx_rules = tmp_array['regex']
			doc_vars = tmp_array['variables']

			if float(file_version) >= 2.0:
				line_rep_rules = tmp_array['lines']
			else:
				print "Using a 1.0 document, 2.0 is suggested."
				line_rep_rules = {}
		
		for k in regx_rules.keys():
			ret = validate_regex(k)
			if not ret:
				is_valid_regex = False
		
		for k in doc_vars:
			ret = validate_regex(k)
			if not ret:
				is_valid_regex = False
		
		if not is_valid_regex:
			print "Cannot continue with invalid regex(s)"
			exit(2)
		
		print_verbose( "== Regex Rules ==")
		for k, v in regx_rules.items():
			print_verbose("\t %s -> %s" % (k,v))
			
		print_verbose("== Variables ==")
		for k in doc_vars:
			print_verbose("\t %s" % k)
	
		for big_k, big_d in rep_rules.items():
			print_verbose("==Rules for files containing: '%s'==" % (big_k))
			for k, v in big_d.items():
				print_verbose("\t %s -> %s" % (k,v))

		for big_k, big_d in line_rep_rules.items():
			print_verbose("==Rules for lines containing: '%s'==" % (big_k))
			for k, v in big_d.items():
				print_verbose("\t %s -> %s" % (k,v))
			
	except Exception, ex:
		print "Your JSON is not properly formatted: %s" % (ex)
		exit(2)
	

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Replaces text in files based upon complex regexs', 
									epilog=load_expressions.__doc__, 
									formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument('-q', '--quiet', help="Turns off verbose debugging", action='store_true', default=False) 
	parser.add_argument('-a', '--accept', help="Automatically accept ALL file changes without showing them", action='store_true', default=False) 
	parser.add_argument('-d', '--diff_only', help="Does not change files, rather creates a universal diff and prints it to stdout (implies -a)",action='store_true', default=False) 
	parser.add_argument('--no_summary', help="Do not show a summary of the changed files.", action='store_false', default=True)
	parser.add_argument('PATH', help='the path of the directory to parse files in')
	parser.add_argument('REPLACE_PATH', help='the path of the replacement fiter')
	args = parser.parse_args()
	
	try:
		verbose = not args.quiet
		accept_all = args.accept
		show_summary = args.no_summary
		print_diff = args.diff_only
	
		if args.PATH and args.REPLACE_PATH:
			load_expressions(args.REPLACE_PATH)
			check_diff_dirs(args.PATH)
	except IOError:
		print "File given can't be found."
