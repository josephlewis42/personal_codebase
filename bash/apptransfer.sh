#!/bin/bash
#Script written by Joseph Lewis <joehms22@gmail.com>
#Copyright 2010
#License: Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported.
#http://creativecommons.org/licenses/by-nc-sa/3.0/
#Thu 23 Sep 2010 09:40:06 AM MDT

cd `dirname $0`

# Check for admin rights. If user is not an admin user, exit the script

if [ $UID != 0 ]
then
echo "You need to be root to run this script."
exit
fi

clear
echo "Backup Programs"
echo "==========================="
echo "1 To Backup"
echo "2 To Restore"
echo "-----------------"
read -p "? " number

clear

#Backup
if [ $number = 1 ]; then 
    dpkg --get-selections > apps.txt
fi

#Backup
if [ $number = 2 ]; then 
    dpkg --set-selections < apps.txt
    dselect update
    apt-get dselect-upgrade show
fi
