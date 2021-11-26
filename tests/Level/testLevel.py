import json, sys

from model.room import Room
from model.hallway import Hallway
from model.level_generator import LevelGenerator
from model.level import Level
from model.position import Position2D
from game_manager import GameManager
from view.level_view import View

def build_rooms(room_jsons):
	"""
	Builds a list of Snarl rooms from a list of room JSONs

	Parameters
	----------
	room_jsons : List[Dict]
		List of JSON representation of rooms
	"""
	rooms = []

	for room_json in room_jsons:
		board = []
		tile_map = {0: 'X', 1: 'O', 2: '|'}
		# Convert the layout to a mapped list of strings
		for row_ind in range(len(room_json['layout'])):
			row = ""
			for col_ind in range(len(room_json['layout'][row_ind])):
				row += tile_map[room_json['layout'][row_ind][col_ind]]
			board.append(row)

		# Generate a room from the layout and the given origin
		new_room = Room(room_json['origin'][1], room_json['origin'][0], board)
		rooms.append(new_room)

	return rooms


def build_hallways(hallways_json):
	"""
	Builds a list of Snarl hallways from a list of hallway JSONs

	Parameters
	----------
	hallways_json : List[Dict]
		List of JSON representation of hallways
	"""
	hallways = []

	for hall_json in hallways_json:
		new_waypoints = [(pt[1], pt[0]) for pt in hall_json['waypoints']]
		new_hall = Hallway((hall_json['from'][1], hall_json['from'][0]), 
			(hall_json['to'][1], hall_json['to'][0]), new_waypoints)
		hallways.append(new_hall)

	return hallways

def determine_object(lev, x, y):
	"""
	Determine whether the given point is a key or exit in the given level

	Parameters
	----------
	lev : Level
		Level that tile is in
	x : int
		x coodinate of the tile
	y : int
		y coordinate of the tile

	Returns
	-------
	str
		key, exit, or none
	"""
	if lev.tile_has_key(origin_point[1], origin_point[0]):
		object_type = "key"
	elif lev.tile_is_exit(origin_point[1], origin_point[0]):
		object_type = "exit"
	else:
		object_type = None

	return object_type

def determine_type(lev, x, y):
	"""
	Determine whether the given point is in a room hallway or void

	Parameters
	----------
	lev : Level
		Level that tile is in
	x : int
		x coodinate of the tile
	y : int
		y coordinate of the tile

	Returns
	-------
	str
		room, hallway, or void
	"""
	if lev.tile_in_room(origin_point[1], origin_point[0]) is not None:
		tile_type = "room"
	elif lev.tile_in_hallway(origin_point[1], origin_point[0]) is not None:
		tile_type = "hallway"
	else:
		tile_type = "void"

	return tile_type

def determine_traversable(lev, tile_type, x, y):
	"""
	Retrieve the traversable rooms or if hallway, rooms the hallway connects

	Parameters
	----------
	lev : Level
		Level that tile is in
	tile_type : str
		Whether the tile is a room, hallway, or none
	x : int
		x coodinate of the tile
	y : int
		y coordinate of the tile

	Returns
	-------
	str
		room, hallway, or void
	"""
	if tile_type == "room":
		reachable_rooms = lev.get_reachable_rooms(origin_point[1], origin_point[0])
	elif tile_type == "hallway":
		hallway = lev.tile_in_hallway(origin_point[1], origin_point[0])
		reachable_rooms = []
		for pos in (hallway.get_start_pos(), hallway.get_end_pos()):
			reachable_rooms.append(lev.tile_in_room(pos.get_x(), pos.get_y()))
	else:
		reachable_rooms = []

	reachable_rooms = [room.get_position() for room in reachable_rooms]
	reachable_rooms = [[pos.get_y(), pos.get_x()] for pos in reachable_rooms]

	return reachable_rooms

if __name__ == "__main__":
	user_input = sys.stdin.read()
	user_input_json = json.loads(user_input)

	level_data = user_input_json[0]
	origin_point = user_input_json[1]

	# Build rooms, hallways, and generate level
	rooms = build_rooms(level_data['rooms'])
	hallways = build_hallways(level_data['hallways'])
	lev_gen = LevelGenerator(rooms, hallways)
	lev = Level(lev_gen)

	# Adds keys and level exits to the level
	for snarl_object in level_data['objects']:
		if snarl_object['type'] == 'key':
			lev.add_key(snarl_object['position'][1], snarl_object['position'][0])
		elif snarl_object['type'] == 'exit':
			lev.add_exit(snarl_object['position'][1], snarl_object['position'][0])

	traversable = lev.tile_is_traversable(origin_point[1], origin_point[0])

	object_type = determine_object(lev, origin_point[1], origin_point[0])

	tile_type = determine_type(lev, origin_point[1], origin_point[0])

	reachable = determine_traversable(lev, tile_type, origin_point[1], origin_point[0])

	print(json.dumps({"traversable": traversable, "object": object_type, "type": tile_type, 
		"reachable": reachable}))


	manager = GameManager([lev])
	manager.add_player(1)
	state = manager.build_state(1)
	view_json = json.dumps(state)
	view = View(view_json)












