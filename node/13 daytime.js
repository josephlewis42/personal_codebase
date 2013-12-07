/**
  daytime.js - A Node.js implementation of the daytime protocol RFC 867
  
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

function gettime() {
    var d = new Date();
    return d.toISOString() + "\n";
}

//TCP
var tcpserver = net.createServer(function (socket) {
  socket.end(gettime());
})

//UDP
var udpserver = dgram.createSocket("udp4", function (msg, rinfo) {
  var ret = new Buffer(gettime());
  udpserver.send(ret, 0, ret.length, rinfo.port, rinfo.address);
});

//Bind and serve
tcpserver.listen(8013, "127.0.0.1");
udpserver.bind(8013, "127.0.0.1");