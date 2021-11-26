from .tile import *

class Room:
	"""
	Data representation of an individual room for the game Snarl.

	Rooms are valid if they are rectangular.
	Currently, tiles inside of a room can be any combination of spaces and walls.

	Parameters
	----------
	origin_row : int
		row index of top row in room
	origin_col : int
		column index of left most column in room
	tiles : List[str]
		List of string representations of each row in the room. Each character represents a tile.
	"""
	def __init__(self, origin_row, origin_col, tiles):
		if origin_row < 0 or origin_col < 0:
			raise ValueError("Origin row and column must be positive.")
		self._origin_row = origin_row
		self._origin_col = origin_col
		self._tiles = self._build_room(tiles)

	def _build_room(self, str_rows):
		"""
		Generates all of the tiles for a room from a text input of the string representation
		of each tile. Each row of the room is on a new line.

        Parameters
        ----------
        str_rows : List[str]
            A list of textual representation of each row in the room

        Returns
        -------
        List[List[Tile]]
            The room represented as a nested list of tiles.
		"""
		tiles = []
		width = len(str_rows[0])

		for row_ind in range(len(str_rows)):
			if len(str_rows[row_ind]) != width:
				raise ValueError('Invalid room formation, not Rectangular.')

			row = []
			for col_ind in range(len(str_rows[row_ind])):
				char = str_rows[row_ind][col_ind]
				
				# Throw error if the char is not valid
				if char not in ("0", "1", "2"):
					raise ValueError(f'{char} is not a valid tile character.')

				if char == "0":
					tile = Wall(self._origin_row + row_ind, self._origin_col + col_ind)
					row.append(tile)
				elif char == "1":
					tile = Space(self._origin_row + row_ind, self._origin_col + col_ind)
					row.append(tile)
				elif char == "2":
					tile = Door(self._origin_row + row_ind, self._origin_col + col_ind)
					row.append(tile)

			tiles.append(row)

		return tiles
	

	def add_room_door(self, row, col):
		"""
		Adds a room door in the room at the given position, if position is on the boundary

		Parameters
		----------
		row : int
			row of the tile
		col : int
			column of the tile
		"""
		if not self.is_on_boundary(row, col):
			raise ValueError(f"Cannot add room door to ({row}, {col}), not on boundary.")

		self._tiles[row - self._origin_row][col - self._origin_col] = Door(row, col)
		

	def _is_in_room(self, row, col):
		"""
		Determine whether the given position is within the confines of this room

        Parameters
        ----------
        row : int
			row of the tile
		col : int
			column of the tile

        Returns
        -------
        bool
            Whether the position is in the room
		"""
		return (self._origin_row <= row and row <= self._origin_row + self.get_height() and 
			self._origin_col <= col and col <= self._origin_col + self.get_width())

	def is_on_boundary(self, row, col):
		"""
		Determine whether the given position is on the boundary of this room

        Parameters
        ----------
        row : int
			row of the tile
		col : int
			column of the tile

        Returns
        -------
        bool
            Whether the position is on the boundary of the room
		"""
		
		if not self._is_in_room(row, col):
			return False
		else:
			on_boundary = (self._origin_row == row or self._origin_col == col  or 
				self._origin_row + self.get_height() - 1 == row or self._origin_col + self.get_width() - 1 == col)
			return on_boundary

	def _get_tile(self, row, col):
		"""
		Retrieves the tile from this room at the given position

        Parameters
        ----------
        row : int
			row of the tile
		col : int
			column of the tile

        Returns
        -------
        Tile
            The tile at the position
		"""
		# Ensure the tile is in the room
		if not self._is_in_room(row, col):
			raise ValueError("Cannot retrieve tile, outside of room.")
		return self._tiles[row][col]

	def get_height(self):
		"""
		Retrieves the height of this room

        Returns
        -------
        int
            The height of the room along the x-axis.
		"""
		return len(self._tiles)

	def get_width(self):
		"""
		Retrieves the width of this room

        Returns
        -------
        int
            The width of the room along the y-axis.
		"""
		return len(self._tiles[0])

	def get_row(self):
		"""
		Retrieves row of the upper-most row of the room

        Returns
        -------
        int
            row index of the upper-most row of the room
		"""
		return self._origin_row

	def get_col(self):
		"""
		Retrieves row of the left-most row of the room

        Returns
        -------
        int
            column index of the left-most row of the room
		"""
		return self._origin_col

	def get_tiles(self):
		"""
		Retrieves all of the tiles as one list

		Returns
		-------
		List[Tile]
			A list of all tiles in the room
		"""
		all_tiles = []
		for row in self._tiles:
			all_tiles += row
		return all_tiles

	def get_JSON(self):
		"""
		Retrieves JSON representation of room

		Returns
		-------
		dict
			JSON representation of room
		"""
		tile_layout = [[int(str(tile)) for tile in row] for row in self._tiles]

		as_json = {"type": "room", "origin": [self._origin_row, self._origin_col], 
		"bounds": {"rows": self.get_height(), "columns": self.get_width()},
		"layout": tile_layout}

		return as_json

	def __str__(self):
		"""
		Returns the string representation of the room.
		"""
		output = ""
		for row in self._tiles:
			for tile in row:
				output += str(tile)
			output += '\n'
		return output[:-1]

	def __lt__(self, other):
		"""
		Rooms are ordered by the distance to the origin from their upper left tile,
		or the smallest y coordinate, if equal
		"""
		dist = self._origin_row^2 + self._origin_col^2
		other_dist = other.get_row()^2 + other.get_col()^2

		if dist == other_dist:
			return self._origin_row < other.get_row()
		else:
			return dist < other_dist





