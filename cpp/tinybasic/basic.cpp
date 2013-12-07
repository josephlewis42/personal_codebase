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


This interpriter is roughly based upon the dc program as defined by
Bjarne Stroustrup in "The C++ Programming Language, Third Edition".

The language is based upon the TinyBASIC (AKA Palo Alto) dialect whose
grammar is:

line ::= number statement CR | statement CR
statement ::= PRINT expr-list
			 IF expression relop expression THEN statement
			 GOTO expression
			 INPUT var-list
			 LET var = expression
			 GOSUB expression
			 RETURN
			 CLEAR
			 LIST
			 RUN
			 END
expr-list ::= (string|expression) (, (string|expression) )*
var-list ::= var (, var)*
expression ::= (+|-|ε) term ((+|-) term)*
term ::= factor ((*|/) factor)*
factor ::= var | number | (expression)
var ::= A | B | C .... | Y | Z
number ::= digit digit*
digit ::= 0 | 1 | 2 | 3 | ... | 8 | 9
relop ::= < (>|=|ε) | > (<|=|ε) | =
(http://en.wikipedia.org/wiki/Tiny_BASIC#Tiny_BASIC_grammar)

Note that the expression evaluator could possibly be converted to a
Shunting-yard_algorithm to be more efficent.

**/
//#define INCLUDE_RUN // define to include the "run" statement

#include "basic.h"
#include "tokenizer.h"
#include "program_reader.h"
#include "io.h"
#include "stringutils.h"
#include "stack.h"

#ifdef DEBUGGING
#include <stdio.h>
#include <stdarg.h>
#endif

ProgramReader* pr;
IOHandler* io;
Tokenizer * t = 0;

bool is_finished;
int variables[26] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
int currline = 0;
int_stack* gosub_lines = 0;

bool consume(TOKEN);
int getVar(char c);
void setVar(char c, int val);
void process_line();
void process_statement();
void process_print();
void process_if();
void process_let();
void end_statement();
void process_clear();
void process_gosub();
void jump_to_line(int line);
int process_expression();
void process_return();
void error_quit(const char* msg);
void list_statement();
void process_goto();
void process_input();


void DEBUG( const char* format, ... ) {
	#ifdef DEBUGGING
    va_list args;
    fprintf( stderr, "[Debug] " );
    va_start( args, format );
    vfprintf( stderr, format, args );
    va_end( args );
    fprintf( stderr, "\n" );
    #endif
}

void run_bas(IOHandler* i, ProgramReader* p)
{
	DEBUG("run_bas()");
	if(t != 0)
		delete t;

	io = i;
	pr = p;

	io->output("TinyBASIC interpreter (c)2012 Joseph Lewis, BSD License\n");
	t = new Tokenizer(p);
	
	is_finished = false;

	while(!is_finished && !t->isFinished())
		process_line();
}

void process_line()
{
	DEBUG("process_line()");
	// Eat a line number if possible.
	if(t->getToken() == NUMBER)
		currline = t->getInt();
	consume(NUMBER);

	// Process the line statement
	process_statement();

	// Try consuming an endline if the program hasn't ended
	consume(END_STATEMENT);
}

void process_statement()
{
	DEBUG("process_statement()");

	DEBUG("Got token: %c", t->getToken());

	switch(t->getToken()) {
		case PRINT:
			consume(PRINT);
			process_print();
			break;
		case IF:
			consume(IF);
			process_if();
			break;
		case GOTO:
			consume(GOTO);
			process_goto();
			break;
		case INPUT:
			consume(INPUT);
			process_input();
			break;
		
		// Comments can be just strings.
		case STRING:
			consume(STRING);
			break;

		// Variables can be shorthanded
		case LET:
			consume(LET);
		case VARIABLE:
			process_let();
			break;
			
		case GOSUB:
			consume(GOSUB);
			process_gosub();
			break;

		case RETURN:
			consume(RETURN);
			process_return();
			break;
			
		case CLEAR:
			consume(CLEAR);
			process_clear();
			break;

		#ifdef INCLUDE_RUN
		case RUN:
			end_statement();
			break;
		#endif

		case END:
			end_statement();
			break;

		case LIST:
			consume(LIST);
			list_statement();
			break;

		// EMPTY 
		case END_STATEMENT:
			break;
			
		default:
			io->output("Couldn't find symbol:");
			io->output((char)t->getToken());
			is_finished = true;
			break;
		
	}
}


/**
 * Eats a TOKEN if it was tie desired one, otherwise returns an error.
 */
bool consume(TOKEN wanted)
{
	if(t->getToken() != wanted)
		return false;

	t->parse_next_token();
	return true;
}


/**
 * Does a print statment:
 */
void process_print()
{
	while(	t->getToken() == STRING ||
			t->getToken() == VARIABLE ||
			t->getToken() == NUMBER)
	{
		if(t->getToken() == STRING)
			io->output(t->getString());
		if(t->getToken() == VARIABLE)
			io->output(getVar(t->get_variable_name()));
		if(t->getToken() == NUMBER)
			io->output(t->getInt());

		t->parse_next_token();
		consume(COMMA);
	}
	io->output('\n');
}

/**
 * Does an if statement:
 * 		IF expression relop expression THEN statement
 */
void process_if()
{
	DEBUG("getting left");
	int left = process_expression();

	DEBUG("getting relop");
	TOKEN relop = t->getToken();
	consume(relop);

	DEBUG("getting right");
	int right = process_expression();

	bool output = false;
	switch(relop)
	{
		case EQUALS:
			output = (left == right);
			break;
		case GREATER_THAN:
			output = (left > right);
			break;
		case LESS_THAN:
			output = (left < right);
			break;
		default:
			error_quit("Unknown relop");
			return;
	}

	if(output && consume(THEN))
		process_statement();
	else // eat until we're finished.
		while(t->getToken() != END_STATEMENT)
			consume(t->getToken());
}


/**
 * factor ::= var | number | (expression)
 */
int process_factor()
{
	DEBUG("Processing factor");

	int tmp;

	switch(t->getToken())
	{
		case VARIABLE:
			tmp = getVar(t->get_variable_name());
			consume(VARIABLE);
			break;
		
		case NUMBER:
			tmp = t->getInt();
			consume(NUMBER);
			break;
		
		case LPAREN:
			consume(LPAREN);
			tmp = process_expression();
			consume(RPAREN);
			break;
		
		default:
			error_quit("invalid number");
			break;
	}

	DEBUG("\tgot factor: %i", tmp);
	return tmp;
}

/**
 *	term ::= factor ((*|/) factor)*
 */
int process_term()
{
	DEBUG("Processing term");
	int left;
	int right;
	TOKEN operation;

	left = process_factor();
	operation = t->getToken();

	while(operation == DIVIDE || operation == MULTIPLY)
	{
		consume(operation); // Eat the / or *
		right = process_factor();

		if(operation == DIVIDE)
		{
			if(right == 0)
			{
				error_quit("[divide by 0]");
				return 0;
			}
			left = left / right;
		}
		if(operation == MULTIPLY)
			left = left * right;

		operation = t->getToken();
	}
	DEBUG("Term finished");
	return left;
}

/**
 *	expression ::= (+|-|ε) term ((+|-) term)*
 */
int process_expression()
{
	DEBUG("Processing expression");
	int left;
	int right;
	TOKEN operation;

	left = process_term();
	operation = t->getToken();

	while(operation == PLUS || operation == MINUS)
	{
		consume(operation); // eat the +/-
		right = process_term();

		if(operation == PLUS)
			left = left + right;

		if(operation == MINUS)
			left = left - right;

		operation = t->getToken();
	}
	DEBUG("Processing expression finished with val: %i", left);

	return left;
}

/**
 * Does a let statment:
 *
 */
void process_let()
{
	// Get the variable name
	char c = t->get_variable_name();
	if(! consume(VARIABLE) || ! consume(EQUALS))
	{
		error_quit("Malformed Let");
		return;
	}

	setVar(c, process_expression());
}

void process_clear()
{
	io->clear_output();
}

/**
 *	goes to the given line, or quits if it isn't found.
 */
void jump_to_line(int lineno)
{
	// Reset the tokenizer to the first token in the file.
	t->reset();

	TOKEN last = END_STATEMENT;

	while(!t->isFinished())
	{
		if(last == END_STATEMENT)
			if(t->getToken() == NUMBER && t->getInt() == lineno)
			{
				currline = lineno;
				consume(NUMBER);
				process_statement();
				return;
			}
		last = t->getToken();
		t->parse_next_token();
	}
}

/**
 * GOSUB <expression>
 */
void process_gosub()
{
	DEBUG("Gosub jump to: %i", currline);
	istack::push(currline, &gosub_lines);

	jump_to_line(process_expression());
}

/**
 * GOTO <expression>
 */
void process_goto()
{
	jump_to_line(process_expression());
}

/**
 * Pops the return area off the return stack after a GOSUB.
 */
void process_return()
{
	if(! istack::is_empty(gosub_lines))
	{
		int val = istack::pop(&gosub_lines);
		jump_to_line(val);
	}
	else
	{
		error_quit("RETURN w/o GOSUB");
	}
}

void process_input()
{
	while(t->getToken() != END_STATEMENT)
	{
		if(t->getToken() != VARIABLE)
		{
			error_quit("Not a var");
			return;
		}
		io->output(t->get_variable_name());
		io->output(" ?");
		setVar(t->get_variable_name(), io->inputInt());
		consume(VARIABLE);
		consume(COMMA);
	}
}



int getVar(char c)
{
	return variables[c - 'a'];
}


void setVar(char c, int val)
{
	variables[c - 'a'] = val;
}

void error_quit(const char* msg)
{
	io->output("Error: ");
	io->output(msg);
	io->output("\n");
	is_finished = true;
}

void list_statement()
{
	io->output("[not available]");
}

void end_statement()
{
	io->output("[Finished]");
	is_finished = true;
}


int main(int nargs, const char** argv)
{
	STDIOHandler* sioh = new STDIOHandler();
	ProgramReader* b;

	DEBUG("main()");

	#ifdef FILE_READ
		// See if it is a -h or a --help
		if(nargs == 2 && starts_with_ignore_case(argv[1],0,"-"))
		{
			sioh->output("usage: basic <filename>\n");
			return 1;
		}
		
		// If there are more than 1 args assume it is a file.
		if(nargs == 2)
		{
			b = new FileProgramReader(argv[1]);
		}
		else
		{
			b = new InputProgramReader();
		}
	#else
		b = new InputProgramReader();
	#endif
	
	run_bas(sioh, b);
	return 0;
}
