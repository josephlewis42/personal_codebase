/**
A TinyBASIC derivative originally built for the Arduino.

Copyright 2012-04-07 Joseph Lewis <joehms22@gmail.com>
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

    Redistributions of source code must retain the above copyright notice,
    this list of conditions and the following disclaimer.

    Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in the
    documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


The classes in this file are used for displaying stdio, if you wanted
to port this to something, like say an Arduino, you'd need to create
one of these to handle all the keyboard and display stuff. This makes
the BASIC system very portable.
**/

#ifndef IO_H
#define IO_H

#include <iostream>

/**
 * The IOHandler is used for fetching/displaying user input/output.
 */
class IOHandler
{
	public:
		virtual void output(const char* strout) = 0;
		virtual void output(int i) = 0;
		virtual void output(char c) = 0;
		virtual int inputInt() = 0;  // Read an int from a keyboard.
		virtual void clear_output() = 0; // Clear the screen.
};

/**
 * A handler that uses stdout and stdin.
 */
class STDIOHandler : public IOHandler
{
	public:
	void output(const char* strout)
	{
		std::cout << strout;
	}

	void output(int strout)
	{
		std::cout << strout;
	}

	void output(char strout)
	{
		std::cout << strout;
	}

	void clear_output()
	{
		for(int i = 0; i < 50; ++i)
			std::cout << std::endl;
	}
	
	int inputInt()
	{
		int j = 0;

		std::cin >> j;
		return j;
	}
};

#endif 
