import pygame, sys
import random

# General setup
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
clock = pygame.time.Clock()

# Setting up the main window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
icon = pygame.image.load("ping-pong.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Pong")

# Defining Game objects
ball = pygame.Rect(int(screen_width/2) - 10, int(screen_height/2) - 10, 20, 20)
player = pygame.Rect(int(screen_width - 20), int(screen_height/2) - 50, 10, 100)
opponent = pygame.Rect(10, int(screen_height/2) - 50, 10, 100)

# Game variables
bg_color = (18, 18, 18)
teal = (3, 218, 196)

ball_speed_factor = 5
ball_speed_x = ball_speed_factor * random.choice((1, -1))
ball_speed_y = ball_speed_factor * random.choice((1, -1))
player_speed = 0
opponent_speed = 5
speed_target = 10
bounce = 0

# Text Variables
player_score = 0
opponent_score = 0
game_font = pygame.font.Font("freesansbold.ttf", 28)
winner_font = pygame.font.Font("freesansbold.ttf", 36)

# Score Timer
score_time = True

# Sounds
pong_sound = pygame.mixer.Sound("pong.ogg")
score_sound = pygame.mixer.Sound("score.ogg")

def ball_restart():
	global ball_speed_x, ball_speed_y, start, score_time, opponent_speed, ball_speed_factor, bounce

	ball_speed_factor = 5

	current_time = pygame.time.get_ticks()
	ball.center = (int(screen_width/2), int(screen_height/2))

	if current_time - score_time < 700:
		number_three = game_font.render("3", True, teal)
		screen.blit(number_three, (int(screen_width/2) - 8, int(screen_height/2) + 20))
	elif current_time - score_time < 1400:
		number_two = game_font.render("2", True, teal)
		screen.blit(number_two, (int(screen_width/2) - 8, int(screen_height/2) + 20))
	elif current_time - score_time < 2100:
		number_one = game_font.render("1", True, teal)
		screen.blit(number_one, (int(screen_width/2) - 8, int(screen_height/2) + 20))

	if current_time - score_time < 2100:
		ball_speed_x, ball_speed_y = 0, 0
		opponent_speed = 0
	else:
		ball_speed_x = ball_speed_factor * random.choice((1, -1))
		ball_speed_y = ball_speed_factor * random.choice((1, -1))
		score_time = None
		opponent_speed = 5

def ball_animation():
	global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time, bounce
	# Movement animation
	ball.x += ball_speed_x
	ball.y += ball_speed_y

	# Bouncing off the screen boundary
	if ball.top <= 0 or ball.bottom >= screen_height:
		pygame.mixer.Sound.play(pong_sound)
		ball_speed_y *= -1

	# Score Update
	if ball.left <= 0:
		pygame.mixer.Sound.play(score_sound)
		player_score += 1
		score_time = pygame.time.get_ticks()
	if ball.right >= screen_width:
		pygame.mixer.Sound.play(pong_sound)
		opponent_score += 1
		score_time = pygame.time.get_ticks()

	# Bouncing off the paddles
	# Player paddle
	if ball.colliderect(player) and ball_speed_x > 0:
		pygame.mixer.Sound.play(pong_sound)
		bounce += 1
		if abs(ball.right - player.left) < 10:
			ball_speed_x *= -1
		elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
			ball_speed_y *= -1
		elif abs(ball.bottom - player.top) < 10 and ball_speed_y < 0:
			ball_speed_y *= -1
	# Opponent Paddle
	if ball.colliderect(opponent) and ball_speed_x < 0:
		pygame.mixer.Sound.play(pong_sound)
		bounce += 1
		if abs(ball.left - opponent.right) < 10:
			ball_speed_x *= -1
		elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
			ball_speed_y *= -1
		elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y < 0:
			ball_speed_y *= -1


def player_animation():
	player.y += player_speed	
	if player.top <= 0:
		player.top = 0
	elif player.bottom >= screen_height:
		player.bottom = screen_height


def opponent_animation():
	if opponent.top < ball.y:
		opponent.top += opponent_speed
	elif opponent.bottom > ball.y:
		opponent.bottom -= opponent_speed
	if opponent.top <= 0:
		opponent.top = 0
	elif opponent.bottom >= screen_height:
		opponent.bottom = screen_height

def speed_increase():
	global ball_speed_factor, speed_target, ball_speed_x, ball_speed_y
	ball_speed_factor += 1
	speed_target += 10
	if ball_speed_x > 0:
		ball_speed_x = ball_speed_factor * 1
	elif ball_speed_x < 0:
		ball_speed_x = ball_speed_factor * -1
	if ball_speed_y > 0:
		ball_speed_y = ball_speed_factor * 1
	elif ball_speed_y < 0:
		ball_speed_y = ball_speed_factor * -1

def game_over(winner):
	global player_speed, opponent_speed, ball_speed_x, ball_speed_y
	player_speed, opponent_speed, ball_speed_x, ball_speed_y = 0, 0, 0, 0
	screen.fill(bg_color)
	if winner == "Computer":
		winner_text = winner_font.render("{} won!".format(winner), True, teal)
		screen.blit(winner_text, (int(screen_width/2) - 140, int(screen_height/2) - 20))
	else:
		winner_text = winner_font.render("{} won!".format(winner), True, teal)
		screen.blit(winner_text, (int(screen_width/2) - 80, int(screen_height/2) - 20))


while True:
	# Handling input
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_DOWN:
				player_speed += 5
			elif event.key == pygame.K_UP:
				player_speed -= 5
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_DOWN:
				player_speed -= 5
			elif event.key == pygame.K_UP:
				player_speed += 5

	ball_animation()
	player_animation()
	opponent_animation()

	# Visuals
	screen.fill(bg_color)
	pygame.draw.rect(screen, teal, player)
	pygame.draw.rect(screen, teal, opponent)
	pygame.draw.ellipse(screen, teal, ball)
	pygame.draw.aaline(screen, teal, (int(screen_width / 2), 0), (int(screen_width / 2), screen_height))

	if score_time:
		ball_restart()

	if bounce == speed_target:
		speed_increase()

	if player_score == 5:
		game_over("You")
	elif opponent_score == 5:
		game_over("Computer")

	player_text = game_font.render("{}".format(player_score), True, teal)
	screen.blit(player_text, (int(screen_width/2) + 20, 10))
	opponent_text = game_font.render("{}".format(opponent_score), True, teal)
	screen.blit(opponent_text, (int(screen_width/2) - 40, 10))

	# Updating the window
	pygame.display.flip()
	clock.tick(60)