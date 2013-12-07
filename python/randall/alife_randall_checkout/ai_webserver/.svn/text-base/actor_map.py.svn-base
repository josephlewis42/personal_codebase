#       actor_map.py -- Displays the internal map of an actor.
#
#       Copyright 2011 Joseph Lewis <joehms22@gmail.com>
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

self.send_200()

if not SESSION or 'login' not in SESSION.keys() or not SESSION['login']:
    self.wfile.write("You are not logged in...<script type='text/javascript'>window.location = 'login.py'</script>")
else:
    try:
        w = SESSION['world']
        a = SESSION['actor']
        page = w[a].internal_map.gen_HTML()
        self.wfile.write(page)

    except KeyError, e:
        self.wfile.write("Error: Couldn't find the key specified: %s" %(e))

    except Exception, e:
        self.wfile.write("Error: %s" %(e))
