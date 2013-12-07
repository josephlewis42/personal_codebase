REM Made by Joseph Lewis <joehms22@gmail.com>
REM (c) 2010 Joseph Lewis
REM GNU GPL V.3
CLS
INPUT "I am a computer what is your name?" name
PRINT "Hello %(name)s! You can call me Steve."
INPUT "How many stars do you want?" stars
LET numstars = 0
LET mystars = ""
LABEL beforestarcall
IF $numstars < $stars THEN GOTO addstar
PRINT "$mystars"
STOP
LABEL addstar
LET numstars = $numstars + 1.0
LET mystars = "$mystars" + "*"
GOTO beforestarcall