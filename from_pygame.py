import pygame
from pygame import *

from Camera import *

screen_stat = {
	"width": 10,
	"height": 10
}
tile = {
	"size": 48,
	"color": "#9A6C1A"
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
	"width":  int(tile["size"]/2),
	"height": int(tile["size"]*4/5),
	"color": "#00FF19"
}

player = sprite.Sprite()
player.image = Surface((player_stat["width"], player_stat["height"]))
player.image.fill(Color(player_stat["color"]))
# player.image = image.load("pygame_files/") # 24, 38
# player_stand.png
player.image = image.load("pygame_files/player/PNG/Player/Poses/player_stand_scaled.png")

player.rect = Rect(player_stat["x"], player_stat["y"], player_stat["width"], player_stat["height"])

timer = pygame.time.Clock()

def collisions_obstacles(_dx, _dy, _obstacles):
	global player_stat, player

	for p in _obstacles:
		if sprite.collide_rect(player, p):
			if _dx > 0:
				player.rect.right = p.rect.left
			if _dx < 0:
				player.rect.left = p.rect.right
			if _dy > 0:
				player.rect.bottom = p.rect.top
				player_stat["onGround"] = True
				player_stat["dy"] = 0
			if _dy < 0:
				player.rect.top = p.rect.bottom
				player_stat["dy"] = 0

def collisions_interact(_interact):
	global level

	for i in _interact:
		if sprite.collide_rect(player, i["sprite"]):
			m = i["x"]
			n = i["y"]
			key = level[n][m]

			if key == "k":
				level[n] = level[n][:m] + " " + level[n][m+1:]
				for l in range(len(level)):
					if level[l].find("d") > -1:
						z = level[l].index("d")
						level[l] = level[l][:z] + "D" + level[l][z+1:]

			if key == "D":
				print("Next level!")


def player_move(left, right, jump, _obstacles, _interact):
	global player_stat, player

	if left:
		player_stat["dx"] = -player_stat["speed"]
	if right:
		player_stat["dx"] = player_stat["speed"]
	if not(left or right):
		player_stat["dx"] = 0

	if player_stat["onGround"] and jump:
		player_stat["dy"] = -player_stat["jump_power"]
	if not player_stat["onGround"]:
		player_stat["dy"] += player_stat["ddy"]

	player_stat["onGround"] = False

	player.rect.x += player_stat["dx"]
	collisions_obstacles(player_stat["dx"], 0, _obstacles)

	player.rect.y += player_stat["dy"]
	collisions_obstacles(0, player_stat["dy"], _obstacles)

	collisions_interact(_interact)

DISPLAY = (screen_stat["width"]*tile["size"], screen_stat["height"]*tile["size"])

pygame.init()

screen = pygame.display.set_mode(DISPLAY)
pygame.display.set_caption("Test game")

background = Surface(DISPLAY)
background.fill(Color("#ffffff"))

level = [
	"3___________2",
	"7           |",
	"7           |",
	"7      k    |",
	"7      TT   |",
	"7           |",
	"7    TT     |",
	"7           |",
	"7  TT       |",
	"7      TT   |",
	"7    TT     |",
	"7  TT       |",
	"7         d |",
	"1TTTTTTTTTTT0"
]

obstacles_sprites = {
	"0": "pygame_files/surface/PNG/Tiles/tile25.png",
	"1": "pygame_files/surface/PNG/Tiles/tile26.png",
	"2": "pygame_files/surface/PNG/Tiles/tile26_rev.png",
	"3": "pygame_files/surface/PNG/Tiles/tile25_rev.png",
	"7": "pygame_files/surface/PNG/Tiles/tile88.png",
	"_": "pygame_files/surface/PNG/Tiles/tile32_rev.png",
	"|": "pygame_files/surface/PNG/Tiles/tile90.png",
	"T": "pygame_files/surface/PNG/Tiles/tile32.png"
}
interact_sprites = {
	"d": {
		"w": 48,
		"h": 48,
		"sprite": "pygame_files/door_lock.png"
	},
	"D": {
		"w": 48,
		"h": 48,
		"sprite": "pygame_files/door_open.png"
	},
	"k": {
		"w": 26,
		"h": 26,
		"sprite": "pygame_files/key.png"
	}
}

camera = Camera(camera_configure, len(level[0])*tile["size"], len(level)*tile["size"])

left = right = jump = False

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

	objects = pygame.sprite.Group()
	obstacles = []
	interact = []
	
	for y in range(len(level)):
		for x in range(len(level[y])):
			if level[y][x] in obstacles_sprites or level[y][x] in interact_sprites:
				tile_sprite = sprite.Sprite()
				if level[y][x] in obstacles_sprites:
					tile_sprite.image = image.load(obstacles_sprites[level[y][x]])
					tile_sprite.rect = Rect(
						x*tile["size"],
						y*tile["size"],
						tile["size"],
						tile["size"]
					)

					obstacles.append(tile_sprite)

				if level[y][x] in interact_sprites:
					io = interact_sprites[level[y][x]]
					tile_sprite.image = image.load(io["sprite"])
					tile_sprite.rect = Rect(
						x*tile["size"] + int((tile["size"]-io["w"])/2),
						y*tile["size"] + int((tile["size"]-io["h"])/2),
						io["w"],
						io["h"]
					)

					interact.append({
						"sprite": tile_sprite,
						"x": x,
						"y": y
					})

				objects.add(tile_sprite)			

	objects.add(player)
	player_move(left, right, jump, obstacles, interact)

	camera.update(player, screen_stat["width"]*tile["size"], screen_stat["height"]*tile["size"])
	for obj in objects:
		screen.blit(obj.image, camera.apply(obj))

	pygame.display.update()