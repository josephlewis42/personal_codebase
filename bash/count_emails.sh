#!/bin/bash
#2010-11-21  Counts the number of messages in saved html files from Gmail.

#Number of multiple emails
cat *.html | grep messages\<\/font\> | cut -d'>' -f2 | cut -d' ' -f1 > /tmp/tmp.txt

#Number of single emails
singles=`cat *.html | grep message\<\/font\> | wc -l`

#Tally up the number of multiples
value=0
while read var
do
value=`expr $value + $var`
done < /tmp/tmp.txt

#Add the number of singles.
value=`expr $value + $singles`

echo $value
