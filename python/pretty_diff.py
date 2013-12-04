'''
Generates a diff when given two arguments, and opens the web browser to display
it.

Copyright (c) 2013, Joseph Lewis III <joseph@josephlewis.net> | <joehms22@gmail.com>
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

    Redistributions of source code must retain the above copyright notice, this 
    list of conditions and the following disclaimer.
    
    Redistributions in binary form must reproduce the above copyright notice, 
    this list of conditions and the following disclaimer in the documentation 
    and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND 
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED 
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES 
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; 
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON 
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT 
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS 
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

import difflib
import sys
import webbrowser
import sys
import tempfile

def generate_diff(lines1, lines2):
	'''Generates a pretty diff and opens the system web browser to show it.
	
	lines1 - a list of strings for the first file's lines.
	lines2 - a list of strings for the second file's lines.
	'''
	
	diff = difflib.HtmlDiff().make_file(fromlines, tolines, "Original", "New")
	
	with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as tmp:
		tmp.writelines(diff)
		webbrowser.open(tmp.name)

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print("usage: {} original_file new_file".format(sys.argv[0]))
		exit(2)

	fromlines = open(sys.argv[1], 'U').readlines()
	tolines = open(sys.argv[2], 'U').readlines()

	generate_diff(fromlines, tolines)
