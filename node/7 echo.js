/**
  echo.js - A Node.js implementation of the echo protocol RFC 862 
  
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

//TCP
var tcpserver = net.createServer(function (socket) {
  socket.pipe(socket);
})

//UDP
var udpserver = dgram.createSocket("udp4", function (msg, rinfo) {
  udpserver.send(msg, 0, msg.length, rinfo.port, rinfo.address);
});

//Bind and serve
tcpserver.listen(8007, "127.0.0.1");
udpserver.bind(8007, "127.0.0.1");