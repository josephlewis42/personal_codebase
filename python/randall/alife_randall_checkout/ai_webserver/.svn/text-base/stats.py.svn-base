#       stats.py
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

#Handle AJAX query.
elif 'reload' in QUERY_DICT.keys():
    import time
    global last_news_time
    global current_news
    try:
        #Check for new news every ten seconds
        if last_news_time + 5 < time.time():
            last_news_time = time.time()
            current_news = SESSION['world'].item_event_interface.fetch_news()
    except NameError: #Globals not defined yet.
        last_news_time = time.time()
        current_news = SESSION['world'].item_event_interface.fetch_news()

    page = '''<h3>Recent News:</h3><p>'''
    for item in current_news:
        page += item + "<br />"
    page += "</p>"

    self.wfile.write(page)

#Handle page query.
else:
    page = '''
    <html>
    <head>
        <script type="text/javascript" src="assets/jquery.js"></script>
        <script type="text/javascript" src="assets/reloader.js"></script>
        <link rel="StyleSheet" href="assets/login.css" type="text/css" />
    </head>
    <body onLoad="javascript:Update(10000, 'body', 'stats.py?reload=true');" class="widget">
    Loading...
    </body>
    </html>
    '''
    self.wfile.write(page)
