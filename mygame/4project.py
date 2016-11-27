# George Lu
# geolu
# SI 206
# Project 4

import pygame
from pygame import *
from pygame.sprite import *
from random import *
from pygame.locals import Rect, DOUBLEBUF, QUIT, K_ESCAPE, KEYDOWN, K_DOWN, \
K_LEFT, K_UP, K_RIGHT, KEYUP, K_LCTRL, K_RETURN, FULLSCREEN

#required 
pygame.init();

DELAY = 1000 # seed a timer to move sprite
bgcolor = (173, 255, 47)

# #create colors
white = (255,255,255)
black = (0,0,0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

#position vars
# x_pos = 0
# y_pos = 0
# x_delta = 0
# y_delta = 0
clock = pygame.time.Clock()

#create a surface
screen = display.set_mode((800,800)) #initialize with a tuple
#lets add a title, aka "caption"
display.set_caption("George Lu's SI 206 Project 4")
display.update() #only updates portion specified


class Enemy(Sprite):
	def __init__(self):
		Sprite.__init__(self)
		self.image = image.load("gold.bmp").convert_alpha()
		self.rect = self.image.get_rect()

	# move gold to a new random location
	def move(self):
		randX = randint(0, 600)
		randY = randint(0, 600)
		self.rect.center = (randX,randY)

class Player(Sprite):
	def __init__(self):
		Sprite.__init__(self)
		self.image = image.load("shovel.gif").convert()
		self.rect = self.image.get_rect()
		self.x_pos = 0
		self.y_pos = 0
		self.x_delta = 5
		self.y_delta = 5

	# did player collide with an enemy?
	def hit(self, target):
		return self.rect.colliderect(target)



f = font.Font(None, 50)

# create the mole and shovel using the constructors
enemy = Enemy()
player = Player()

# creates a group of sprites so all can be updated at once
sprites = RenderPlain(enemy, player)

hits = 0
time.set_timer(USEREVENT + 1, DELAY)

gameExit = False
while not gameExit:
	screen.fill(bgcolor)
	e = event.poll()
	
	if e.type == QUIT:
		gameExit = True

	if player.hit(enemy):
		mixer.Sound("cha-ching.wav").play()
		enemy.move()
		hits += 1

		# reset timer
		time.set_timer(USEREVENT + 1, DELAY)

	if e.type == KEYDOWN:
		print("KEY!")
		if e.key == K_LEFT:
			player.x_pos -= 10;
			# player.rect.center = (player.x_pos, player.y_pos)
		if e.key == K_RIGHT:
			player.x_pos += 10;
			# player.rect.center = (player.x_pos, player.y_pos)
		if e.key == K_UP:
			player.y_delta -= 10
		if e.key == K_DOWN:
			player.y_delta += 10

	player.x_pos += player.x_delta
	player.y_pos += player.y_delta
	player.rect.center = (player.x_pos, player.y_pos)

	# if e.type == USEREVENT + 1: # TIME has passed
	# 	print("hi")
	# 	enemy.move()

	# player.x_pos += player.x_delta
	# player.y_pos += player.y_delta
	# #screen.fill(red, rect=[x_pos,y_pos, 20,20])
	# screen.fill(red, rect=[player.x_pos, player.y_pos, 20, 20])

	time_text = f.render("Enemy Collisions: " + str(hits), False, (0,0,0))
	# time_text = f.render("Time Elapsed:", str(time_alive))
	screen.blit(time_text, (360, 0))
	# update and redraw sprites
	sprites.update()
	sprites.draw(screen)
	display.update()

#required
pygame.quit()
quit() #exits python
