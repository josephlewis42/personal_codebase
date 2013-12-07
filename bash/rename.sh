#!/bin/sh
# rename.sh
# Tue 09 Nov 2010 10:02:33 AM MST
for file in ${@}; do
    if [ -e $file ]; then
        timestamp=`ls -l --time-style=+%Y-%m-%d-%H%M%S $file |cut -d' ' -f6`
        basename=`echo $file|cut -d'.' -f1`
        ext=`echo $file | cut  -d'.' -f2-`
        mv -v $file $basename_$timestamp.$ext
    fi
done
