from .level_generator import LevelGenerator

class Level:
	"""
	Data representation of a Snarl Level.

	Parameters
	----------
	level_generator : LevelGenerator
		Valid level generation
	"""
	def __init__(self, level_json):
		self._level_generator = LevelGenerator(level_json)
		self._tiles = self._level_generator.get_whole_level()
		self._rooms = sorted(self._level_generator.get_rooms())
		self._hallways = self._level_generator.get_hallways()
		self._is_locked = True
		self._initialize_objects(level_json['objects'])
		self._found_key = None
	
	def _initialize_objects(self, objects_array):
		for obj in objects_array:
			if obj['type'] == 'key':
				self.add_key(obj['position'][0], obj['position'][1])
			elif obj['type'] == 'exit':
				self.add_exit(obj['position'][0], obj['position'][1])

	def get_all_tiles(self):
		return self._tiles

	def get_tile(self, row, col):
		"""
		Retrieve the tile from the given row, col index

		Parameters
		----------
		row : int
			row index of the tile
		col : int
			col index of the tile

		Returns
		-------
		Tile
			tile at the given position
		"""
		try:
			return self._tiles[row][col]
		except:
			return None

	def add_key(self, row, col):
		"""
		Adds a key to the tile at the given x, y coordinate

		Parameters
		----------
		row : int
			row index of the tile
		col : int
			col index of the tile
		"""
		self.get_tile(row, col).add_key()

	def remove_key(self, player_name):
		"""
		Removes the key from the level, someone picked it up
		"""
		for row in self._tiles:
			for tile in row:
				if tile.has_key():
					tile.remove_key()
					self._found_key = player_name

	def add_exit(self, row, col):
		"""
		Adds an exit to the tile at the given row, col index

		Parameters
		----------
		row : int
			row index of the tile
		col : int
			col index of the tile
		"""
		self.get_tile(row, col).add_level_exit()

	def unlock_exit(self):
		"""
		Sets the unlock status of the level to True
		"""
		for row in self._tiles:
			for tile in row:
				if tile.is_exit():
					tile.unlock()
					self._is_locked = False
	
	def who_unlocked(self):
		return self._found_key
	
	def is_locked(self):
		"""
		Retrieve whether the level is unlocked

		Returns
		-------
		bool
			Whether the level is unlocked
		"""
		return self._is_locked

	def get_exit_position(self):
		"""
		Retrieves the exit position

		Returns
		-------
		(int, int)
			Row and column index of the exit position
		"""
		for row in self._tiles:
			for tile in row:
				if tile.is_exit():
					return (tile.get_row(), tile.get_col())

	def get_tiles(self):
		"""
		Retrieves all the tiles in the level as a flat list

		Returns
		-------
		List[Tile]
			All of the tiles in the level
		"""
		all_tiles = []
		for row in self._tiles:
			all_tiles += row
		return all_tiles

	def get_JSON(self):
		"""
		Retrieves JSON representation of a level

		Returns
		-------
		dict
			JSON representation of a level
		"""
		as_json = {
			"type": "level", 
			"rooms": [room.get_JSON() for room in self._rooms], 
			"hallways": [hallway.get_JSON() for hallway in self._hallways],
			"objects": self.get_objects_json(self._tiles)
		}

		return as_json
	
	def get_objects_json(self, tiles):
		all_objects = []

		for row in tiles:
			for tile in row:
				if tile is None:
					continue

				tile_pos = (tile.get_row(), tile.get_col())
				if tile.has_key():
					all_objects.append({"type": "key", "position": tile_pos})
				elif tile.is_exit():
					all_objects.append({"type": "exit", "position": tile_pos})

		return all_objects

	def get_level_layout(self, tiles):
		"""
		Retrieves the level representation as a list of strings. Each string corresponds to
		a row, and each character corresponds to the string representation of that level.

		Returns
		-------
		List[str]
			List of string representations of tiles
		"""
		rows = []
		for row in tiles:
			parsed_row = []
			for tile in row:
				if tile is None:
					parsed_row.append(0)
				else:
					parsed_row.append(int(tile.__str__()))
			rows.append(parsed_row)
		return rows
	
	def get_partial_level_layout(self, origin_pos, radius=2):
		"""
		Retrieves a grid of tiles centered around the origin position with a vertical
		and horizontal radius of the given value

		Parameters:
		-----------
		origin_pos : (int, int)
			Row and column index of the center of the layout
		radius : int
			Horizontal and vertical radius of the grid
		
		Returns:
		--------
		List[List[int]]
			Nested list of integer representation of the tiles
		"""
		rows = []
		origin_row = origin_pos[0]
		origin_col = origin_pos[1]

		for row_ind in range(origin_row - radius, origin_row + radius + 1):
			row = []
			for col_ind in range(origin_col - radius, origin_col + radius + 1):
				tile_to_add = self.get_tile(row_ind, col_ind)

				if tile_to_add is None:
					row.append(None)
				else:
					row.append(tile_to_add)
			rows.append(row)
		
		return rows

	def tile_in_room(self, row , col):
		"""
		Retrieves the Room the tile is in, or None if it is not in a Room

		Parameters
		----------
		row : int
			row index of the tile
		col : int
			col index of the tile

		Returns
		-------
		Room
			The room the tile is in or None
		"""
		tile_in_question = self.get_tile(row, col)
		for room in self._rooms:
			if tile_in_question in room.get_tiles():
				return room
		return None

	def tile_in_hallway(self, row , col):
		"""
		Retrieves the Hallway the tile is in, or None if it is not in a Hallway

		Parameters
		----------
		row : int
			row index of the tile
		col : int
			col index of the tile

		Returns
		-------
		Hallway
			The Hallway the tile is in or None
		"""
		tile_in_question = self.get_tile(row, col)
		for hallway in self._hallways:
			if tile_in_question in hallway.get_tiles():
				return hallway
		return None

	def get_reachable_rooms(self, row, col):
		"""
		Retrieves the rooms that are immediately reachable from the room that the given tile location is in.
		A Room is reachable if they can be reached by exactly one hallway

		Parameters
		----------
		row : int
			row index of the tile
		col : int
			col index of the tile

		Returns
		-------
		List[Room]
			All reachable rooms from room given tile is in
		"""
		tile_room = self.tile_in_room(row, col)
		reachable_rooms = []

		for hallway in self._hallways:
			start_pos = hallway.get_start_pos()
			end_pos = hallway.get_end_pos()
			start_tile = self.get_tile(start_pos[0], start_pos[1])
			end_tile = self.get_tile(end_pos[0], end_pos[1])
			
			if start_tile in tile_room.get_tiles():
				reachable_rooms.append(self.tile_in_room(end_pos[0], end_pos[1]))
			elif end_tile in tile_room.get_tiles():
				reachable_rooms.append(self.tile_in_room(start_pos[0], start_pos[1]))

		return reachable_rooms
	
	def build_state(self):
		"""
		Builds a dictionary of the current game state including the layout of current level, 
		and positions of the player, their teammates, and their zombies
		"""
		game_state = {
		"type": "state",
		"level": self.get_JSON(),
		"players": [],
		"adversaries": [],
		"exit-locked": self.is_locked(),
		}
		for row in self._tiles:
			for tile in row:
				actor = tile.get_person()
				if actor is None:
					continue
				elif actor.get_type() == 'player' and (actor.is_ejected() or actor.is_exited()):
					continue
				elif actor.get_type() == 'player':
					game_state['players'].append(actor.get_position_JSON())
				else:
					game_state['adversaries'].append(actor.get_position_JSON())

		return game_state
	
	def player_in_room(self, row, col):
		room = self.tile_in_room(row, col)
		if room is None:
			return None
		player_pos = []
		for r in self._rooms:
			if (room.get_row(), room.get_col()) == (r.get_row(), r.get_col()):
				for tile in room.get_tiles():
					if tile.get_person() is not None and tile.get_person().get_type() == 'player':
						player_pos.append(tile.get_position())
		return player_pos



		







