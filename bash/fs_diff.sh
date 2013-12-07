#!/bin/bash
#Fri 10 Dec 2010 03:10:34 PM MST  < Actually Late november

startfolder=/

cat before < EOF

EOF

cat after < EOF

EOF

find $startfolder -type f > before
echo "Press enter when ready to stop recording and see fs differences..."
read

find $startfolder -type f > after

clear

diff before after | grep -v /proc | grep / > diff

rm before
rm after

cat diff
