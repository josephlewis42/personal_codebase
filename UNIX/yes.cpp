/**
 * A utility that emulates the UNIX command "yes", repeating the input
 * until killed.
 * 
 * Used in places like Jurassic Park (the movie) when Nedry leaves a 
 * trap that outputs the string "You didn't say the magic word!" over
 * and over.
 * 
 * Copyright 2011-12-23 Joseph Lewis <joehms22@gmail.com>
 */

#include <iostream>

using namespace std;

int main(int nargs, char* vargs[])
{
	string s;
	
	for(int i = 0; i < nargs - 1; i++)
	{
		if(i != 0)
			s += " ";
		s += vargs[i + 1];
	}
	s += "\n";
	
	while(true)
	{
		cout << s;
	}
}
