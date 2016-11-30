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

#position update vars
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

# maybe make it so you can kill off the walls? but the walls start spawning more and more so it's harder to kill them all off and avoid them
# or maybe have yellow squares spawn and you have to eat the yellow squares
# if player.rect.center == point.rect.center


# how do i move the green prize to another object FAST ENOUGH while making sure it doesn't overlap with a black square?
# im just making it random rn, but it's also hard to make the centers of each object line up exactly
# maybe i should just check if it any part of it touches any part of the other object? (fix definition of a collision in general)

class Player(Sprite):
	def __init__(self):
		self.x_pos = 400
		self.y_pos = 400
		self.length = 20
		self.width = 20
		self.rect = pygame.Rect(self.x_pos, self.y_pos, self.length, self.width)

		self.lives = 3
		self.points = 0

	def move(self, x, y):
		self.rect.x += x
		self.rect.y += y

	def check_collision(self, sprite1, sprite2):
		col = pygame.sprite.collide_rect(sprite1, sprite2)
		if col == True:
			return True
		return False

class Wall(Sprite):
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
		self.image = image.load("poop.bmp").convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.center = (400, 200)

	# move enemy sprite to a new random location
	def move(self):
		randX = randint(50, display_width - 50)
		randY = randint(50, display_height - 50)
		self.rect.center = (randX ,randY)


player = Player()

wall = Wall()
wall_list = []
wall_list.append(wall)

prize = Prize()

enemy = Enemy()
enemies = RenderPlain(enemy)

f = font.Font(None, 30)

gameExit = False
time_check = 3000
enemy_time_check = 5000
while not gameExit:
	gameDisplay.fill(white)

	for event in pygame.event.get():
		if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
			gameExit = True

		# could use a dictionary where keys are the x, y coordinates and value is the wall object
		# just check if player is on those coordinates, check if the player object is colliding with the key's wall object

		for wall in wall_list: # sometimes this doesn't work because it's still looping through the enemies
			if player.check_collision(player, wall):
				print("collision!")
				# mixer.Sound("cha-ching.wav").play()
				wall.move()
				player.lives -= 1

		if player.check_collision(player, prize):
			print("player hit the prize!")
			mixer.Sound("cha-ching.wav").play()
			player.points += 1
			prize.move()

		if player.check_collision(player, enemy):
			print("player hit the bat!")
			# mixer.Sound("cha-ching.wav").play()
			player.lives -= 1
			enemy.move()

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

	if len(wall_list) < 1000 and pygame.time.get_ticks() > time_check: # this way adds a new block every few seconds
		temp_wall = Wall()
		temp_wall.rect.x = (randint(20, display_width - 20) // 20) * 20 # this should be rounding to multiples of 20 correctly
		temp_wall.rect.y = (randint(20, display_height - 20) // 20) * 20
		while temp_wall.rect.x >= 200 and temp_wall.rect.x <= 550 and temp_wall.rect.y <= 20:
			temp_wall.rect.x = (randint(20, display_width - 20) // 20) * 20
			temp_wall.rect.y = (randint(20, display_height - 20) // 20) * 20
		wall_list.append(temp_wall)
		if pygame.time.get_ticks() < 6000:
			time_check += 8000
		elif pygame.time.get_ticks() < 12000:
			time_check += 600
		elif pygame.time.get_ticks() < 20000:
			time_check += 400
		else:
			time_check += 200


	if pygame.time.get_ticks() > enemy_time_check:
		enemy.move()
		if pygame.time.get_ticks() < 10000:
			enemy_time_check += 4000
		elif pygame.time.get_ticks() < 26000:
			enemy_time_check += 1000
		elif pygame.time.get_ticks() < 35000:
			enemy_time_check += 800
		else:
			enemy_time_check += 600


	# if len(wall_list) < 200 and randint(0, 15) == 5:
	# 	temp_wall = Wall()
	# 	temp_wall.rect.x = (randint(20, display_width - 20) // 20) * 20 # this should be rounding to multiples of 20 correctly
	# 	temp_wall.rect.y = (randint(20, display_height - 20) // 20) * 20
	# 	while temp_wall.rect.x > 300 and temp_wall.rect.x < 500:
	# 		temp_wall.rect.x = (randint(20, display_width - 20) // 20) * 20
	# 	while temp_wall.rect.y < 50:
	# 		temp_wall.rect.y = (randint(20, display_height - 20) // 20) * 20
	# 	wall_list.append(temp_wall)

	if player.lives <= 0:
		print("game over!!!")
		print(player.points)
		gameExit = True

	# show number of seconds elapsed
	time_text = f.render("Time Elapsed: " + str(pygame.time.get_ticks() / 1000), False, black)
	gameDisplay.blit(time_text, (200, 0))
	# if player.lives > 0:
	# 	lives_text = f.render("Current Lives: " + str(player.lives), False, black)
	# 	gameDisplay.blit(lives_text, (300, 30))
	if player.lives > 0:
		points_text = f.render("Points: " + str(player.points), False, black)
		gameDisplay.blit(points_text, (450, 0))

	enemies.update()
	enemies.draw(gameDisplay)
	pygame.draw.rect(gameDisplay, blue, player.rect)
	pygame.draw.rect(gameDisplay, green, prize.rect)
	for wall in wall_list:
		pygame.draw.rect(gameDisplay, violet, wall.rect)
	pygame.display.update()
	clock.tick(30)

#required
pygame.quit()
quit() #exits python
