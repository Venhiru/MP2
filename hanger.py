import engine
import random 
from string import punctuation
import pyglet
from pyglet.window import key
from pathlib import Path


bgm = pyglet.media.load('Music.mp3')
hitsound = pyglet.media.load('hitsound.wav', streaming=False)
failsound = pyglet.media.load('failsound.mp3', streaming=False)
goodsound = pyglet.media.load('goodsound.wav', streaming=False)
image = []
for x in range(0,6):
	image.append(pyglet.image.load(str(x) + 'lives.png'))

window = pyglet.window.Window(1280, 720, caption = "Oppa Hangaman Style", resizable=False)
window.set_location(130, 50)
def preload():
	x = random.randint(0,4)
	file_name, items = engine.pick_category(x)
	lives = 5
	score = 0
	return file_name,items,lives,score

def loaditem():
	global items
	current_word = engine.pick_word(items)	
	blanks = engine.string_blanks(current_word)
	guesses = []
	return current_word,blanks,guesses

def reload():
	global file_name,items,lives,score, current_word,blanks,guesses, player
	global message, blnk,check
	global show_score,blankses, category, scores, buhay, messages, hanged_man
	file_name,items,lives,score = preload()
	current_word,blanks,guesses = loaditem()
	message = ''
	blnk = ' '.join(blanks)
	check = False

	show_score = pyglet.text.Label('Your Score: {}'.format(score),font_size = 20, x=1280//2, y=720//2 - 60, anchor_x='center', anchor_y='center')
	blankses = pyglet.text.Label(blnk, font_size = 30, x=1280//2, y=300, anchor_x='center', anchor_y='center')
	category = pyglet.text.Label(file_name, font_size = 40, x=1000, y=600, anchor_x='center', anchor_y='center')
	scores = pyglet.text.Label(str(score), font_size = 20, x=270, y=600, anchor_x='center', anchor_y='center')
	#buhay = pyglet.text.Label(str(lives), font_size = 30, x=1100, y=600, anchor_x='center', anchor_y='center')
	messages = pyglet.text.Label(message, font_size = 30, x=1280//2, y=180, anchor_x='center', anchor_y='center')
	hanged_man = pyglet.sprite.Sprite(image[lives])
	hanged_man.position = (425, 325)
	category.color = (100, 200, 200, 255)
	scores.color = (123, 209, 120, 55)

title = pyglet.text.Label('Titulo ay Di Pa Alam', font_size=60, x = window.width/2, y= window.height*3/4 - 50 , anchor_x = 'center',anchor_y ='center')
title.bold =True
title.italic = True
title.color = (100,234,189,200)

intro = pyglet.text.Label('Press mo yung "space" para magstart', font_size=30, x = window.width/2, y= window.height/2-100, anchor_x = 'center',anchor_y ='center')
intro.color = (220, 100, 150, 255)

scoring = pyglet.text.Label('', font_size = 30, x=140, y=600, anchor_x='center', anchor_y='center')

#printbuhay = pyglet.text.Label('Lives left: ', font_size = 30, x=950, y=600, anchor_x='center', anchor_y='center')

ending_perfect = pyglet.text.Label('Noice Wan! Nadali mo!',font_size = 40, x=1280//2, y=720//2, anchor_x='center', anchor_y='center')
ending_notperf = pyglet.text.Label('Wala na, pinish na :(',font_size = 50, x=1280//2, y=300, anchor_x='center', anchor_y='center')
ending_notperf.color = (105,105,205,205)
try_again = pyglet.text.Label('press mo "r" kung uulit ka',font_size = 50, x=1280//2, y=220, anchor_x='center', anchor_y='center')

file_name,items,lives,score = preload()
current_word,blanks,guesses = loaditem()

message = ''
blnk = ' '.join(blanks)

show_score = pyglet.text.Label('Your Score: {}'.format(score),font_size = 20, x=1280//2, y=720//2 - 60, anchor_x='center', anchor_y='center')

blankses = pyglet.text.Label(blnk, font_size = 30, x=1280//2, y=300, anchor_x='center', anchor_y='center')

category = pyglet.text.Label(file_name, font_size = 40, x=1000, y=600, anchor_x='center', anchor_y='center')
category.color = (100, 200, 200, 255)

scores = pyglet.text.Label(str(score), font_size = 20, x=270, y=600, anchor_x='center', anchor_y='center')
scores.color = (123, 209, 120, 55)

#buhay = pyglet.text.Label(str(lives), font_size = 30, x=1100, y=600, anchor_x='center', anchor_y='center')

messages = pyglet.text.Label(message, font_size = 30, x=1280//2, y=180, anchor_x='center', anchor_y='center')

hanged_man = pyglet.sprite.Sprite(image[lives])
hanged_man.position = (425, 325)

game = False
check = False
retry = False


@window.event
def on_draw():
	global game
	window.clear()
	if retry: 
		window.clear()
		ending_notperf.draw()
		try_again.draw()
		scoring.text = 'Final Score: '
		scoring.draw()
		scores.draw()
		hanged_man.draw()
	elif game:
		category.draw()
		blankses.draw()
		scoring.text = 'Your Score: '
		scoring.draw()
		scores.draw()
		messages.draw()
		hanged_man.draw()
		#printbuhay.draw()
		#buhay.draw()
	else:
		title.draw()
		intro.draw()
	

@window.event
def on_key_press(symbol, modifiers):
	global game,check,current_word, blanks, guesses, items, score, lives,message, blnk
	global blankses, scores, messages, buhay,retry, hanged_man
	hitsound.play()
	print('key ' + str(symbol) + " was pressed (" + str(chr(symbol)) + ')')
	if retry:
		if symbol == key.R:
			retry = False
			reload()
			game = True

	elif not game:
		bgm.play()
		if symbol == key.SPACE:
			game = True
	else:
		guess = chr(symbol)
		check, message = engine.check_input(guess,current_word,guesses,blanks)
		if check:
			goodsound.play()
			blnk = ' '.join(blanks)
			score += 1
			blankses = pyglet.text.Label(blnk, font_size = 30, x=1280//2, y=300, anchor_x='center', anchor_y='center')
			scores = pyglet.text.Label(str(score), font_size = 20, x=270, y=600, anchor_x='center', anchor_y='center')
			messages = pyglet.text.Label(message, font_size = 30, x=1280//2, y=180, anchor_x='center', anchor_y='center')
			scores.color = (123, 209, 120, 55)
		else:
			failsound.play()
			lives -= 1
			buhay = pyglet.text.Label(str(lives), font_size = 30, x=1100, y=600, anchor_x='center', anchor_y='center')
			messages = pyglet.text.Label(message, font_size = 30, x=1280//2, y=180, anchor_x='center', anchor_y='center')
			hanged_man = pyglet.sprite.Sprite(image[lives])
			hanged_man.position = (425, 325)
			if lives == 0:
				game = False
				retry = True
		if '_' not in blanks:
			current_word,blanks,guesses = loaditem()
			blnk = ' '.join(blanks)
			blankses = pyglet.text.Label(blnk, font_size = 30, x=1280//2, y=300, anchor_x='center', anchor_y='center')
pyglet.app.run()