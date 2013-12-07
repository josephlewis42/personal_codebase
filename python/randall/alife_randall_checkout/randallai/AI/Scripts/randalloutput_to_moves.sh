#!/bin/bash
#cd `dirname $0`
#ls
cat 'randalloutput' | grep -v "'" | grep Randall | grep ',' | cut -d"(" -f2 | cut -d")" -f1 | awk -F, '{ print "x"$1"y"$2"z"$3 }' > output
