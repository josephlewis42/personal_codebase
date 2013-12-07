#!/bin/bash


lastlog=$(dmesg | grep UFW\ BLOCK | tail -1)

while [ 1 -gt 0 ]; do
 
    sleep 1
    
    curlog=$(dmesg | grep UFW\ BLOCK | tail -1)
    
    if [ "$curlog" != "$lastlog" ]; then
        #get information.
        ip=$( echo $curlog | cut -d = -f5 | cut -d \  -f1)
        port=$( echo $curlog | cut -d = -f14 | cut -d \  -f1)
        portfrom=$( echo $curlog | cut -d = -f13 | cut -d \  -f1)
        lastlog=$(dmesg | grep UFW\ BLOCK | tail -1)
        
        #send message.
        notify-send "Src: $ip:$portfrom Dest: $port" -u critical -i security-low
    fi

done

echo $curlog
echo $ip
echo $port