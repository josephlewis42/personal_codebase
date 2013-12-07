#       login.py
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

#Check password
user_pass = {"admin":"21232f297a57a5a743894a0e4a801fc3"}

if SESSION and 'login' in SESSION.keys() and SESSION['login']:
    #Redirect to the index page if already logged in.
    self.redirect('index.py')

elif POST_DICT:
    try:
        #If the user validated correctly redirect.
        if POST_DICT['password'] == user_pass[POST_DICT['username']]:
            #Send headder
            SESSION['login'] = True
            SESSION['username'] = POST_DICT['username']
            self.redirect('index.py')
        else:
            POST_DICT = []
    except:
        POST_DICT = []

if not POST_DICT:

    self.send_200()

    page = '''
    <!--
            login.py

            Copyright 2010 Joseph Lewis <joehms22@gmail.com>

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
    -->

    <html lang="en">

    <head>
        <title>AI Webserver Login</title>
        <meta http-equiv="content-type" content="text/html;charset=utf-8" />
        <LINK REL=StyleSheet HREF="assets/login.css" TYPE="text/css"> </LINK>
        <script type="text/javascript" src="assets/jquery.js"></script>
        <script type="text/javascript" src="assets/md5.js"></script>
        <script type="text/javascript">
            function start()
            {
                $('#login').hide();
                $('#login_text').hide();
                $('#login').delay(1000).fadeIn(2000, function() {});
                $('#login_text').fadeIn(2000, function() {});
            }
            function hash()
            {
                //Hash the password before submission, not secure against
                //things like wireshark, but will at least hide plaintext. :)
                document.getElementById('pass').value = MD5(document.getElementById('pass').value);
                $('#bg').fadeOut(1000, function() {});
                $('#login').fadeOut(2000, function() {});
                $('#login_text').fadeOut(2000, function() {});
            }
          </script>
    </head>

    <body id="login_page" onLoad="start()">
        <!--Stretched background-->
        <img src="assets/earthrise.jpg" alt="background image" id="bg" />

        <h1 id="login_text">AI Webserver Login</h1>
        <!--Login form-->
        <div id="login">
            <form method="post">
                <input type="text" name="username" placeholder="Username"/> <br />
                <input type="password" id="pass" name="password" placeholder="Password"/> <br />
                <input type="submit" value="Submit" onClick="hash()"/>
            </form>
        </div>
    </html>
    </body>
    '''

    #Send body
    self.wfile.write(page)
