import re

class WheelMatch:
	letters = set(['a','t','e'])
	looking = ['a','.','e','.','.','.','a']
	
	def matches(self, word):
		
		if len(word) != len(self.looking):
			return False
		
		for i, letter in enumerate(self.looking):
			if letter == '.':
				if word[i] in self.letters:
					return False
			else:
				if word[i] != letter:
					return False
		
		return True


if __name__ == "__main__":
	wm = WheelMatch()

	wordlist = open('/usr/share/dict/american-english').readlines()

	wordlist = [word.strip().lower() for word in wordlist]

	for i in range(100):
		for word in wordlist:
			if wm.matches(word):
				print words
