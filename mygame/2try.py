import pygame
from pygame import *
from pygame.sprite import *
from random import *
from pygame.locals import Rect, DOUBLEBUF, QUIT, K_ESCAPE, KEYDOWN, K_DOWN, \
K_LEFT, K_UP, K_RIGHT, KEYUP, K_LCTRL, K_RETURN, FULLSCREEN

pygame.init();

# RGB colors
white = (255,255,255)
black = (0,0,0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

#position vars
x_pos = 0
y_pos = 0
x_delta = 0
y_delta = 0
clock = pygame.time.Clock()

display_width = 800
display_height = 800
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Try Game")


class Player(object):
	def __init__(self):
		self.x_pos = 0
		self.y_pos = 0
		self.length = 20
		self.width = 20
		self.rect = pygame.Rect(self.x_pos, self.y_pos, self.length, self.width)
	def move(self, x, y):
		self.x_pos += x
		self.y_pos += y

class Enemy(Sprite):
	def __init__(self):
		Sprite.__init__(self)
		# self.image = image.load("poop.bmp").convert_alpha()
		# self.rect = self.image.get_rect()
		self.x_pos = 50
		self.y_pos = 50
		self.length = 20
		self.width = 20
		self.rect = pygame.Rect(self.x_pos, self.y_pos, self.length, self.width)

	# move gold to a new random location
	def move(self):
		randX = randint(0, display_width - 50)
		randY = randint(0, display_height - 50)
		# self.rect.center = (randX ,randY)

		self.x_pos = randX
		self.y_pos = randY
		

player = Player()
enemy = Enemy()
enemy_list = []
enemy_list.append(enemy)
sprites = RenderPlain(enemy_list)
everything = pygame.sprite.Group()

f = font.Font(None, 50)

gameExit = False
while not gameExit:
	gameDisplay.fill(white)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			gameExit = True

		for enemy in enemy_list:
			if enemy.rect.colliderect(player):
				print("woah!")
				mixer.Sound("cha-ching.wav").play()
				enemy.move()

		if event.type == pygame.KEYDOWN:
			print(event.key)
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
	
	player.x_pos += x_delta
	player.y_pos += y_delta
	if player.x_pos < 0:
		player.x_pos = 780
	elif player.x_pos > 800:
		player.x_pos = 0
	if player.y_pos < 0:
		player.y_pos = 780
	elif player.y_pos > 800:
		player.y_pos = 0
	
	# gameDisplay.fill(blue, rect=[x_pos,y_pos, 20, 20])
	if len(enemy_list) < 3 and randint(0, 50) == 5:
		enemy_list.append(Enemy())
		sprites = RenderPlain(enemy_list)
		for enemy in sprites:
			enemy.move()
	if randint(0, 20) == 5:
		for enemy in sprites:
			enemy.move()


	# show number of seconds elapsed
	time_text = f.render("Time Elapsed: " + str(pygame.time.get_ticks() / 1000), False, (0,0,0))
	gameDisplay.blit(time_text, (200, 0))


	sprites.update()
	sprites.draw(gameDisplay)
	pygame.draw.rect(gameDisplay, blue, (player.x_pos, player.y_pos, 20, 20)) # is this not using the player class?
	pygame.display.update()
	clock.tick(60)

#required
pygame.quit()
quit() #exits python
