# player_move
# screen.blit(player.image, (player.rect.x, player.rect.y))
# timer
# player["onGround"]

import pygame
from pygame import *

pygame.init()

screen_stat = {
	"width": 10,
	"height": 10,
	"tile": 48
}

player_stat = {
	"x": 100,
	"y": 100,
	"speed": 5,
	"jump_power": 10,
	"onGround": False,
	"dx": 0,
	"dy": 0,
	"ddy": 0.35,
	"width":  int(screen_stat["tile"]/2),
	"height": int(screen_stat["tile"]*4/5)
}

def player_move(left, right, jump):
	print(left, right, jump)
	global player_stat, player

	if left:
		player_stat["dx"] = -player_stat["speed"]
	if right:
		player_stat["dx"] = player_stat["speed"]
	if not(left or right):
		player_stat["dx"] = 0

	if player_stat["onGround"] and jump:
		player_stat["dy"] = -player_stat["jump_power"]
	# if not player_stat["onGround"]:
	# 	player_stat["dy"] += player_stat["ddy"]

	player.rect.x += player_stat["dx"]
	player.rect.y += player_stat["dy"]

player = sprite.Sprite()
player.image = Surface((player_stat["width"], player_stat["height"]))
player.image.fill(Color("#00FF19"))
player.rect = Rect(player_stat["x"], player_stat["y"], player_stat["width"], player_stat["height"])

level = [
	"##########",
	"#        #",
	"#        #",
	"#        #",
	"#        #",
	"#        #",
	"#        #",
	"#        #",
	"#        #",
	"##########"
]

DISPLAY = (screen_stat["width"]*screen_stat["tile"], screen_stat["height"]*screen_stat["tile"])
screen = pygame.display.set_mode(DISPLAY)
pygame.display.set_caption("Test game")

background = Surface(DISPLAY)
background.fill(Color("#ffffff"))

left = right = jump = False
timer = pygame.time.Clock()

while 1:
	timer.tick(60)
	for e in pygame.event.get():
		if e.type == QUIT:
			exit()
		if e.type == KEYDOWN and e.key in [K_LEFT, K_a]:
			left = True
		if e.type == KEYDOWN and e.key in [K_RIGHT, K_d]:
			right = True
		if e.type == KEYDOWN and e.key in [K_UP, K_SPACE, K_w]:
			jump = True

		if e.type == KEYUP and e.key in [K_LEFT, K_a]:
			left = False
		if e.type == KEYUP and e.key in [K_RIGHT, K_d]:
			right = False
		if e.type == KEYUP and e.key in [K_UP, K_SPACE, K_w]:
			jump = False

	screen.blit(background, (0,0))

	for y in range(len(level)):
		for x in range(len(level[y])):
			coordX = x*screen_stat["tile"]
			coordY = y*screen_stat["tile"]

			if level[y][x] == "#":
				tile = Surface((screen_stat["tile"], screen_stat["tile"]))
				tile.fill(Color("#FF6262"))

				screen.blit(tile, (coordX, coordY))

	player_move(left, right, jump)
	screen.blit(player.image, (player.rect.x, player.rect.y))

	pygame.display.update()