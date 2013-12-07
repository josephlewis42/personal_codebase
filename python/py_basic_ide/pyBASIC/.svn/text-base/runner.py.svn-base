import time
debug = False

def error_fx(text):
    '''The default error handling, print the text to the console.
    replace with your own function if you want, have it print to your
    wx application or whatever.'''
    sys.stderr.write(text)
    
def output_fx(text):
    '''The default output handling, print text to the console.
    replace with your own function if you want, like have it print to
    a text control in your wx application.'''
    print text
    
def input_fx(text):
    '''The default user input handler, use raw_input, if you like you
    can replace this with your own function, like have it read from a 
    text control.'''
    return raw_input(text)
    
def check_killed():
	'''Checks if the program was killed during execution implemented
	by pyBASIC ide to kill runaway threads.'''
	return False

def var_replace(string, var_dict):
	'''
	Replaces variables the user is using ($asdf) with python 
	understood ones ( %(asdf)s )
	'''
	terminators = [" ", ",", "\'", "\"", ".", ";", ":", "!", "?"]
	#string = string.replace("\\$", "|DOLLAR SIGN|")
	
	newstring = ""
	in_var = False
	curr_var = ""
	for char in string:
		#If we are in a var add the current char to the curr var
		if in_var and char not in terminators:
			curr_var += char
		#The start of a variable
		if char == '$':
			in_var = True
			newstring += "%("
		#The end of a var
		elif in_var == True and char in terminators:
			#Give the appropriate ending based on type
			if type(var_dict[curr_var.strip()]) == type(0.0):
				newstring+=")d"
			if type(var_dict[curr_var.strip()]) == type(0):
				newstring += ")i"
			if type(var_dict[curr_var.strip()]) == type(""):
				newstring += ")s"
			newstring += char
			curr_var = ""
			in_var = False
		else:
			newstring += char
	#if closed without finishing variable
	if in_var == True:
		#Give the appropriate ending based on type
			if type(var_dict[curr_var.strip()]) == type(0.0):
				newstring+=")d"
			if type(var_dict[curr_var.strip()]) == type(0):
				newstring += ")i"
			if type(var_dict[curr_var.strip()]) == type(""):
				newstring += ")s"
	return newstring.replace("|DOLLAR SIGN|", "$")
	
def get_labels(td):
	labeldict = {"START": 0}
	
	index = 0;
	for line in td:
		if line[0] in ["LBL", "LABEL"]:
			labeldict[line[1]] = index
		index += 1
		
	return labeldict
	
def error(str,line):
	error_fx("Error Line %d: %s" % (line, str))

def debug_msg(str):
	if debug:
		output_fx(str) 
	
def process_line(index, line, label_list, var_dict):
	'''
	Processes a line of basic to run. Returns the new index along with
	the new variable list.
	'''
	if line[0] in ["STOP"]:
		#Force out of bounds = program stops
		index = -100
	#Print statment
	if line[0] in ["PRINT"]:
		try:
			output_fx( eval(var_replace(line[1], var_dict)%(var_dict)) )
		except KeyError:
			error("No such variable", index)
		except ValueError:
			error("Value Error",index)
		except TypeError:
			error("Type Error", index)
		
	#Clear Statment
	if line[0] in ["CLEAR", "CLS"]:
		for i in range(0,100):
			output_fx("")
	#If statment
	if line[0] in ["IF"]:
		#debug_msg(var_replace(line[1], var_dict) %(var_dict))
		#debug_msg(eval(var_replace(line[1], var_dict)%(var_dict))))
		if eval(var_replace(line[1], var_dict)%(var_dict)):
			index, var_dict = process_line(index, line[2], label_list, var_dict)
		else:
			index, var_dict = process_line(index, line[3], label_list, var_dict)
		index -= 1
	#Goto Statment
	if line[0] in ["GOTO"]:
		index = label_list[line[1]] -1
		
	#Define Let Statment
	if line[0] in ["LET"]:
		try:
			mystr = var_replace(line[2], var_dict)
			
			x = eval(mystr %(var_dict))
			var_dict[line[1]] = x
		except ValueError:
			error("ValueError", index)
		except TypeError:
			error("Type Error", index)

		
	#Define Input Statment
	if line[0] in ["INPUT"]:
		x = input_fx(line[1] + "\n")
		try:
			x = float(x)
		except ValueError:
			x = str(x)
		var_dict[line[2]] = x
		
		debug_msg(var_dict)
		
	index += 1
	
	return index, var_dict

def run(td):
	'''
	Runs a BASIC program given a token document.
	'''
	debug_msg("Lines List:\n"+str(td)+"\n")
	start_time=time.time()
	index = 0 #Current line in file.
	running = True
	label_list = get_labels(td)
	var_dict = {}
	
	while running:
		try:
			line = td[index]
			
			index, var_dict = process_line(index, line, label_list, 
											var_dict)
			if check_killed():
				#Stop by making a long line
				print "Killed"
				index = len(td)
		except IndexError:
			running = False
		
	end_time=time.time()
	output_fx("\n\n")
	output_fx("--------------------------------")
	output_fx("Program exited normally.")
	debug_msg("Debug Mode ON:")
	debug_msg("Variables: " + str(var_dict))
	debug_msg("Labels: " + str(label_list))
	debug_msg("Uptime: " + str(end_time - start_time) + " seconds")
