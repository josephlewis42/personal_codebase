#!/bin/bash

#       winebuilder.sh  -- Finds windows programs from your win partition and
#       creates desktop files for them.
#
#       Copyright 2011-01-11 Joseph Lewis <joehms22@gmail.com>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

#Check permissions.
if [ $EUID -ge 1000 ]
then
    echo "Need root permissions to run this program, exiting..."
exit
fi

WINEDIR=/media/wines
MAXDEPTH=2  #Depth to find exes in from Program Files (removes crap and speeds search)
WINEFOLDER=/etc/winebuilder
DESKTOPPATH=$WINEFOLDER/desktops  #Place to store the desktop files.
ICONPATH=$WINEFOLDER/icons  #Place to store the icons.
DEFAULTICON=/usr/share/icons/application-default-icon.png

#Clean the winedir
rm -rf $WINEFOLDER

#Set up the winedir
mkdir -p $DESKTOPPATH
mkdir -p $ICONPATH

#Find windows partitions.
parts=`cat /boot/grub/grub.cfg | grep Windows | cut -d"/" -f2- | cut -d")" -f1`
echo $parts

mkdir -p $WINEDIR
for p in $parts; do
    #Mount windows paritions.
    diskdir=$WINEDIR/$p
    mkdir -p $diskdir
    mount /$p $diskdir

    #Check to see if the partition has a program files folder, if not
    #unmount it.
    if [ ! -d $diskdir/Program\ Files ]
    then
        umount $diskdir
    else
        #Find executables in Program Files 86 if it exists and Program files otherwise.
        if [ -d $diskdir/Program\ Files\ \(x86\) ]
        then
            progs=`find $diskdir/Program\ Files\ \(x86\) -maxdepth $MAXDEPTH -name *.exe`
        else
            progs=`find $diskdir/Program\ Files -maxdepth $MAXDEPTH -name *.exe`
        fi

        oifs=$IFS
        IFS=$'\n'
        for prog in $progs; do
            echo "==================================================="
            progname=${prog##*/}
            dskname=$DESKTOPPATH/$progname.desktop
            echo "Found program: "$progname
            echo "At: "$prog

            #Find icon and save it.
            #get icons.
            tmpfolder=/tmp/$$
            rm -rf $tmpfolder
            mkdir -p $tmpfolder
            cd $tmpfolder

            #Extract icons from program to tempfolder.
            wrestool -t 14 -o $tmpfolder -x $prog
            ls $tmpfolder

            #If there is an icon, then rename and move it (choose the largest)
            if [ -n "`ls $tmpfolder`" ]
            then
                echo "Icons exist:"
                icon=`ls -S -1 $tmpfolder/*.ico | tac | tail -n 1`

                #Convert icon to png
                convert $icon output.png

                #repeat once extracted.
                icon=`ls -S -1 $tmpfolder/*.png | tac | tail -n 1`


                mv $icon $ICONPATH/$progname.png

                if [ -f $ICONPATH/$progname.png ]
                then
                    progicon=$ICONPATH/$progname.png
                else
                    progicon=$DEFAULTICON
                fi
            else
                progicon=$DEFAULTICON
            fi

            #Write .desktop files for your windows programs.
            cat > $dskname << EOF
[Desktop Entry]
Name=$progname
Exec=wine '$prog'
Categories=Application
Type=Application
StartupNotify=true
Icon=$progicon
EOF
        chmod +x $dskname
        done
        IFS=$oifs
    fi

done

#Cleanup tmp folder
rm -rf /tmp/$$

#Copy all of the desktop files to the user's applications directory.

mkdir -p ~/Applications/Windows/
cp $DESKTOPPATH/*.* ~/Applications/Windows/
sudo chmod 777 -R ~/Applications/Windows/