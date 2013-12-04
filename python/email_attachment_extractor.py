#!/usr/bin/env python3

import email.parser
import os
import sys
import base64
import binascii
import sys


def extract(rootdir):
	fileList = []
	
	for root, subFolders, files in os.walk(rootdir):
		for file in files:
		    fileList.append(os.path.join(root,file))

	for path in fileList:
		if not path.endswith(".eml"):
		    continue

		fp = email.parser.BytesFeedParser()
		fp.feed(open(path, "rb").read())

		message = fp.close()
		
		print("Checking {}".format(path))

		for message in message.walk():
		    fn = message.get_filename()
		    if fn == None:
		        continue
		    try:
		        try:
		            with open(fn, 'wb') as out:
		                out.write(message.get_payload(decode=True))
		        except (TypeError, binascii.Error):
		            with open(fn, 'wb') as out:
		                print(message.get_payload())
		                out.write(bytes(message.get_payload(), message.get_charset()))
		    except Exception:
		        print("Error extracting item from {}".format(path))

if __name__ == "__main__":
	if len(sys.argv) == 1:
		print("usage: {} path/to/.eml/files".format(sys.argv[0]))
		exit(1)
	extract(sys.argv[1])
