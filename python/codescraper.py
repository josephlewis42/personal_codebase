#!/usr/bin/python
'''Copyright 2010 Joseph Lewis <joehms22@gmail.com>

BSD License

Retrives Java code stored in an HTML page that is wrapped in <pre> tags.
'''

import re
import urllib2
import xml.sax.saxutils

numnones = 0

def unescape(string):
    '''Unescape the & escapes in html, like &quot; returns a string '''
    
    string = string.replace("&quot;", "\"")  #Not done by xml lib
    string = xml.sax.saxutils.unescape(string)
    
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
    
    page = urllib2.urlopen(url)
    pagetext = ""
    
    for line in page:
        pagetext += line
    
    return pagetext
    
def get_name(class_text):
    ''' Returns the name of the abstract, class, or interface, when given the
    text of a Java file.
    
    Returns None if the name can not be determined.
    
    Warning: Although Java classes may be named with unicode, this function 
    will only return characters A-Z, a-z, and 0-9.
    
    '''
    
    #Compile the regular expressions, they all ignore case and accept all chars.
    class_ = re.compile(r'public class (.*?) ', re.DOTALL | re.IGNORECASE)
    interface = re.compile(r'public interface (.*?) ', re.DOTALL | re.IGNORECASE)
    abstract = re.compile(r'public abstract class (.*?) ', re.DOTALL | re.IGNORECASE)
    
    #Find the name of the class/interface/abstract
    name =  class_.findall(class_text)  #Returns [] if none found

    if name == []:
        name = abstract.findall(class_text)
    
    if name == []:
        name = interface.findall(class_text)
    
    #If no name is found return None.
    if name == []:  
        return None 
        
    #Remove any remaining non a-z A-Z characters
    accepted_chars = re.compile(r'[^A-Za-z0-9]*')
    return accepted_chars.sub('', name[0])
    
    
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
    
def write_file(name, content, location, ext=".java"):
    '''Writes a file with the name given, with the content provided, to the
    location given, with the given extension.
    
    Arguments:
    name -- The name of the file to be written.
    content -- The content of the file to be written.
    location -- The folder where the file will be created/overwritten.
    
    Keyword Arguments:
    ext -- The extension for the file. (default ".java")
    
    Warning: This function will overwrite any pre-existing files without 
    giving warnings.
    
    '''
    
    if not location.endswith("/"):  #FIXME This is not cross platform!
        location = location + "/"
        
    print("Location: "+location)
        
    f = open( location + name + ext, "w" )
    f.write( content )
    f.close()
    
def main(url, output_folder):
    '''Fetches the text at the supplied url and outputs .java files of code
    between pre tags.
    
    Arguments:
    url -- The url of the page to scrape code from. (string)
    output_folder -- The directory that the java files will be created in.
    
    '''
    global numnones
    page_text = fetch_page(url)
    
    #Get the text between the pre tags
    code_and_garbage = return_between("<pre>", "</pre>", page_text)
    
    #Walk through each entry clean it, and write the source file
    for i in code_and_garbage:
        
        print i
        
        i = remove_HTML_tags(i)
        i = unescape(i)
        
        name = get_name(i)
        
        if name == None:
            write_file("None"+str(numnones), i, output_folder)
            numnones += 1
        else:
            write_file(name, i, output_folder)

if __name__ == "__main__":
    location = raw_input("Enter the url: ")
    output_folder = raw_input("Enter the folder to write to: ")
    
    main( location, output_folder )


