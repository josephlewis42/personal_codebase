Wheel of Fortune AI
===================

This is a player for Wheel of Fortune, you input a full, known puzzle and the 
computer tries to guess. It'll return it's top ten guesses because it doesn't
know about the categories or how to remove "stupid" answers.

It uses n-grams to find words that commonly follow one another in the English
language. These can be generated from Gutenberg books, Wikipedia, etc. I believe
I got part of this list from every Simpsons script ever, the rationale being 
they would incorporate lots of pop culture that Gutenburg may not.

Example
-------

We try to get the program to guess "boy scouts of america", it gets it by the
fifth letter and is very close in the fourth but it makes a "stupid" mistake.

	$ python wheel.py
	To play, enter a full puzzle in lower case.
	The computer will output its best guesses for the puzzle.
	After that, input a letter, and the computer will guess again.
	Enter Puzzle: boy scouts of america
	the united in america (22213173)
	the united in general (22206726)
	the united in another (22202694)
	the united in january (22202174)
	the united in chicago (22201479)
	and others in america (10687426)
	and others in general (10680979)
	and others in another (10676947)
	and others in january (10676427)
	and others in chicago (10675732)
	Update puzzle <letter> (blank to end): s
	Puzzle: ... s....s .. .......
		   (boy scouts of america)
	the states to provide (22089828)
	the states to protect (22086168)
	the states to believe (22081540)
	the states to develop (22081328)
	the states to prevent (22078536)
	and starts to provide (10676952)
	and starts to protect (10673292)
	and starts to believe (10668664)
	and starts to develop (10668452)
	and starts to prevent (10665660)
	Update puzzle <letter> (blank to end): a
	Puzzle: ... s....s .. a.....a
		   (boy scouts of america)
	the series of america (22096935)
	the series of arizona (22080977)
	the series of alberta (22079243)
	the series of ammonia (22079223)
	the series of algeria (22079223)
	for sports in america (3334134)
	for sports in arizona (3314713)
	for sports in algeria (3312919)
	for sports in alberta (3312612)
	for sports in armenia (3312514)
	Update puzzle <letter> (blank to end): y
	Puzzle: ..y s....s .. a.....a
		   (boy scouts of america)
	why series of america (241336.5)
	why series of arizona (233357.5)
	why series of alberta (232490.5)
	why series of ammonia (232480.5)
	why series of algeria (232480.5)
	try series of america (134456.5)
	try series of arizona (126477.5)
	try series of alberta (125610.5)
	try series of ammonia (125600.5)
	try series of algeria (125600.5)
	Update puzzle <letter> (blank to end): b
	Puzzle: b.y s....s .. a.....a
		   (boy scouts of america)
	buy stocks in america (65124)
	buy stocks in arizona (45703)
	buy stocks in algeria (43909)
	buy stocks in armenia (43504)
	buy stocks in antigua (43490)
	bey series of america (41407.5)
	bly series of america (41362.5)
	bey series of arizona (33428.5)
	bly series of arizona (33383.5)
	boy scouts to america (33168)
	Update puzzle <letter> (blank to end): f
	Puzzle: b.y s....s .f a.....a
		   (boy scouts of america)
	buy stocks of america (61209)
	boy scouts of america (46779)
	buy stocks of arizona (45251)
	buy stocks of ammonia (43497)
	buy stocks of algeria (43497)
	buy stocks of armenia (43398)
	bey series of america (41407.5)
	bly series of america (41362.5)
	bey series of arizona (33428.5)
	bly series of arizona (33383.5)

