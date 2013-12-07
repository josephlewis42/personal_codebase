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

#ifndef STRINGUTILS_H
#define STRINGUTILS_H


// Converts an a-z character to upper case.
char toUpper(char c);

/**
 *	Determines if a string, orig, starting at offset, starts with the
 * given string. e.g.
 * 	starts_with_ignore_case("Hello World",7,"world") would be true.
 */
bool starts_with_ignore_case(const char* orig, int offset, const char* test);


/**
 * Returns true if the given character is a whitespace char.
 */
bool is_whitespace(char c);

/**
 * True if the given char is an ASCII digit.
 **/
bool is_digit(char c);

/**
 * Converts the given char to a digit, assumes it is 0-9.
 **/
int to_digit(char c);

/**
 * Tests if the character after this is a-zA-Z.
 */
bool is_alpha(char c);

/**
 * Returns a substring of another string.
 **/
char* substring(const char* orig, int offset, int length);


#endif 
