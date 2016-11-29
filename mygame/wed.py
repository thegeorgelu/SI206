import pygame
from pygame import *
from pygame.sprite import *
from random import *
from pygame.locals import Rect, DOUBLEBUF, QUIT, K_ESCAPE, KEYDOWN, K_DOWN, \
K_LEFT, K_UP, K_RIGHT, KEYUP, K_LCTRL, K_RETURN, FULLSCREEN, K_SPACE

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
pygame.display.set_caption("Survival Game")

# should i create a screen explosion the player can use once just like in the testing_pygame game?

# maybe randomly add wall objects too to make the player have to avoid them too
# 2 options
# make the player unable to go past the wall objects (so actually like wall objects)
# or make them like mines where they are stationary and the player should avoid hitting them too


class Player(Sprite):
	def __init__(self):
		self.x_pos = 400
		self.y_pos = 400
		self.length = 20
		self.width = 20
		self.rect = pygame.Rect(self.x_pos, self.y_pos, self.length, self.width)
		self.lives = 3

	def move(self, x, y):
		self.rect.x += x
		self.rect.y += y

	def check_collision(self, sprite1, sprite2):
		col = pygame.sprite.collide_rect(sprite1, sprite2)
		if col == True:
			return True
		return False

class Enemy(Sprite):
	def __init__(self):
		Sprite.__init__(self)
		self.image = image.load("enemy.bmp").convert_alpha()
		self.rect = self.image.get_rect()
		self.hits = 0

		self.explosion_sound = pygame.mixer.Sound("Arcade Explo A.wav")
		self.explosion_sound.set_volume(0.4)

	# move enemy sprite to a new random location
	def move(self):
		randX = randint(0, display_width - 50)
		randY = randint(0, display_height - 50)
		self.rect.center = (randX ,randY)

	# def kill(self):

class Wall(Sprite):
	def __init__(self):
		Sprite.__init__(self)
		self.x_pos = 400
		self.y_pos = 400
		self.length = 20
		self.width = 20
		self.rect = pygame.Rect(self.x_pos, self.y_pos, self.length, self.width)

		
player = Player()

enemy = Enemy()
enemy_list = []
enemy_list.append(enemy)

wall = Wall()
wall_list = []
wall_list.append(wall)

sprites = RenderPlain(enemy_list)
everything = pygame.sprite.Group()

f = font.Font(None, 30)

hits = 0
gameExit = False
while not gameExit:
	gameDisplay.fill(white)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			gameExit = True

		for enemy in enemy_list: # sometimes this doesn't work because it's still looping through the enemies
			if player.check_collision(player, enemy):
				print("collision!")
				mixer.Sound("cha-ching.wav").play()
				enemy.move()
				player.lives -= 1

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
			# if event.key == pygame.K_SPACE:
			# 	for enemy in enemy_list:
			# 		enemy.
	
	player.rect.x += x_delta
	player.rect.y += y_delta
	if player.rect.x < 0:
		player.rect.x = 780
	elif player.rect.x > 800:
		player.rect.x = 0
	if player.rect.y < 0:
		player.rect.y = 780
	elif player.rect.y > 800:
		player.rect.y = 0

	if len(enemy_list) < 5 and randint(0, 50) == 5:
		enemy_list.append(Enemy())
		sprites = RenderPlain(enemy_list)
		for enemy in sprites:
			enemy.move()
	if randint(0, 30) == 5:
		for enemy in sprites:
			enemy.move()

	if player.lives == 0:
		# show game over message
		myfont = pygame.font.SysFont("monospace", 15)
		label = myfont.render("GAME OVER!!!", 1, red)
		gameDisplay.blit(label, (400, 400))
		gameExit = True
		# sys.exit()

	# show number of seconds elapsed
	time_text = f.render("Time Elapsed: " + str(pygame.time.get_ticks() / 1000), False, (0,0,0))
	gameDisplay.blit(time_text, (300, 0))
	lives_text = f.render("Current Lives: " + str(player.lives), False, (0,0,0))
	gameDisplay.blit(lives_text, (300, 30))

	sprites.update()
	sprites.draw(gameDisplay)
	pygame.draw.rect(gameDisplay, blue, player.rect)

	pygame.draw.rect(gameDisplay, red, wall.rect)


	pygame.display.update()
	clock.tick(60)


#required
pygame.quit()
quit() #exits python
