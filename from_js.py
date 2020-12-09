from tkinter import *

screen = {
	"width": 10,
	"height": 10,
	"tile": 50
}

player = {
	"x": 0,
	"y": 0,
	"width": int(screen["tile"]/2),
	"height": int(screen["tile"]*4/5),
	"dx": 0,
	"dy": 0,
	"ddy": 0.3,
	"onGround": False,
	"max_dx": 4,
	"max_dy": -8
}

tiles = [
	"white",
	"brown",
	"black",
	"",
	"",
	"",
	"",
	"",
	"",
	"red"
]

game_map = [
	[0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0],
	[0,0,1,1,0,0,0,0,0,0],
	[0,0,0,0,0,0,0,0,0,0],
	[0,0,0,0,1,1,9,0,0,0],
	[0,0,0,0,0,0,0,0,2,0],
	[0,0,0,0,0,0,0,1,1,1],
	[1,1,1,1,1,1,1,1,1,1]
]

def draw_player():
	global player

	game_field.create_rectangle(
		player["x"],
		player["y"],
		player["x"] + player["width"],
		player["y"] + player["height"],
		fill="red",
		width=0
	)

def draw_map():
	global game_map, player

	for y in range(len(game_map)):
		for x in range(len(game_map[y])):
			if game_map[y][x] == 9:
				player["x"] = x*screen["tile"]
				player["y"] = y*screen["tile"]
				game_map[y][x] = 0
				continue

			game_field.create_rectangle(
				x*screen["tile"],
				y*screen["tile"],
				x*screen["tile"] + screen["tile"],
				y*screen["tile"] + screen["tile"],
				fill=tiles[game_map[y][x]],
				width=0
			)

def check_obj_collision(_dir, Debug=False):
	global player
	# x1,y1 ----- *
	#   |         |
	#   |         |
	#   |         |
	#   * ----- x2,y2
	x1 = int(player["x"] / screen["tile"])
	y1 = int(player["y"] / screen["tile"])
	x2 = int((player["x"] + player["width"]) / screen["tile"])
	y2 = int((player["y"] + player["height"]) / screen["tile"])

	zeros = 0
	counter = 0

	for y in range(y1, y2+1):
		for x in range(x1, x2+1):
			if game_map[y][x] == 1:
				if player["dx"] > 0 and _dir == 0: 
					player["x"] = x*screen["tile"] - player["width"] - 1
				if player["dx"] < 0 and _dir == 0:
					player["x"] = x*screen["tile"] + screen["tile"] + 1
				if player["dy"] > 0 and _dir == 1:
					player["y"] = y*screen["tile"] - player["height"] - 1
					player["dy"] = 0
					player["onGround"] = True
				if player["dy"] < 0 and _dir == 1:
					player["dy"] = 0
					player["y"] = y*screen["tile"] + screen["tile"] + 1

			counter += 1
			if y+1 < len(game_map[y]):
				if game_map[y+1][x] == 0 and player["onGround"]:
					zeros += 1

			if Debug:
				game_field.create_rectangle(
					x*screen["tile"],
					y*screen["tile"],
					x*screen["tile"] + screen["tile"],
					y*screen["tile"] + screen["tile"],
					width=1
				)
	if zeros == counter:
		player["onGround"] = False

def check_map_border_collisions():
	global player

	if player["x"]+player["dx"] < 0:
		player["x"] = 0

	if player["x"]+player["width"]+player["dx"] > screen["width"]*screen["tile"]:
		player["x"] = screen["width"]*screen["tile"] - player["width"] - 1

def move(ev):
	global player
	key_code = ev.keycode

	# left
	if key_code in [38, 113]:
		player["dx"] = -player["max_dx"]
	# right
	if key_code in [40, 114]:
		player["dx"] = player["max_dx"]
	# jump
	if key_code in [65] and player["onGround"]:
		player["dy"] = player["max_dy"]
		player["onGround"] = False

def stop(ev):
	global player
	key_code = ev.keycode

	if key_code in [38, 113, 40, 114]:
		player["dx"] = 0

def update():
	game_field.delete("all")
	draw_map()

	if player["onGround"]:
		player["dy"] = 0
	else:
		player["dy"] += player["ddy"]

	player["x"] += player["dx"]
	check_map_border_collisions()
	check_obj_collision(0, True)

	player["y"] += player["dy"]
	check_obj_collision(1, True)
	
	draw_player()

	root.after(10, update)

root = Tk()
game_field = Canvas(
	root,
	width=screen["width"]*screen["tile"],
	height=screen["height"]*screen["tile"],
	bg="white"
)
game_field.pack()

root.bind("<KeyPress>", move)
root.bind("<KeyRelease>", stop)

update()
root.mainloop()