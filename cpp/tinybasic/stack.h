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

#ifndef STACK_H
#define STACK_H

struct int_stack;

struct int_stack
{
	int val;
	int_stack* next;

	int_stack(int v)
	:val(v)
	{}

	int_stack(int v, int_stack*n)
	{
		val = v;
		next = n;
	}
};

namespace istack
{
	bool is_empty(int_stack* i)
	{
		return i == 0;
	}

	void push(int i, int_stack** j) 
	{
		*j = new int_stack(i, *j);
	}

	int pop(int_stack** j)
	{
		int tmp = (*j)->val;
		int_stack* todel = (*j);
		*j = (*j)->next;
		delete todel;
		return tmp;
	}
};

#endif
