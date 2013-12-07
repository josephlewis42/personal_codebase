#!/usr/bin/nodejs
/**
  chargen.js - A Node.js implementation of the Character Generation
  protocol, RFC 864
  
  Copyright 2011 Joseph Lewis <joehms22@gmail.com>
  
  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.
  
  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.
  
  You should have received a copy of the GNU General Public License
  along with this program; if not, write to the Free Software
  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
  MA 02110-1301, USA.
**/

var net = require('net');
var dgram = require('dgram');

var linewidth = 72; //Width of a line of text on the console.
var str = "";

//Generate from: ! to ~
for(var i = 33; i < 127; i++) {
    str += String.fromCharCode(i);
}

//Make sure length is at least 512 bytes (max for udp)
for(var i = str.length; i < 512; i += str.length)
{
    str += str;
}


function getline(lineno) {
    return str.substr(lineno % (127 - 33), linewidth ) + "\n";
}

//TCP
var tcpserver = net.createServer(function (socket) {
    var j = 0;
    while(j < 1000)
    {
      socket.write(getline(j));
      j++;
    }
    socket.end();
})

//UDP
var udpserver = dgram.createSocket("udp4", function (msg, rinfo) {
  var ret = new Buffer(str.substr(0, Math.floor(Math.random()*(513))));
  udpserver.send(ret, 0, ret.length, rinfo.port, rinfo.address);
});

//Bind and serve (Port 19 is actual)
tcpserver.listen(8019, "127.0.0.1");
udpserver.bind(8019, "127.0.0.1");