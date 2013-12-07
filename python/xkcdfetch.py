#!/usr/bin/python

import urllib2
import time
import sys

WGET = False
try:
    if sys.argv[1] == "-w":
        WGET = True
except IndexError:
    pass

for i in range(1,850):
    if i == 404:  #Skip the 404th comic which is an error 404 page.
        continue
    url = "http://xkcd.com/%i/info.0.json" % (int(i))
    comic_json = urllib2.urlopen(url)
    time.sleep(.2)
    comic = eval( comic_json.read() )

    number = comic['num']
    title  = comic['title']
    image  = comic['img']
    alt    = comic['alt']

    if WGET:  #Just list urls for wget :)
        print(image)
    else:
        print("<li><a href='%s'>%s - %s</a> - %s</li>\n" % (image, number, title, alt))