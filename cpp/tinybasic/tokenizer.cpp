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
#include "tokenizer.h"
#include <iostream>
#include "stringutils.h"
//#define DEBUG

void Tokenizer::reset()
{
	current_token = END_STATEMENT;
	current_line = 0;
	current_line_position = 0;
	m_file->seek_begin();
	curr_str = 0;
	curr_int = 0;
	varname = 'a';
	
	parse_next_token();
}

int Tokenizer::getInt()
{
	return curr_int;
}

char Tokenizer::get_variable_name()
{
	return varname;
}


const char* Tokenizer::getString()
{
	if(curr_str == 0)
		return "";
	return curr_str;
}

Tokenizer::Tokenizer(ProgramReader* pgm)
{
	current_token = END_STATEMENT; // Force a restart on next.
	m_file = pgm;
	curr_str = 0;
	current_line = 0;
	parse_next_token();
}

TOKEN Tokenizer::getToken()
{
	return current_token;
}

bool Tokenizer::isFinished()
{
	// If nothing is left in file, and this is EOL)
	return (! m_file->has_next() && current_token == END_STATEMENT) || current_token == END_PROGRAM;
}

// Reads the next token available, and sets up the variables for that.
void Tokenizer::parse_next_token()
{
	// If the current token is the end of a statement, read the next one.
	if( current_token == END_STATEMENT)
	{
		if(m_file->has_next())
		{
			#ifdef DEBUG
			std::cout << "Getting next" << std::endl;
			#endif
			
			current_line = m_file->read_line();
			current_line_position = 0;
			// Continue parsing on!
			#ifdef DEBUG
			std::cout << "Next is: " << current_line << std::endl;
			#endif
		}
		else
		{
			current_token = END_PROGRAM;
			return;
		}
	}
	// Skip all whitespace.
	while(is_whitespace(current_line[current_line_position]))
		current_line_position++;

	#ifdef DEBUG
		std::cout << "Getting next token at pos: " << current_line_position << std::endl;
		std::cout << current_line << std::endl;
		for(int i = 0; i < current_line_position; ++i)
		std::cout << " ";
		std::cout << "^" << std::endl;
	#endif
	
	// Check to see if this is the end of the statement.
	if(current_line[current_line_position] == 0)
	{
		current_token = END_STATEMENT;
		return;
	}

	
	
	// Check to see if this is a number
	if(is_digit(current_line[current_line_position]))
	{
		curr_int = 0;
		while(is_digit(current_line[current_line_position]))
		{
			curr_int *= 10;
			curr_int += to_digit(current_line[current_line_position]);

			current_line_position++;
		}
		
		current_token = NUMBER;
		return;
	}

	// Check to see if this is an operator
	current_line_position ++; // Skip past this for now, decrement later if wrong.
	switch(current_line[current_line_position - 1])
	{
		case ',':
			current_token = COMMA;
			return;
		case '+':
			current_token = PLUS;
			return;
		case '-':
			current_token = MINUS;
			return;
		case '*':
			current_token = MULTIPLY;
			return;
		case '/':
			current_token = DIVIDE;
			return;
		case '=':
			current_token = EQUALS;
			return;
		case '(':
			current_token = LPAREN;
			return;
		case ')':
			current_token = RPAREN;
			return;
		case '>':
			current_token = GREATER_THAN;
			return;
		case '<':
			current_token = LESS_THAN;
			return;
		case '\n':
			current_token = END_STATEMENT;
			return;
		default:
			current_line_position--;
			break;
	}

	// Check to see if this is a var.
	if(is_alpha(current_line[current_line_position]) &&
		! is_alpha(current_line[current_line_position + 1]))
	{
		current_token = VARIABLE;
		varname = current_line[current_line_position];


		current_line_position++;

		#ifdef DEBUG
		std::cout << "Is a variable: " << varname << std::endl;
		#endif
		return;
	}

	// Check to see if this is a string
	if(current_line[current_line_position] == '"')
	{
		int tmp = 1;

		while(current_line[current_line_position + tmp] != '"' &&
			current_line[current_line_position + tmp] != 0)
			tmp ++;
		tmp++; // advance past the final "

		delete[] curr_str;
		curr_str = 0;
		
		curr_str = substring(current_line,current_line_position + 1, tmp - 2);
		current_line_position += tmp;
		current_token = STRING;
		
		return;
	}

	// Check to see if this is a function
	if(starts_with_ignore_case(current_line, current_line_position, (char*)"PRINT"))
	{
		current_token = PRINT;
		current_line_position += 5;
		return;
	}
	if(starts_with_ignore_case(current_line, current_line_position, (char*)"IF"))
	{
		current_token = IF;
		current_line_position += 2;
		return;
	}
	if(starts_with_ignore_case(current_line, current_line_position, (char*)"THEN"))
	{
		current_token = THEN;
		current_line_position += 4;
		return;
	}
	if(starts_with_ignore_case(current_line, current_line_position, (char*)"GOTO"))
	{
		current_token = GOTO;
		current_line_position += 4;

		return;
	}
	if(starts_with_ignore_case(current_line, current_line_position, (char*)"INPUT"))
	{
		current_token = INPUT;
		current_line_position += 5;
		return;
	}
	if(starts_with_ignore_case(current_line, current_line_position, (char*)"LET"))
	{
		current_token = LET;
		current_line_position += 3;
		return;
	}
	if(starts_with_ignore_case(current_line, current_line_position, (char*)"GOSUB"))
	{
		current_token = GOSUB;
		current_line_position += 5;
		return;
	}
	if(starts_with_ignore_case(current_line, current_line_position, (char*)"RETURN"))
	{
		current_token = RETURN;
		current_line_position += 6;
		return;
	}
	if(starts_with_ignore_case(current_line, current_line_position, (char*)"CLEAR"))
	{
		current_token = CLEAR;
		current_line_position += 5;
		return;
	}
	if(starts_with_ignore_case(current_line, current_line_position, (char*)"LIST"))
	{
		current_token = LIST;
		current_line_position += 4;
		return;
	}
	if(starts_with_ignore_case(current_line, current_line_position, (char*)"RUN"))
	{
		current_token = RUN;
		return;
	}
	if(starts_with_ignore_case(current_line, current_line_position, (char*)"END"))
	{
		current_token = END;
		current_line_position += 3;
		return;
	}

	current_token = ERROR;
	
}
