#!/usr/bin/env python
''' Provides a database for games

Copyright (c) 2011 Joseph Lewis <joehms22@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

import games_db
import game_searcher
import codescraper
import re
import email_fetch

gs = game_searcher.GameSearcher()
ef = None
sofar = 0  #served so far

inst = '''
<span style="text-align: center;"><h1>Game Bot</h1></span>

<p>Thank you for using GAME BOT, the best (and probably only) automated 
game fetching service in the world. The game you requested has been 
attached, if nothing attached, GAME BOT couldn't find the game you requested.</p>

<p><i>Sharing is caring!</i> Please forward these games to your allies, rather than
having them download from GAME BOT so we can keep bandwidth costs down.</p>

<p>Better yet, just start an email account (we suggest Gmail) which you 
and your friends share the password to, then use it to fetch and store
games you all like, creating a private, secure, game collection.</p>


<hr>
<h3> FAQs </h3>
<p>
Q: This isn't the game I asked for, what happened?<br>
A: GAME BOT is after all a computer, and sometimes it gets fooled.<br>
<br>
Q: How do I use GAME BOT?<br>
A: Send GAME BOT an email message where the subject is the game you 
 want to play, GAME BOT will find it on the Internet and send it 
 back to you soon.<br>
<br>
Q: Who actually owns these games?<br>
A: All games are Copyright their respective creators, GAME BOT simply
 passes what is already available on the Internet on to you.<br>
<br>
Q: How do I contribute?<br>
A: In the future GAME BOT may ask you to complete a survey, that will
 pay the maker of GAME BOT to keep it running and updated, but for 
 now, just enjoy it :)<br> 
<br>
Q: How do I play these games?<br>
A: Download the file attached, then open it up in Firefox, Internet Explorer, 
 Chrome, or any other Flash enabled web browser.<br>
<br>
Q: The game attached does not work, why?<br>
A: Some game authors only allow their games to be played on the sites
they put them on, there is nothing GAME BOT can do about this.<br>
</p>
'''

def __clean_name(name):
    return re.sub('[^a-z1-9\w+]', '', name.lower().strip())

def fetch_game(name):
    print "Looking for: %s" % (name)
    bin = games_db.find(name)
    if bin:
        print "   > Found in database."
        return bin
    else:
        try:
            name = __clean_name(name)
            gs.search_for_games(name)
            game_loc = gs.get_next_game()
            
            print "   > Finding online at: %s" % (game_loc)
            
            games_db.add(name, codescraper.fetch_page(game_loc))
            
            return games_db.find(name)
        except game_searcher.NoResultsException:
            return None

def build_body():
    '''Builds the body of the message.'''
    body = inst + '''
<hr>
<h3> Random Games You Might Like </h3>

<ul>
'''
    
    for i in games_db.random_names():
        body += " <li> "+ i + "</li>"
    
    body += "</ul>"
    return body


def mail_caller(msg):
    global sofar
    j = email_fetch.SimpleMessage(msg)
    sofar += 1
    
    print ("%s : %s is searching for: %s" % (sofar, j.personfrom, j.subject))
    
    game = fetch_game(j.subject)
    
    attach = {}
    if game != None:
        attach['%s.swf' % (__clean_name(j.subject))] = game
    
    ef.send_mail(j.personfrom, j.subject, build_body(), full_attachments=attach)
    

if __name__ == "__main__":
    
    #while 1:
    #    fetch_game(raw_input("What game do you want? "))
    email_fetch.DEBUG = True  #turn on debugging for email fetch (verbose mode)

    print "If this is your first time running the server, please configure"
    print "it using config_file.ini, config_file.ini is already set up for"
    print "gmail (just change your email and password!)"
    ef = email_fetch.EmailInterface(time=3, callback=mail_caller)
    
    #Have the email fetcher set up by the ini file.
    import ini_reader
    ini_reader.setup_fetcher(ef)
    
    try:
        ef.run()
    except KeyboardInterrupt:
        print "Server terminated, bye."