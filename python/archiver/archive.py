#!/usr/bin/env python

'''
Generates an "archived" version of some text by converting it to text/qr codes
in HTML.
'''

import StringIO
import urllib
import qrcode
import sys
import os
import hashlib
import datetime

CHARS_PER_SECTION = 500

def generate_file_info(filename, text):
	'''Generates file information about the file at the given path.'''
	output = "[fileinformation]\n\n"
	output += "name = {}\n".format(filename)
	output += "path = {}\n".format(os.path.abspath(filename))
	stat = os.stat(filename)
	output += "size = {}\n".format(stat.st_size)
	output += "accessed = {}\n".format(stat.st_atime)
	output += "modified = {}\n".format(stat.st_mtime)
	output += "ctime = {}\n".format(stat.st_ctime)
	output += "md5 = {}\n".format(hashlib.md5(text).hexdigest())
	output += "sha1 = {}\n".format(hashlib.sha1(text).hexdigest())
	output += "current_time = {}\n".format(datetime.datetime.now().isoformat())
	
	return output
	
def to_data_uri(pil_image):
	'''Converts a pil image to a data: URI'''
	f = StringIO.StringIO()
	pil_image.save(f, "PNG")
	return 'data:image/png,' + urllib.quote(f.getvalue())

def split_text(text, length):
	''' splits text in to sections of the given length '''
	output = []
	
	while text:
		output.append(text[:length])
		text = text[length:]
	
	return output

def bold_non_printing(text):
	
	replacedict = {	"<":"&lt;", 
					">":"&gt;", 
					"&":"&amp;", 
					"\n":"<span class='nonprinting'>[LF]</span><br/>", 
					" ":"<span class='nonprinting'>.</span><wbr>", 
					"\t":"<span class='nonprinting'>[TAB]</span>", 
					"\r":"<span class='nonprinting'>[CR]</span>" }
	
	outtext = ""
	for char in text:
		if char in replacedict:
			outtext += replacedict[char]
		else:
			outtext += char
			
	return outtext

def generate_table_row(text):
	qr = qrcode.make(text)
	bolded = bold_non_printing(text)
	return '''<tr>
				<td><p style="font-family:monospace">{}</p></td>
				<td><img width="250px" src="{}"></td>
			</tr>'''.format(bolded, to_data_uri(qr))

def generate_table_header_row(text):
	return '''<tr><th colspan='2'>{}</th></tr>'''.format(text)

def text_to_document(text, title):
	
	
	output = "<table border='1'><tbody>"
	output += generate_table_header_row("<h1>{}</h1>".format(title))
	output += generate_table_header_row("File Information")
	output += generate_table_row(generate_file_info(title, text))
	output += generate_table_header_row("Data")
	
	
	for section in split_text(text, CHARS_PER_SECTION):
		output += generate_table_row(section)
		#qr = qrcode.make(section)
		#bolded = bold_non_printing(section)
		#output += '''<tr style="page-break-inside: avoid;"><td><p style="font-family:monospace">{}</p></td><td><img width="250px" src="{}"></td></tr>'''.format(bolded, to_data_uri(qr))
	
	output += "</tbody></table>"
	return output

if __name__ == "__main__":

	print '''<html>
	<head>
	<style>
img 
{
	display:block;
	page-break-inside: avoid;
}

tr 
{
	page-break-inside: avoid;
}

th 
{
	text-align:center;
}

.nonprinting
{
	background-color:#ccc;
}
	</style>
</head>
<body>

'''
	for arg in sys.argv[1:]:
		#try:
		with open(arg) as f:
			print text_to_document(f.read(), arg)
		#except Exception:
		#	pass
	
	print '''</body></html>'''
