#!/usr/bin/env python3

import json, sys

from model.room import Room
from model.hallway import Hallway
from model.level_generator import LevelGenerator
from model.level import Level
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
				row += str(room_json['layout'][row_ind][col_ind])
			board.append(row)

		# Generate a room from the layout and the given origin
		new_room = Room(room_json['origin'][0], room_json['origin'][1], board)
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
		new_hall = Hallway((hall_json['from'][0], hall_json['from'][1]), 
			(hall_json['to'][0], hall_json['to'][1]), hall_json['waypoints'])
		hallways.append(new_hall)

	return hallways

def build_level(level_json):
	rooms = build_rooms(level_json['rooms'])
	hallways = build_hallways(level_json['hallways'])
	lev_gen = LevelGenerator(rooms, hallways)
	lev = Level(lev_gen)

	# Adds keys and level exits to the level
	for snarl_object in level_json['objects']:
		if snarl_object['type'] == 'key':
			lev.add_key(snarl_object['position'][0], snarl_object['position'][1])
		elif snarl_object['type'] == 'exit':
			lev.add_exit(snarl_object['position'][0], snarl_object['position'][1])

	return lev


if __name__ == "__main__":
	user_input = sys.stdin.read()
	user_input_json = json.loads(user_input)

	state_data = user_input_json[0]
	name_to_move = user_input_json[1]
	point_to_move = user_input_json[2]

	# Build rooms, hallways, and generate level
	lev = build_level(state_data['level'])
	if not state_data["exit-locked"]:
		lev.unlock_exit()

	manager = GameManager([lev])

	for actor in state_data['players'] + state_data['adversaries']:
		if actor['type'] == 'player':
			manager.add_player(actor['name'], actor['position'][0], actor['position'][1])
		elif actor['type'] in ('zombie', 'ghost'):
			manager.add_adversary(actor['name'], actor['type'], actor['position'][0], actor['position'][1])

	print(manager.player_move(name_to_move, point_to_move))











