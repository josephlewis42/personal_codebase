#!/usr/bin/python
'''
Copyright (c) 2010 Joseph Lewis <joehms22@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

import re
import urllib2
from xml.sax.saxutils import unescape as xmlunescape

numnones = 0

def unescape(string):
    '''Unescape the & escapes in html, like &quot; returns a string '''
    
    string = string.replace("&quot;", "\"")  #Not done by xml lib
    string = xmlunescape(string)
    
    return string
    
def remove_HTML_tags(text):
    '''Removes html tags from a supplied string.
    
    Warning: This is accomplished using regular expressions that simply cut 
    out all text in between and including less than and greater than 
    characters.
    
    '''
    
    regex_html = re.compile(r'<.*?>')
    return regex_html.sub('', text)

def fetch_page(url):
    '''Returns the html for the webpage at the supplied url.'''
    hdr = {'User-Agent': 'Mozilla/5.0 Gecko/20100101 Firefox/4.0',
      'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Language':'en-us,en;q=0.5',
      'Accept-Encoding':'none',
      'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
      'Keep-Alive':'115',
      'Connection':'keep-alive'}
    request = urllib2.Request(url, None, hdr)
    page = urllib2.urlopen(request)
    pagetext = ""
    
    for line in page:
        pagetext += line
    
    return pagetext
    
def url_content_type(url):
    from urlparse import urlparse
    o = urlparse(url)
    
    
    import httplib
    conn = httplib.HTTPConnection(o.netloc)
    conn.request("HEAD", o.path)
    res = conn.getresponse()
    
    for key, value in res.getheaders():
        if key.lower() == "content-type":
            return value
        
def return_between(first_tag, second_tag, text):
    '''Returns an array of the text between the delimiters given. All text 
    between the end and beginning delimiters will be discarded.
    
    Arguments:
    first_tag -- The tag to begin text harvesting. (string)
    second_tag -- The tag to end text harvesting.  (string)
    text -- The string in which the tags are to be found. (string)
    
    '''
    
    basic_split = text.split(first_tag)
    
    #select only the sections which contain the close tags, discard the rest.
    second_split = []
    for i in basic_split:
        if second_tag in i:
            second_split.append(i)
    
    #Cut out the text before the close tag
    between = []
    
    for line in second_split:
        value, end = line.split(second_tag, 1)
        between.append(value)
        
    return between
