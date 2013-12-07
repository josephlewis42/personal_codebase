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
**/

#ifndef TOKENIZER_H
#define TOKENIZER_H

#include "program_reader.h"

enum TOKEN
{
	PRINT = 'P',
	IF = 'I',
	THEN = 't',
	GOTO = 'G',
	INPUT = 'N',
	LET = 'L',
	GOSUB = 'S',
	RETURN = 'R',
	CLEAR = 'C',
	LIST = 'T',
	RUN = 'U',
	END = 'E',
	COMMA = ',',
	NUMBER = '#',
	STRING = 's',
	VARIABLE = 'v',
	END_STATEMENT = 'e',
	BEGIN_STATEMENT = 'b',
	END_PROGRAM = 'q',
	CHAR = 'c',
	PLUS = '+',
	MINUS = '-',
	MULTIPLY = '*',
	DIVIDE = '/',
	EQUALS = '=',
	ERROR = 'X',
	LPAREN = '(',
	RPAREN = ')',
	GREATER_THAN = '>',
	LESS_THAN = '<'
};

class Tokenizer
{
	public:
		Tokenizer(ProgramReader* pgm);
		~Tokenizer()
		{
			delete[] curr_str;
			delete[] current_line;
		}
		void parse_next_token();		// Parses the next token.
		TOKEN getToken();	// Gets the current token.
		bool isFinished();	// Gets whether or not the program has ended.
		int getInt();		// Gets the value of the current chunk as an int.
		const char* getString();
		char get_variable_name();
		void reset();	// Resets all vars and restarts the file.
		
	private:
		TOKEN current_token;
		const char* current_line;
		int current_line_position;
		ProgramReader* m_file;
		void read_next_token();

		const char* curr_str;
		int curr_int;
		char varname;
};

#endif 
