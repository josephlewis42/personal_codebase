/**
 * A copy of the "echo" command on UNIX, missing a few options, but it
 * does what is normally asked of it.
 * 
 * Copyright 2011-12-23 Joseph Lewis <joehms22@gmail.com>
 */
#include <iostream>

using namespace std;

int main(int nargs, char* vargs[])
{
	for(int i = 0; i < nargs - 1; i++)
	{
		if(i != 0)
			cout << " ";
		cout << vargs[i + 1];
	}
	cout << "\n";
}
