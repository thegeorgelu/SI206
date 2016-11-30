import pygame
from pygame import *
from pygame.sprite import *
from random import *
import math
from pygame.locals import Rect, DOUBLEBUF, QUIT, K_ESCAPE, KEYDOWN, K_DOWN, \
K_LEFT, K_UP, K_RIGHT, KEYUP, K_LCTRL, K_RETURN, FULLSCREEN, K_SPACE

pygame.init();

# RGB colors
white = (255,255,255)
black = (0,0,0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
violet = (238, 130, 238)
medium_violet = (219, 112, 147)
violet_red = (208, 32, 144)

#position update vars
x_delta = 0
y_delta = 0
clock = pygame.time.Clock()

display_width = 800
display_height = 800
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Survival Game")

class Player(Sprite):
	def __init__(self):
		self.x_pos = 400
		self.y_pos = 400
		self.length = 20
		self.width = 20
		self.rect = pygame.Rect(self.x_pos, self.y_pos, self.length, self.width)

		self.lives = 10
		self.points = 0

	def move(self, x, y):
		self.rect.x += x
		self.rect.y += y

	def check_collision(self, sprite1, sprite2):
		col = pygame.sprite.collide_rect(sprite1, sprite2)
		if col == True:
			return True
		return False

class BadBlock(Sprite):
	def __init__(self):
		Sprite.__init__(self)
		self.x_pos = 600
		self.y_pos = 400
		self.length = 20
		self.width = 20
		self.rect = pygame.Rect(self.x_pos, self.y_pos, self.length, self.width)

	def move(self):
		randX = (randint(20, display_width - 20) // 20) * 20
		randY = (randint(20, display_width - 20) // 20) * 20
		self.rect.center = (randX ,randY)


class Prize(Sprite):
	def __init__(self):
		Sprite.__init__(self)
		self.x_pos = 200
		self.y_pos = 400
		self.length = 20
		self.width = 20
		self.rect = pygame.Rect(self.x_pos, self.y_pos, self.length, self.width)

	def move(self):
		randX = (randint(20, display_width - 20) // 20) * 20
		randY = (randint(20, display_width - 20) // 20) * 20
		self.rect.center = (randX ,randY)

class Enemy(Sprite):
	def __init__(self):
		Sprite.__init__(self)
		# self.image = image.load("enemy.bmp").convert_alpha()
		self.image = image.load("poop.bmp").convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.center = (400, 200)

	# move enemy sprite to a new random location
	def move(self):
		randX = randint(50, display_width - 50)
		randY = randint(50, display_height - 50)
		self.rect.center = (randX ,randY)


player = Player()

bad_block = BadBlock()
bad_block_list = []
bad_block_list.append(bad_block)

prize = Prize()

enemy = Enemy()
enemies = RenderPlain(enemy)

f = font.Font(None, 30)

pygame.mixer.music.load("soundtrack.wav")
pygame.mixer.music.set_volume(0.6)
pygame.mixer.music.play(-1)

gameExit = False
time_check = 3000
enemy_time_check = 5000
while not gameExit:
	gameDisplay.fill(white)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			gameExit = True

		if event.type == pygame.KEYDOWN:
			x_delta = 0
			y_delta = 0
			if event.key == pygame.K_LEFT:
				x_delta -= 10
			if event.key == pygame.K_RIGHT:
				x_delta += 10
			if event.key == pygame.K_UP:
				y_delta -= 10
			if event.key == pygame.K_DOWN:
				y_delta += 10

		if player.check_collision(player, enemy): # lags when hitting this guy now, not sure if i should keep it in the for loop or take it out to underneath
			print("player hit the bat!")
			mixer.Sound("enemyhit.wav").play()
			player.lives -= 3
			enemy.move()
	
	player.rect.x += x_delta
	player.rect.y += y_delta
	if player.rect.x < 0:
		player.rect.x = display_width - 20
	elif player.rect.x > display_width:
		player.rect.x = 0
	if player.rect.y < 0:
		player.rect.y = display_height - 20
	elif player.rect.y > display_height:
		player.rect.y = 0

	# check if player collides with a bad block
	for bad_block in bad_block_list:
		if player.check_collision(player, bad_block):
			print("collision!")
			mixer.Sound("badblockhit.wav").play()
			bad_block.move()
			player.lives -= 1

	# check if player collides with the prize
	if player.check_collision(player, prize):
		print("player hit the prize!")
		mixer.Sound("coin.wav").play()
		player.points += 1
		prize.move()

	# adds a new block faster and faster
	if len(bad_block_list) < 1000 and pygame.time.get_ticks() > time_check: # this way adds a new block every few seconds
		temp_bad_block = BadBlock()
		temp_bad_block.rect.x = (randint(20, display_width - 20) // 20) * 20 # this should be rounding to multiples of 20 correctly
		temp_bad_block.rect.y = (randint(20, display_height - 20) // 20) * 20
		while temp_bad_block.rect.x >= 120 and temp_bad_block.rect.x <= 650 and temp_bad_block.rect.y <= 20:
			temp_bad_block.rect.x = (randint(20, display_width - 20) // 20) * 20
			temp_bad_block.rect.y = (randint(20, display_height - 20) // 20) * 20
		bad_block_list.append(temp_bad_block)
		if pygame.time.get_ticks() < 10000:
			time_check += 800
		elif pygame.time.get_ticks() < 16000:
			time_check += 600
		elif pygame.time.get_ticks() < 22000:
			time_check += 400
		else:
			time_check += 200

	# moves the enemy faster and faster
	if pygame.time.get_ticks() > enemy_time_check:
		enemy.move()
		if pygame.time.get_ticks() < 10000:
			enemy_time_check += 8000
		elif pygame.time.get_ticks() < 26000:
			enemy_time_check += 6000
		elif pygame.time.get_ticks() < 40000:
			enemy_time_check += 4000
		else:
			enemy_time_check += 2000

	# run game over stuff
	if player.lives <= 0:
		print("game over!!!")
		print(player.points)
		gameExit = True

	# show number of seconds elapsed, number of lives, and number of points
	if player.lives > 0:
		time_text = f.render("Time Elapsed: " + str(pygame.time.get_ticks() / 1000), False, black)
		gameDisplay.blit(time_text, (120, 0))
		lives_text = f.render("Current Lives: " + str(player.lives), False, black)
		gameDisplay.blit(lives_text, (350, 0))
		points_text = f.render("Points: " + str(player.points), False, black)
		gameDisplay.blit(points_text, (550, 0))

	enemies.update()
	enemies.draw(gameDisplay)
	pygame.draw.rect(gameDisplay, blue, player.rect)
	pygame.draw.rect(gameDisplay, green, prize.rect)

	# color of bad_blocks gets more and more red as time goes on
	if pygame.time.get_ticks() < 15000:
		for bad_block in bad_block_list:
			pygame.draw.rect(gameDisplay, violet, bad_block.rect)
	elif pygame.time.get_ticks() < 30000:
		for bad_block in bad_block_list:
			pygame.draw.rect(gameDisplay, medium_violet, bad_block.rect)
	elif pygame.time.get_ticks() < 45000:
		for bad_block in bad_block_list:
			pygame.draw.rect(gameDisplay, violet_red, bad_block.rect)
	else:
		for bad_block in bad_block_list:
			pygame.draw.rect(gameDisplay, red, bad_block.rect)

	pygame.display.update()
	clock.tick(30)

#required
pygame.quit()
quit() #exits python

