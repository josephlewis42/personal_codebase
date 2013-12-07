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

These classes are used for "reading" the program from different sources,
stdio, files, etc. If you wanted something to run on an embedded system
you'd just implement a ProgramReader that would accept data from say,
EEPROM.
**/

#ifndef READER_H
#define READER_H

#include <iostream>
#include <string>
#include <list>
#include <fstream>

class ProgramReader
{
	public:
		ProgramReader()
		{
		}
		virtual const char* read_line() = 0;
		virtual bool has_next() = 0;
		virtual void seek_begin() = 0;
};

class InputProgramReader : public ProgramReader {
		public:
		
		const char* read_line()
		{
			std::string line;
			std::getline(std::cin,line);
			return (char*)line.c_str();
		}

		bool has_next()
		{
			return true;
		}

		void seek_begin()
		{
			
		}
};

class FileProgramReader : public ProgramReader {
	public:
		FileProgramReader(const char* filename)
		{
			std::ifstream infile;
			infile.open(filename); // open file
			if(infile)
			{
				std::string s = "";
				while(getline(infile, s))
				{
					lines.push_back(s);
				}
			}
			
			seek_begin();
		}

		const char* read_line()
		{
			std::string tmp = *it;
			it++;
			return tmp.c_str();
		}
		
		bool has_next()
		{
			return it != lines.end();
		}
		
		void seek_begin()
		{
			it = lines.begin();
		}

	private:
		std::list<std::string> lines;
		std::list<std::string>::iterator it;

};

#endif 
