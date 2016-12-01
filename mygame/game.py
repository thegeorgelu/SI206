import pygame
from pygame import *
from pygame.sprite import *
from random import *
import math

# RGB colors
white = (255,255,255)
black = (0,0,0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

violet = (238, 130, 238)
medium_violet = (219, 112, 147)
violet_red = (208, 32, 144)

aqua = (127, 255, 212)
saddle_brown = (139, 69, 19)
maroon = (176, 48, 96)
forest_green = (34, 139, 34)
yellow_green = (154, 205, 50)

display_width = 800
display_height = 720
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("The Survival Game")

class Player(Sprite):
	def __init__(self):
		self.x_pos = 400
		self.y_pos = 400
		self.length = 20
		self.width = 20
		self.rect = pygame.Rect(self.x_pos, self.y_pos, self.length, self.width)

		self.health = 15
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
		randX = (randint(20, display_width - 20) // 20) * 20 # this should be rounding to multiples of 20 correctly
		randY = (randint(20, display_height - 20) // 20) * 20
		while randX >= 120 and randX <= 650 and randY <= 20:
			randX = (randint(20, display_width - 20) // 20) * 20
			randY= (randint(20, display_height - 20) // 20) * 20
		self.rect.center = (randX, randY)

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

def main():
	pygame.init();
	easy_mode_flag = True
	flashing_mode_flag = True

	#position update vars
	x_delta = 0
	y_delta = 0

	# pygame clock
	clock = pygame.time.Clock()

	credits_timer = 20000

	player = Player()

	bad_block = BadBlock()
	bad_block_list = []
	bad_block_list.append(bad_block)

	prize = Prize()

	enemy = Enemy()
	enemies = RenderPlain(enemy)

	f = font.Font(None, 30)

	# play music in the background
	pygame.mixer.music.load("soundtrack.wav")
	pygame.mixer.music.set_volume(0.6)
	pygame.mixer.music.play(-1)

	# enemy delay values
	time_check = 3000
	enemy_time_check = 5000

	update_life_1 = True
	update_life_2 = True
	update_life_3 = True
	update_life_4 = True
	update_life_5 = True

	# this gets activated once the player survives long enough in the game
	late_game_color_blocks_switch = False

	time_survived = 0
	end_points = 0

	gameExit = False
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

			# working fine for now (with the poop.bmp)
			if player.check_collision(player, enemy):
				print("player collided with the enemy!")
				mixer.Sound("enemyhit.wav").play()
				player.health -= 3
				enemy.move()
		
		player.rect.x += x_delta
		player.rect.y += y_delta
		if player.rect.x < 0:
			player.rect.x = display_width - 20
		elif player.rect.x > display_width - 20:
			player.rect.x = 0
		if player.rect.y < 0:
			player.rect.y = display_height - 20
		elif player.rect.y > display_height - 20:
			player.rect.y = 0

		# check if player collides with a bad block
		for bad_block in bad_block_list:
			if player.check_collision(player, bad_block):
				print("collision with bad block!")
				mixer.Sound("badblockhit.wav").play()
				bad_block.move()
				prize.move() # TROLL
				player.health -= 1

		# check if player collides with the prize
		if player.check_collision(player, prize):
			print("player hit the prize!")
			mixer.Sound("1up.wav").play()
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

			# easy mode:
			if easy_mode_flag:
				if pygame.time.get_ticks() < 10000:
					time_check += 4000
				elif pygame.time.get_ticks() < 30000:
					time_check += 2000
				elif pygame.time.get_ticks() < 60000:
					time_check += 1000
				elif pygame.time.get_ticks() < 90000:
					time_check += 600
				else:
					time_check += 400
			# hard mode
			else:
				if pygame.time.get_ticks() < 10000:
					time_check += 1000
				elif pygame.time.get_ticks() < 20000:
					time_check += 600
				elif pygame.time.get_ticks() < 40000:
					time_check += 400
				elif pygame.time.get_ticks() < 60000:
					time_check += 200
				else:
					time_check += 100



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

		# give health back to players as they collect more points
		if player.points == 5:
			if update_life_1:
				player.health += 1
				update_life_1 = False
		elif player.points == 10:
			if update_life_2:
				player.health += 2
				update_life_2 = False
		elif player.points == 15:
			if update_life_3:
				player.health += 3
				update_life_3 = False
		elif player.points == 20:
			if update_life_4:
				player.health += 5
				update_life_4 = False
		elif player.points == 25:
			if update_life_5:
				player.health += 10
				update_life_5 = False

		# run game over stuff
		if player.health <= 0:
			time_survived = pygame.time.get_ticks() / 1000
			end_points = player.points
			gameExit = True

		# show number of seconds elapsed, number of health, and number of points
		if player.health > 0:
			time_text = f.render("Time Elapsed: " + str(pygame.time.get_ticks() / 1000), False, black)
			gameDisplay.blit(time_text, (120, 0))
			health_text = f.render("Current Health: " + str(player.health), False, black)
			gameDisplay.blit(health_text, (350, 0))
			points_text = f.render("Points: " + str(player.points), False, black)
			gameDisplay.blit(points_text, (550, 0))

		enemies.update()
		enemies.draw(gameDisplay)
		pygame.draw.rect(gameDisplay, blue, player.rect)
		pygame.draw.rect(gameDisplay, forest_green, prize.rect)

		# color of bad_blocks gets more and more red as time goes on
		# and then things start getting crazy
		if pygame.time.get_ticks() < 15000:
			for bad_block in bad_block_list:
				pygame.draw.rect(gameDisplay, violet, bad_block.rect)
		elif pygame.time.get_ticks() < 30000:
			for bad_block in bad_block_list:
				pygame.draw.rect(gameDisplay, medium_violet, bad_block.rect)
		elif pygame.time.get_ticks() < 45000:
			for bad_block in bad_block_list:
				pygame.draw.rect(gameDisplay, violet_red, bad_block.rect)
		elif pygame.time.get_ticks() < 60000:
			for bad_block in bad_block_list:
				pygame.draw.rect(gameDisplay, red, bad_block.rect)
		else:
			late_game_color_blocks_switch = True
		# things start to get crazy
		# flashing lights mode haha

		if late_game_color_blocks_switch and flashing_mode_flag:
			if pygame.time.get_ticks() < 90000:
				if pygame.time.get_ticks() % 10 == 0:
					for bad_block in bad_block_list:
						pygame.draw.rect(gameDisplay, saddle_brown, bad_block.rect)
				else:
					for bad_block in bad_block_list:
						pygame.draw.rect(gameDisplay, black, bad_block.rect)
			else:
				if pygame.time.get_ticks() % 8 == 0:
					for bad_block in bad_block_list:
						pygame.draw.rect(gameDisplay, black, bad_block.rect)
				else:
					for bad_block in bad_block_list:
						pygame.draw.rect(gameDisplay, yellow_green, bad_block.rect)
		if late_game_color_blocks_switch and not flashing_mode_flag and pygame.time.get_ticks() > 60000:
			for bad_block in bad_block_list:
				pygame.draw.rect(gameDisplay, black, bad_block.rect)


		pygame.display.update()
		clock.tick(30)


	print("game over!!!")
	print(player.points)

	if credits_timer:
		myfont = pygame.font.SysFont("monospace", 50)
		credits = myfont.render("GAME OVER!", 1, black)
		gameDisplay.blit(credits, (300, 300))
		time_survived = myfont.render("Time Survived: " + str(time_survived), 1, black)
		gameDisplay.blit(time_survived, (250, 330))
		end_points = myfont.render("Total Points: " + str(end_points), 1, black)
		gameDisplay.blit(end_points, (280, 360))
		pygame.display.update()
		clock.tick(30)
		credits_timer -= 1
	else:
		pygame.quit()
		quit() #exits python





if __name__ == '__main__':
	main()



	

