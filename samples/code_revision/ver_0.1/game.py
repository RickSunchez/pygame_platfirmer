import pygame
from pygame import *

pygame.init()

screen_stat = {
	"width": 10,
	"height": 10,
	"tile": 48
}

DISPLAY = (screen_stat["width"]*screen_stat["tile"], screen_stat["height"]*screen_stat["tile"])
screen = pygame.display.set_mode(DISPLAY)
pygame.display.set_caption("Test game")

background = Surface(DISPLAY)
background.fill(Color("#ffffff"))

while 1:
	for e in pygame.event.get():
		if e.type == QUIT:
			exit()

	screen.blit(background, (0,0))

	pygame.display.update()