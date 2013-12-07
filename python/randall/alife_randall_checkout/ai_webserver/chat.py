#       chat.py -- A simple chat mechanism.
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
    import time

    #If there is a global chat use it, if not init it.
    global chat
    try:
        c = chat
    except NameError:  #Not defined yet.
        chat = []

    #Handle chat text entry.
    if POST_DICT != None:
        try:
            text = POST_DICT['text']
            usr = SESSION['username']
            t = time.strftime("%b %d %H:%M:%S %Z")

            chat.insert(0, "<span style='color:#7F7F7F;'>%s</span> <b>%s &gt;</b> %s" % (t, usr, text))

            if len(chat) > 10:
                chat = chat[:10]
        except KeyError:  #The text entered must have been None.
            pass

    #Handle AJAX chat refresh query.
    if 'reload' in QUERY_DICT.keys():
        text = ""
        for i in chat:
            text += i + "<br />\n"

        page = '''<h3>Chat</h3>
                  <p style="height:80px;overflow:auto;">%s</p>
               ''' % (text)

        self.wfile.write(page)

    #Handle page query.
    else:
        self.wfile.write('''
        <html>
        <head>
            <script type="text/javascript" src="assets/jquery.js"></script>
            <script type="text/javascript" src="assets/reloader.js"></script>
            <link rel="StyleSheet" href="assets/login.css" type="text/css" />
        </head>
        <body onLoad="javascript:Update(1500, '#chatarea', 'chat.py?reload=true');" class="widget">
            <div id="chatarea"></div>
            <form method="post" width='100%' style='background-color:#FFF;'>
                <input type="text" name="text" placeholder="Enter message..."/>
                <input type="submit" value="Submit"/>
            </form>
        </body>
        </html>
        ''')