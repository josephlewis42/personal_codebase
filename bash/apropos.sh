#!/bin/bash
#Thu 28 Oct 2010 02:57:31 PM MDT
#An interactive apropos.
hello=`zenity --text="Enter Query:" --title="Program Search" --entry`
apropos $hello | xmessage -center -file -
