/**
  discard.js - A Node.js implementation of the discard protocol RFC 863
  
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
//An implementation of the discared protocol RFC 863
var net = require('net');
var dgram = require('dgram');

var tcpserver = net.createServer(function(socket) { })
var udpserver = dgram.createSocket("udp4", function(msg, rinfo) { });

//Bind and serve
tcpserver.listen(8009, "127.0.0.1");
udpserver.bind(8009, "127.0.0.1");