from resources import engine
import random 
from string import punctuation
import pyglet
from pyglet.window import key


#loading the sound fx needed
bgm = pyglet.media.load('resources/sounds/Music.mp3')
hitsound = pyglet.media.load('resources/sounds/hitsound.wav', streaming=False)
failsound = pyglet.media.load('resources/sounds/failsound.mp3', streaming=False)
goodsound = pyglet.media.load('resources/sounds/goodsound.wav', streaming=False)

#strings/names of the images in a list
image = []
for x in range(0,6):
	image.append('resources/pic/'+str(x) + 'lives.png')

window = pyglet.window.Window(1280, 720, caption = "Oppa Hangman Style", resizable=False)
window.set_location(130, 50)

#loading new font
pyglet.font.add_file('GANG BANG CRIME.ttf')
F = pyglet.font.load('GANG BANG CRIME')

def preload():
	x = random.randint(0,4)
	file_name, items = engine.pick_category(x)
	lives = 5
	score = 0
	#reading high score from txt file
	high_score_file = open('resources/high_score.txt', 'r')
	current_high_score = int(high_score_file.readline())
	high_score_file.close()

	return file_name,items,lives,score,current_high_score
#loading the elements per items
def loaditem():
	global items
	current_word = engine.pick_word(items)	
	blanks = engine.string_blanks(current_word)
	guesses = []
	return current_word,blanks,guesses

#reloading the variables after restart/retry
def reload():
	global file_name,items,lives,score, current_word,blanks,guesses,current_high_score
	global message, blnk,check
	global blankses, category, scores, messages, hanged_man
	file_name,items,lives,score,current_high_score = preload()
	current_word,blanks,guesses = loaditem()
	message = ''
	blnk = ' '.join(blanks)
	check = False
	high_score_file = open('resources/high_score.txt', 'r')
	current_high_score = int(high_score_file.readline())
	high_score_file.close()

	blankses.text = blnk
	category.text = file_name
	scores.text = str(score)
	high_scores.text = str(current_high_score)
	messages.text = message
	hanged_man.update()
	category.color = (100, 200, 200, 255)
	scores.color = (207, 60, 25, 207)

#image object hanging man
class Image(pyglet.sprite.Sprite):
	global lives
	def __init__(self):
		self.imahe = pyglet.image.load(image[lives])
		super(Image, self).__init__(self.imahe)
		self.position = (0, 360)
	def update(self):
		self.imahe = pyglet.image.load(image[lives])
		super(Image, self).__init__(self.imahe)
		self.position = (0, 360)

#background of the game
background = pyglet.image.load('resources/pic/b.png')
back = pyglet.sprite.Sprite(background)
back.postition = (0,0)

#Title of the game
title = pyglet.text.Label('HANGER MAN', font_size=80, x = window.width/2, y= window.height*3/4 - 50 , anchor_x = 'center',anchor_y ='center')
title.bold =True
title.font_name = 'GANG BANG CRIME'
title.italic = False
title.color = (245,10,10,245)

#introductory message (instruction to start the game)
intro = pyglet.text.Label('Press mo yung "space" para magstart', font_size=30, x = window.width/2, y= window.height/2-100, anchor_x = 'center',anchor_y ='center')
intro.color = (220, 100, 150, 255)
intro.font_name = 'Arial'

#initializing for the 'Your score: ' label
scoring = pyglet.text.Label('', font_size = 30, x=1000, y=600, anchor_x='center', anchor_y='center')

#label for completing a set of game
ending_perfect = pyglet.text.Label('Noice Wan! Nadali mo!',font_size = 50, x=1280//2, y=300, anchor_x='center', anchor_y='center')

#label for not completing a set of game
ending_notperf = pyglet.text.Label('Wala na, pinish na :(',font_size = 50, x=1280//2, y=300, anchor_x='center', anchor_y='center')
ending_notperf.color = (105,105,205,205)

#label asking the user to retry, instructions also
try_again = pyglet.text.Label('press mo "r" kung uulit ka',font_size = 50, x=1280//2, y=220, anchor_x='center', anchor_y='center')

#loading the variable needed
file_name,items,lives,score,current_high_score = preload()
current_word,blanks,guesses = loaditem()

message = ''
blnk = ' '.join(blanks)

#The blanks in the main game
blankses = pyglet.text.Label(blnk, font_size = 30, x=1280//2, y=300, anchor_x='center', anchor_y='center')

category = pyglet.text.Label(file_name, font_size = 55, x=1280//2, y=480, anchor_x='center', anchor_y='center',bold = True)
category.color = (100, 200, 200, 255)

#Actual score of the player
scores = pyglet.text.Label(str(score), font_size = 40, x=1130, y=600, anchor_x='center', anchor_y='center', bold = True)
scores.color = (207, 60, 25, 207)

#showing messages if the player's input is correct or wrong
messages = pyglet.text.Label(message, font_size = 30, x=1280//2, y=180, anchor_x='center', anchor_y='center')

#shows "High score: " label
high_scoring = pyglet.text.Label('High Score: ', font_size = 24, x=975, y=650, anchor_x='center', anchor_y='center')

#shows actual high score
high_scores = pyglet.text.Label(str(current_high_score), font_size = 28, x=1085, y=650, anchor_x='center', anchor_y='center', bold = True)
high_scores.color = (60, 25, 207, 207)

game = False
check = False
retry = False
win = False

hanged_man = Image()

@window.event
def on_draw():
	global game
	window.clear()
	if retry: 
		back.draw()
		ending_notperf.draw()
		try_again.draw()
		scoring.text = 'Final Score: '
		scoring.font_size = 50
		scoring.x = 1280//2
		scoring.y = 450
		scoring.draw()
		scores.font_size = 70
		scores.x=865
		scores.y=450
		scores.draw()
		high_scoring.draw()
		high_scores.draw()
		hanged_man.draw()
	elif win:
		back.draw()
		ending_perfect.draw()
		try_again.draw()
		scoring.text = 'Final Score: '
		scoring.font_size = 50
		scoring.x = 1280//2
		scoring.y = 450
		scoring.draw()
		scores.font_size = 70
		scores.x=865
		scores.y=450
		scores.draw()
		hanged_man.draw()

	elif game:
		back.draw()
		category.draw()
		blankses.draw()
		scoring.text = 'Your Score: '
		scoring.font_size = 30
		scoring.x=1000
		scoring.y=600
		scoring.draw()
		scores.font_size = 40
		scores.x=1130
		scores.y=600
		scores.draw()
		high_scoring.draw()
		high_scores.draw()
		messages.draw()
		hanged_man.draw()

	else:
		back.draw()
		title.draw()
		intro.draw()
	

@window.event
def on_key_press(symbol, modifiers):
	global game,check,current_word, blanks, guesses, items, score, lives,message, blnk
	global blankses, scores, messages, retry, hanged_man,win,current_high_score
	hitsound.play()
	print('key ' + str(symbol) + " was pressed (" + str(chr(symbol)) + ')')
	if retry: #reloading the game
		if symbol == key.R:
			retry = False
			win = False
			reload()
			game = True
	elif win:#reloading the game after winning
		if symbol == key.R:
			retry = False
			win = False
			reload()
			game = True
	elif not game: #Starting the game
		bgm.play()
		if symbol == key.SPACE:
			game = True
	else:
		guess = chr(symbol)
		check, message = engine.check_input(guess,current_word,guesses,blanks)
		if check: #checking the input of the player
			goodsound.play()
			blnk = ' '.join(blanks)
			score += 1
			blankses.text = blnk
			scores.text = str(score)
			messages.text = message
			if '_' not in blanks and len(items) == 0: # true if the player completed a set of game
				win = True
				game = False
			elif '_' not in blanks:
				current_word,blanks,guesses = loaditem() # true if the player filled correctly a ceratin item
				blnk = ' '.join(blanks)
				blankses.text = blnk	
		else:
			failsound.play()
			lives -= 1
			messages.text = message
			hanged_man.update()
			if lives == 0:
				if score >= current_high_score:
					high_score_file = open('resources/high_score.txt', 'w')
					high_score_file.write(str(score))
					high_score_file.close()
				game = False
				retry = True
		
	
pyglet.app.run()