#!/usr/bin/python
SHOW_ERRORS = True
import sys

def error_fx(text):
    '''The default error handling, print the text to the console.
    replace with your own function if you want, have it print to your
    wx application or whatever.'''
    sys.stderr.write(text)
    
def show_error(text):
	'''
	Send an error if SHOW_ERRORS = True
	'''
	if SHOW_ERRORS:
		error_fx(text)

def split_text(text, seperator=" "):
	return get_word(text, seperator)

def get_word(text, seperator=" "):
	'''
	Returns the beginning and end of text seperated around seperator.
	If seperator is not found, the tail will be a blank string.
	'''
	try:
		head = text[0:text.index(seperator)]
		tail = text[text.index(seperator) + len(seperator) : len(text)]
	except ValueError:
		return text, ""		
	return head.strip(), tail.strip()
	
def remove_between(text, char="\""):
	'''
	Returns a string from between the next two characters from the 
	input string, returns the head, thorax, and tail.
	Example:
	remove_between("TEST \"Hello Jane!\" said Dick.")
	("TEST ", "Hello Jane!", "said Dick.")
	'''
	head, tail = get_word(text, char)
	thorax, abdomen = get_word(tail,char)
	
	return head.strip(), thorax.strip(), abdomen.strip()
				
def has_another(text, substring):
	'''
	Tests if the text has another substring, if it does returns true,
	if else it returns false.
	'''
	try:
		text.index(substring)
		return True
	except:
		return False
	
def tokenize(line, linenumber):
	'''
	Tokenize so the runner can work and check for errors in the syntax.
	'''
	word_list = [] #Is returned with each token in a proper area. 
	
	#Get the keyword
	first_word, rest_line = split_text(line)
	first_word = first_word.upper()
	
	#Add the first word to the list for identification in runner.
	word_list.append(first_word)
	
	#Check for first keyword
	acceptable_words_list = ["PRINT", "CLS", "IF", "GOTO", \
							 "LABEL", "INPUT", "LET", "REM", \
							 "END", "STOP", "", "CLEAR", "LBL"]
	
	if first_word not in acceptable_words_list:
		show_error("Token error line %d, %s is not a valid token."
						%(linenumber, first_word))
		
	#Tokenize the rest of the line based off of first keyword.
	
	"""
	If statment:
	["IF", "EXPRESSION", "THEN STATMENT", "ELSE STATMENT"]
	
	Example
	IF y=='' THEN PRINT 'Hello'
	Is formatted as.
	["IF", "%(y)s == ''", "PRINT 'Hello'", "PRINT 'Goodbye'"]
	The else is optional.
	"""
	if first_word in ["IF"]:
		#Check for syntax errors
		if not has_another(rest_line, "THEN"):
			show_error("IF error line %d, no THEN statment."%(linenumber))
		
		expression, tail = get_word(rest_line, "THEN")
		word_list.append(expression)
		if not has_another(rest_line, "ELSE"):
			#if no else
			word_list.append( tokenize(tail, linenumber) )
			word_list.append( tokenize("REM Nothing", linenumber) )
		else:
			#If there is an else still.
			then, rest = get_word(tail, "ELSE")
			word_list.append( tokenize(then, linenumber) )
			word_list.append( tokenize(rest, linenumber) )

	#Let
	if first_word in ["LET"]:
		if not has_another(rest_line, "="):
			show_error("LET error line %d, no assignment operator after variable." %(linenumber))
		else:
			head, tail = get_word(rest_line, "=")
			word_list.append(head)
			word_list.append(tail)
	
	#Input
	if first_word in ["INPUT"]:
		a,b,c = remove_between(rest_line, "\"")
		if a != "":
			show_error("INPUT error line %d, too many tokens before String." %(linenumber))
		if has_another(c, " "):
			show_error("INPUT error line %d, extra tokens found after variable." %(linenumber))
		if c == "":
			show_error("INPUT error line %d, no assignment variable." %(linenumber))
		word_list.append(b)  #User Display Text
		word_list.append(c)  #Variable
	
	#Rem
	if first_word in ["REM"]:
		word_list.append(rest_line)
	
	#End
	if first_word in ["END"]:
		if rest_line != "":
			show_error("END error line %d, too many tokens after END." %(linenumber))
	
	#Stop
	if first_word in ["STOP"]:
		if rest_line != "":
			show_error("STOP error line %d, too many tokens after STOP." %(linenumber))
			
	#gosub
	
	#Goto Statment
	if first_word in ["GOTO"]:
		if has_another(rest_line, " "):
			show_error("GOTO error line %d, too many tokens after GOTO" %(linenumber))
		else:
			word_list.append(rest_line)
			
	#PRINT Statment
	if first_word in ["PRINT"]:
			word_list.append(rest_line)
			
	#Clear statment
	if first_word in ["CLS", "CLEAR"]:
		if rest_line != "":
			show_error("CLEAR/CLS error line %d, too many tokens after CLEAR/CLS." %(linenumber))
	
	#LABEL statment
	if first_word in ["LABEL", "LBL"]:
		if has_another(rest_line, " "):
			show_error("LABEL/LBL error line %d, too many tokens after LABEL/LBL." %(linenumber))
		else:
			word_list.append(rest_line)
	
	#Return the list of tokenized words
	return word_list
	
def tokenize_document(text):
	'''
	Create a token list of a document with newline characters.
	'''
	tokens = []
	tokenlines = text.split("\n")
	index = 1
	for line in tokenlines:
		t = tokenize(line, index)
		if t != [""]:
			tokens.append(t)
		index += 1
	return tokens
	
def tokenize_from_file(path):
	'''
	Create a basic token list from a document.
	'''
	text = ""
	a = file(path)
	for line in a:
		text += line
	return tokenize_document(text)
