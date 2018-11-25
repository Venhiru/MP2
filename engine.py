import random 
from string import punctuation

files_dict = {0:'Movies.txt', 1:'Superheroes.txt', 2:'Songs.txt',3:'Celebrities.txt',4: 'TechCompanies.txt'}

punc = list(punctuation)
punc.append(' ')

def pick_category(x): #choosing a category and creating list composing of set of items in the category
	file_name = files_dict[x]
	file = open(file_name)
	items = [item.strip() for item in file.readlines()]
	file_name = ''.join(file_name[0:len(file_name)-4])
	return file_name, items

def pick_word(items_list):#choosing an item from the picked category	
	word = random.choice(items_list) 
	items_list.remove(word) #items variable should be a global variable to update its content
	return word 

def string_blanks(word):
	blanks = []
	for i in word:
		if i not in punc:
			blanks.append('_')
		else:
			blanks.append(i)
	return blanks

def check_input(guess, word,guesses,blanks):
	lword = word.lower()
	if guess.isdigit():
		return False, 'No use of numbers.'
	elif not guess.isalpha():
		return False, 'Use only the letters in the alphabet.'
	elif guess in guesses:
		return False,'You already tried that.'
	elif len(guess) > 1:
		return False, 'input single letter only!'
	elif guess.lower() in lword:
		guesses.append(guess)

		for i in range(len(word)):
			if word[i].lower() == guess:
				blanks[i] = word[i]
		return True, 'correct'

	else:
		guesses.append(guess)
		return False, 'Your guessed letter is not in the word.'