#!/bin/bash
cd `dirname $0`

xmessage -center -buttons ok:0,cancel:1 Recursively removing .svn folders from `pwd`

if [ $? -eq 0 ] ; then
    rm -rf `find . -type d -name .svn`
    xmessage -center "Success!"
fi
