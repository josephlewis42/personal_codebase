#!/bin/bash
# Copyright 2011-05-14 12:12:34 Joseph Lewis <joehms22@gmail.com>
#       Redistribution and use in source and binary forms, with or without
#       modification, are permitted provided that the following conditions are
#       met:
#       
#       * Redistributions of source code must retain the above copyright
#         notice, this list of conditions and the following disclaimer.
#       * Redistributions in binary form must reproduce the above
#         copyright notice, this list of conditions and the following disclaimer
#         in the documentation and/or other materials provided with the
#         distribution.
#       * Neither the name of the  nor the names of its
#         contributors may be used to endorse or promote products derived from
#         this software without specific prior written permission.
#       
#       THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#       "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#       LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#       A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#       OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#       SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#       LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#       DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#       THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#       (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#       OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Check for proper args
if [ -z "$1" ];
then
    echo -e "Usage:\n$0 URL_TO_COPY_FROM URL_TO_COPY_TO" && exit 1
fi;

SVNFROM=$1
SVNTO=$2

echo "Fetching branch from: $SVNFROM"
echo "Copying branch to: $SVNTO"

# Set up environment.
if [ -e tempsvn ];
then
    rm -rf tempsvn
fi;

mkdir tempsvn tempsvn/download tempsvn/upload tempsvn/current
cd tempsvn

echo "Checking out current..."
svn co $SVNFROM current
HISTORY=`svn log current | grep \| | cut -d\  -f1 | sed 's/r\([0-9]*\).*/\1/' | sort -k1,1n`

# Init the new repo at the given location.
svn import upload $SVNTO -m ""
svn co $SVNTO upload

num=`echo $HISTORY | wc -w`
echo "There are $num revisions in this branch."


for REVNO in $HISTORY; do
    rm -rf download
    echo "-----------------------------------------------------------------------"
    echo "Revision: $REVNO"
    echo "Fetching..."
    ENTRIES=`svn co $SVNFROM@$REVNO download`
    CHANGES=`echo $ENTRIES | wc -l`
    echo "Found $CHANGES change(s)."
    
    echo "Change Log:"
    cd download
    LOG=`svn log -r $REVNO | grep \- -v`
    echo $LOG
    echo ""
    cd ..
    
    echo "Exporting..."
    rsync -a --exclude='.svn' download/ upload/
    
    cd upload
    
    IFS_BAK=$IFS
    IFS=$'\n'
    for E in $ENTRIES; do
        BEGIN=`echo $E | cut -d\  -f1`
        END=`echo $E | cut -d\  -f5- | cut -d/ -f2-`
        
        case "$BEGIN" in
        'A') svn add -q $END ;;
        'D') svn del $END ;;
        esac
    done
    IFS=$IFS_BAK
    
    if [ -e log.log ]; then rm log.log; fi;
    
    echo $LOG > log.log
    echo "Commiting new..."
    svn commit -F log.log 
    cd ..
done
# Tear down environment.
cd ..
rm -rf tempsvn