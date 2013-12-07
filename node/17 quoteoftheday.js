#!/usr/bin/nodejs
/**
  quoteoftheday.js - A Node.js implementation of the Quote Of The Day
  protocol, RFC 865
  
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

var quotes = [
    "Time is an illusion. Lunchtime doubly so.\n - Douglas Adams",
    "The quieter you become the more you can hear.\n - Baba Ram Dass",
    "Wisdom lies in knowing when to remember and when to forget.\n - Ayn Rand",  
    "Chance favors the prepared mind.\n - Louis Pasteur",
    "The advertisement is the most truthful part of a newspaper.\n - Thomas Jefferson",  
    "To communicate through silence is a link between the thoughts of man.\n - Marcel Marceau",  
    "There are periods when...to dare, is the highest wisdom.\n - William Ellery Channing"
    ];  

function getquote() {
    randno = Math.floor ( Math.random() * quotes.length ); 
    return quotes[randno] + "\n";
}

//TCP
var tcpserver = net.createServer(function (socket) {
  socket.end(getquote());
})

//UDP
var udpserver = dgram.createSocket("udp4", function (msg, rinfo) {
  var ret = new Buffer(getquote());
  udpserver.send(ret, 0, ret.length, rinfo.port, rinfo.address);
});

//Bind and serve (Port 17 is actual)
tcpserver.listen(8017, "127.0.0.1");
udpserver.bind(8017, "127.0.0.1");