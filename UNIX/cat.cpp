/**
 * A copy of the "cat" command on UNIX, missing a few options, but it
 * does what is normally asked of it (reading files).
 * 
 * About 1/4 the size of the GNU one without stripping.
 * 
 * Copyright 2012-01-25 Joseph Lewis <joehms22@gmail.com>
 */
#include <iostream>
#include <fstream>
#include <string.h>
#include <stdio.h>
using namespace std;

int main(int nargs, char* vargs[])
{
	// General help behaviour.
	if(strcmp(vargs[0],"--help") == 0 || strcmp(vargs[0], "-h") == 0)
	{
		cout << "Usage: " << vargs[0] << " filename [filename ...]" << endl;
		cout << "\tPrints the contents of the given file(s)" << endl;
		return 1;
	}
	
	// If the only arg is the program name, read from stdin.
	if(nargs == 1)
	{
		while(cin.good())
		{
			string line;
			getline(cin,line);
			cout << line << endl;
		}
		
		return 0;
	}
	
	// If the program has args, try to read the files.
	for(int i = 1; i < nargs; i++)
	{
		string line;
		ifstream myfile;
		myfile.open (vargs[i]);
		
		if(myfile.bad() || myfile.fail())
		{
			cout << "cat: "<< vargs[i] << ": No such file or directory" << endl;
		}

		while ( myfile.good() )
		{
			getline (myfile,line);
			cout << line << endl;
		}
		myfile.close();
	}
	return 0;
}
