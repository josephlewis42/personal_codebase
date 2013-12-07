from parser import tokenize_document, tokenize_from_file
from runner import run

def set_debug(bool):
	print "DEBUG = ", bool
	runner.debug = bool
