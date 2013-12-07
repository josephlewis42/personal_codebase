/**
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

var http = require('http');
var util  = require('util');
var spawn = require('child_process').spawn;
  
http.createServer( function (req, res) {
    res.writeHead(200);
  
    res.write("<html><body><h1>Server Check</h1>");
  
    var ls = spawn('lsof',["-l", "-i4"]);
    
    ls.stdout.on('data', function (data) {
        var mystr = data+"";
        var output = "<table border='1px solid gray'><tr><td>PID</td><td>Service</td><td>Port</td><td>Port</td><td>Status</td></tr>"
        
        mystr = mystr.split("\n");
        
        for(line in mystr) {
          if(mystr[line].indexOf("LISTEN") != -1) {
              linesplit = mystr[line].split(/[\s]+/);              
              output += "<tr><td>"+linesplit[1]+"</td><td>"+linesplit[0];
              output += "</td><td>"+linesplit[4]+"</td><td>"+linesplit[8];
              output += "</td><td>"+linesplit[9]+"</td></tr>";
          }
        }
        res.end(output+"</table></html>");
    });
}).listen(8000);