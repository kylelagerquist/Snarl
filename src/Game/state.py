
class State:
	def __init__(self, state_json):
		self._state_json = state_json
		self._layout = self._build_layout()
	
	def get_tile(self, pos):
		"""
		Retrieve the tile at the given pos

		Parameters
		----------
		pos : (int, int)
			row, column index of tile to retrieve
		
		Returns
		-------
		int
			Int representation of tile
		"""
		try:
			return self._layout[pos[0]][pos[1]]
		except:
			return None
	
	def get_layout(self):
		return self._layout
	
	def get_json(self):
		return self._state_json
	
	def players_in_room(self, pos):
		player_pos = []
		if self.get_tile(pos) is None:
			return player_pos
		
		for room_json in self._state_json['level']['rooms']:
			if self._pos_in_room(pos, room_json):
				for player_json in self._state_json['players']:
					if self._pos_in_room(player_json['position'], room_json):
						player_pos.append(player_json['position'])
		
		return player_pos
	
	def tile_has_adversary(self, pos):
		"""
		Retrieve whether the tile contains an adversary

		Parameters
		----------
		pos : (int, int)
			Tile position to check
		
		Returns
		-------
		bool
			Whether the tile has an adversary on it
		"""
		if self.get_tile(pos) is None:
			return False
		
		for adversary in self._state_json['adversaries']:
			if tuple(adversary['position']) == tuple(pos):
				return True
		
		return False

	def _pos_in_room(self, pos, room_json):
		"""
		Determine whether the given pos is located in the room_json

		Parameters
		----------
		pos : (int, int)
			row, column index of tile
		room_json : dict
			json of room information
		
		Returns
		-------
		bool
			Whether the pos in the room
		"""
		top = room_json['origin'][0]
		bottom = top + room_json['bounds']['rows'] - 1
		left = room_json['origin'][1]
		right = left + room_json['bounds']['columns'] - 1
		
		return top <= pos[0] <= bottom and left <= pos[1] <= right
	
	def _build_layout(self):
		"""
		Turn the lists or rooms and hallways into a rectangular layout

		Returns
		-------
		List[List[int]]
			Int representations of tiles in level
		"""
		level = self._state_json['level']
		height, width = self._level_dimensions()
		layout = [[0 for col in range(width)] for row in range(height)]

		for room in level['rooms']:
			origin = room['origin']
			for row_ind in range(len(room['layout'])):
				for col_ind in range(len(room['layout'][row_ind])):
					row = origin[0] + row_ind
					col = origin[1] + col_ind
					layout[row][col] = room['layout'][row_ind][col_ind]
		
		for hall in level['hallways']:
			hall_tiles = self._get_hallway_tiles(hall)
			for pos in hall_tiles:
				layout[pos[0]][pos[1]] = 1
		
		return layout

	def _level_dimensions(self):
		"""
		Retrieve the dimensions of the level

		Returns
		-------
		(int, int)
			height, width of the level
		"""
		level = self._state_json['level']
		height = 0
		width = 0

		for room_json in level['rooms']:
			height = max(height, room_json["origin"][0] + room_json['bounds']['rows'])
			width = max(width, room_json["origin"][1] + room_json['bounds']['columns'])
		
		for hall_json in level['hallways']:
			points = [hall_json['from']] + hall_json['waypoints'] + [hall_json['to']]
			height = max(height, max([p[0] for p in points]) + 1)
			width = max(width, max([p[1] for p in points]) + 1)
		
		return (height, width)

	def _get_hallway_tiles(self, hall_json):
		"""
		Retrieves the points of all the tiles in the hallway, not including start and
		end points

		Returns
		-------
		List[(int, int)]
			List of tiles that make up the hallway
		"""
		polyline = [hall_json['from']] + hall_json['waypoints'] + [hall_json['to']]
		all_points = []

		for ind in range(1, len(polyline)):
			prev_point = polyline[ind - 1]
			point = polyline[ind]
			# Vertical line connecting points
			if prev_point[1] == point[1]:
				top = min(prev_point[0], point[0])
				bottom = max(prev_point[0], point[0])
				for y in range(top + 1, bottom):
					all_points.append((y, point[1]))
			# Horizontal line connecting points
			else:
				leftmost = min(prev_point[1], point[1])
				rightmost = max(prev_point[1], point[1])
				for x in range(leftmost + 1, rightmost):
					all_points.append((point[0], x))

		all_points += hall_json['waypoints']

		return all_points