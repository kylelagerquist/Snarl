#!/usr/bin/env python3

import json, sys
from room import Room
from level_generator import LevelGenerator
from level import Level
from position import Position2D

def validate_input(input_string):
	"""
	Ensure the input test string is a valid JSON with the necessary valid arguments

	Parameters
	----------
	input_string : str
		Inputted user test string for traversable points
	"""
	# Ensure it is a valid JSON
	try:
		as_json = json.loads(input_string)
	except:
		raise ValueError("Invalid JSON input.")

	room_data = as_json[0]

	# Ensure all arguments are present
	for param in ('type', 'origin', 'bounds', 'layout'):
		if param not in room_data:
			raise ValueError(f'Invalid JSON, missing {param} parameter.')

	# Ensure the test type is valid
	if room_data['type'] not in ('room'):
		raise ValueError(f"Invalid JSON, {room_data['type']} is not a valid type.")

	# Ensure room boundaries match the layout boundaries
	if (room_data['bounds']["rows"] != len(room_data['layout']) or 
		room_data['bounds']["columns"] != len(room_data['layout'][0])):
		raise ValueError('Width and height of room do not match layout.')

	# Ensure layout is rectangular
	for row_ind in range(1, len(room_data['layout'])):
		if len(room_data['layout'][row_ind-1]) != len(room_data['layout'][row_ind]):
			raise ValueError("Invalid layout, not rectangular.")

	# Ensure all tiles are either a wall, space, or door
	for row in room_data['layout']:
		for tile_repr in row:
			if tile_repr not in (0, 1, 2):
				raise ValueError(f"{tile_repr} is an invalid tile representation.")

	return as_json

if __name__ == "__main__":
	user_input = sys.stdin.read()
	user_input = validate_input(user_input)

	room_data = user_input[0]
	origin_point = user_input[1]

	board = []
	tile_map = {0: 'X', 1: 'O', 2: '|'}
	# Convert the layout to a mapped list of strings
	for row_ind in range(len(room_data['layout'])):
		row = ""
		for col_ind in range(len(room_data['layout'][row_ind])):
			row += tile_map[room_data['layout'][row_ind][col_ind]]
		board.append(row)

	# Generate a room from the layout and the given origin
	new_room = Room(room_data['origin'][1], room_data['origin'][0], board)
	# Generate the level
	lev_generator = LevelGenerator([new_room], [])
	lev1 = Level(lev_generator)

	# Determine the traversable points, get their position, sort, 
	# and convert to (row, col) format
	traversable_points = lev1.get_traversable_points(origin_point[1], origin_point[0])
	traversable_points = [tile.get_position() for tile in traversable_points]
	traversable_points.sort()
	traversable_points = [(pos.get_y(), pos.get_x()) for pos in traversable_points]
	
	# Generate the output json
	if len(traversable_points) > 0:
		print(json.dumps(["Success: Traversable points from ", origin_point, 
			" in room at ", room_data['origin'] , " are ", traversable_points]))
	else:
		print(json.dumps(["Failure: Point ", origin_point, " is not in room at ", 
			room_data['origin']]))






