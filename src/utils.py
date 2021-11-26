import json
import os

def parse_levels(file_name):
	"""
	Parse all of the levels from the given file

	Parameters
	----------
	file_name : str
		Name of the file to parse
	
	Returns
	-------
	[JSON]
		First JSON should be an int, rest should be level instances
	"""
	jsons = []
	json_strs = []

	with open(os.path.join(os.getcwd(), file_name)) as f:
		for line in f:
			if line != '\n':
				json_strs.append(line.strip())
			else:
				as_json = json.loads(' '.join(json_strs))
				jsons.append(as_json)
				json_strs = []

	as_json = json.loads(' '.join(json_strs))
	jsons.append(as_json)

	if len(jsons) < 1:
		raise ValueError("Invalid levels file.")
	elif not isinstance(jsons[0], int):
		raise ValueError("First JSON must be int")
	return jsons[1:]

def build_player_update(player, level):
	"""
	Build a player update JSON for the designated player name

	Parameters:
	-----------
	player_name : str
		The player name to build the update for
	
	Returns:
	--------
	dict
		A formatted plauer update with their location, the tiles in their range,
		as well as players and objects in those tiles
	"""
	player_pos = player.get_position()
	visible_tiles = level.get_partial_level_layout(player_pos)
	
	actors = []
	# Retrieve the actors that are visible to the player
	for row in visible_tiles:
		for tile in row:
			if tile is None:
				continue
			elif tile.get_person() is None:
				continue
			elif tile.get_person().get_name() == player.get_name():
				continue
			else:
				actors.append(tile.get_person().get_position_JSON())
	
	player_state = {
		"type": "player-update",
		"layout": level.get_level_layout(visible_tiles),
		"position": player.get_position(),
		"objects": level.get_objects_json(visible_tiles),
		"actors": actors,
		"message": None,
		"health": player.get_health()
	}

	return player_state

def send_end_level(players, who_unlocked):
	"""
	Compile the end level JSON to be sent to all the players
	"""
	players_exited = []
	players_ejected = []

	for p in players:
		if p.is_exited():
			players_exited.append(p.get_name())
		elif p.is_ejected():
			players_ejected.append(p.get_name())
	
	end_level_json = {
		"type": "end-level",
		"key": who_unlocked,
		"exits": players_exited,
		"ejects": players_ejected
	}
	
	for p in players:
		p.send_message(json.dumps(end_level_json))

def send_level_start(players, level_num):
	"""
	Compile a level start json to be sent to all the players
	"""
	active_players = []
	for p in players:
		if not p.is_ejected() and not p.is_exited():
			active_players.append(p)
	
	start_level_json = {
		"type": "start-level",
		"level": level_num,
		"players": [p.get_name() for p in active_players]
	}
	
	for p in active_players:
		p.send_message(json.dumps(start_level_json))
