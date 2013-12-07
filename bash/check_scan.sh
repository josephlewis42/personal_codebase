#!/bin/bash
#
#Wed 18 Aug 2010 11:13:29 AM MDT
# Copyright (c) 2010 Joseph Lewis III <joehms22@gmail.com>
# Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php

#This software is meant to notify you when you have been portscanned, it uses
#three ports and netcat to do so.  When a person uses a basic nmap scan on your
#system, nmap only completes part of the TCP handshake, which kills netcat.  I
#discovered this quite by accident while playing with nc and nmap.  Because of 
#this your system can set up a warning system for when you get portscanned.
#I chose three ports because it seemed that it would be less likely to get false
#positives.  Occasionally this script does not work, so use at your own risk.

#The ports used, none of these should be used on your system, and all should be
#high enough to stay out of the way of any permission problems.

ONE=1024    #1024 - Reserved UDP
TWO=2002    #2002 - Secure Access Control Server (ACS) for Windows
THREE=1755  #1755 - Microsoft Media Services

echo "Checking if the ports I want to listen are open..."
echo "Checking Port $ONE"
#Check One
if nc -w 3 localhost $ONE <<< ” &> /dev/null
then 
PORT_ONE=1
echo "[ERROR]"
else 
PORT_ONE=0
echo "[OK]"
fi
#Check Two
echo "Checking Port $TWO"
if nc -w 3 localhost $TWO <<< ” &> /dev/null
then PORT_TWO=1
echo "[ERROR]"
else PORT_TWO=0
echo "[OK]"
fi
#Check Three
echo "Checking Port $THREE"
if nc -w 3 localhost $THREE <<< ” &> /dev/null
then PORT_THREE=1 
echo "[ERROR]" 
else
PORT_THREE=0 
echo "[OK]"
fi

#If all ports are open the sum of their values should be 0.
SCAN_VAL=$(($PORT_ONE+$PORT_TWO+$PORT_THREE))

if [ $SCAN_VAL = 0 ]
then
echo "Portscan Log:"
echo "============="
while [ 1 -gt 0 ]
do
nc -l $ONE | nc -l $TWO | nc -l $THREE
TIME=$(date +%F\ %T\ %Z)
echo "$TIME"

#If you have zenity installed and want to run the script as a daemon
#you can have it pop a message up in your gui, just un comment the next line.
#zenity --warning --text="You have been portscanned at $TIME." &

#If you want a notification that will appear on all of your terminals, virtual
#and real, un comment the next three lines.
#wall << end_of_file
#You have portscanned!
#end_of_file

done
else
echo "Couldn't get a lock on all ports."
fi
