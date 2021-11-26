from abc import ABC, abstractmethod

class Tile(ABC):
	"""
	Data representation for a tile in the game. A tile can either be an empty space, wall, or door.

	Parameters
	----------
	row : int
		row of the tile
	col : int
		column of the tile
	"""
	def __init__(self, row, col):
		if row < 0 or col < 0:
			raise ValueError("Row and column must be positive.")
		self._row = row
		self._col = col
		super().__init__()

	def get_row(self):
		"""
		Retrieves the row of the tile.

		Returns
		-------
        int
            Row of the tile
		"""
		return self._row

	def get_col(self):
		"""
		Retrieves the column of the tile.

		Returns
		-------
        int
            Column of the tile
		"""
		return self._col
	
	def get_position(self):
		"""
		Retrieves the position of the tile.

		Returns
		-------
        (int, inw)
            Row and column index of tie tile
		"""
		return (self._row, self._col)

	@abstractmethod
	def has_key(self):
		"""
		Determines whether the tile contains a key

		Returns
		-------
        bool
            Whether the tile contains a key
		"""
		pass
	
	@abstractmethod
	def is_exit(self):
		"""
		Determines whether the tile is a level exit

		Returns
		-------
        bool
            Whether the tile is a level exit
		"""
		pass
	
	@abstractmethod
	def is_unlocked(self):
		"""
		Determines whether the tile is unlocked

		Returns
		-------
		bool
			Whether or not the tile is unlocked
		"""
		pass
	
	@abstractmethod
	def get_person(self):
		"""
		Retrieves the person on the space, or None if it is not occupied.

		Returns
		-------
		Person
			Person occupying the space or None
		"""
		pass

class Space(Tile):
	"""
	A space is a tile that people can move onto, possibly contain an item, or an exit.

	Parameters
	----------
	row : int
		row of the tile
	col : int
		column of the tile
	"""
	def __init__(self, row, col):
		self._person = None
		self._has_key = False
		self._level_exit = False
		self._is_unlocked = False
		super().__init__(row, col)

	def add_person(self, person):
		"""
		Attempts to add a person to the space. Unable to add person if the space is occupied.

		Parameters
		----------
		person : Person
			Person object to add to the space

		Returns
        -------
        bool
            Whether the person was successfully added to the space or not.
		"""
		if self._person is None:
			self._person = person
			return True
		else:
			return False

	def get_person(self):
		"""
		Retrieves the person on the space, or None if it is not occupied.

		Returns
		-------
		Person
			Person occupying the space or None
		"""
		return self._person

	def remove_person(self):
		"""
		Removes person from tile
		"""
		self._person = None

	def add_key(self):
		"""
		Adds a key to the tile
		"""
		if self.is_exit():
			raise ValueError("Cannot add key to tile that is exit.")
		else:
			self._has_key = True

	def has_key(self):
		"""
		Determines whether the tile contains a key

		Returns
		-------
		bool
			Whether or not the tile is a level exit
		"""
		return self._has_key

	def remove_key(self):
		"""
		Adds a key to the tile
		"""
		self._has_key = False

	def add_level_exit(self):
		"""
		Adds level exit to the tile
		"""
		if self.has_key():
			raise ValueError("Cannot add exit to tile that has key.")
		else:
			self._level_exit = True

	def is_exit(self):
		"""
		Determines whether the tile is a level exit

		Returns
		-------
		bool
			Whether or not the tile is a level exit
		"""
		return self._level_exit

	def is_unlocked(self):
		"""
		Determines whether the tile is unlocked

		Returns
		-------
		bool
			Whether or not the tile is unlocked
		"""
		return self._is_unlocked

	def unlock(self):
		"""
		Unlocks the tile if it is a level exit
		"""
		if self.is_exit:
			self._is_unlocked = True

	def get_type(self):
		"""
		Retrieves the tile type

		Returns
		-------
		str
			Tile type
		"""
		return "space"

	def __str__(self):
		return "1"

	def __repr__(self):
		return "1"

	def __eq__(self, other):
		if isinstance(other, Space):
			return self._row == other.get_row() and self._col == other.get_col()
		return False


class Door(Tile):
	"""
	A door is a tile that is the connection between a hallway and room.

	Parameters
	----------
	row : int
		row of the tile
	col : int
		column of the tile
	"""
	def __init__(self, row, col):
		self._person = None
		self._has_key = False
		self._level_exit = False
		self._is_unlocked = False
		super().__init__(row, col)

	def add_person(self, person):
		"""
		Attempts to add a person to the space. Unable to add person if the space is occupied.

		Parameters
		----------
		person : Person
			Person object to add to the space

		Returns
        -------
        bool
            Whether the person was successfully added to the space or not.
		"""
		if self._person is None:
			self._person = person
			return True
		else:
			return False

	def get_person(self):
		"""
		Retrieves the person on the space, or None if it is not occupied.

		Returns
		-------
		Person
			Person occupying the space or None
		"""
		return self._person

	def remove_person(self):
		"""
		Removes person from tile
		"""
		self._person = None

	def add_key(self):
		"""
		Adds a key to the tile
		"""
		if self.is_exit():
			raise ValueError("Cannot add key to tile that is exit.")
		else:
			self._has_key = True

	def has_key(self):
		"""
		Determines whether the tile contains a key

		Returns
		-------
		bool
			Whether or not the tile is a level exit
		"""
		return self._has_key

	def remove_key(self):
		"""
		Adds a key to the tile
		"""
		self._has_key = False

	def add_level_exit(self):
		"""
		Adds level exit to the tile
		"""
		if self.has_key():
			raise ValueError("Cannot add exit to tile that has key.")
		else:
			self._level_exit = True

	def is_exit(self):
		"""
		Determines whether the tile is a level exit

		Returns
		-------
		bool
			Whether or not the tile is a level exit
		"""
		return self._level_exit

	def is_unlocked(self):
		"""
		Determines whether the tile is unlocked

		Returns
		-------
		bool
			Whether or not the tile is unlocked
		"""
		return self._is_unlocked

	def unlock(self):
		"""
		Unlocks the tile if it is a level exit
		"""
		if self.is_exit:
			self._is_unlocked = True

	def get_type(self):
		return "door"

	def __str__(self):
		return "2"

	def __repr__(self):
		return "2"

	def __eq__(self, other):
		if isinstance(other, Door):
			return self._row == other.get_row() and self._col == other.get_col()
		return False

class Wall(Tile):
	def has_key(self):
		return False
	
	def is_exit(self):
		return False
	
	def is_unlocked(self):
		return False
	
	def get_person(self):
		return None

	def get_type(self):
		return "wall"

	def __str__(self):
		return "0"

	def __repr__(self):
		return "0"

	def __eq__(self, other):
		if isinstance(other, Wall):
			return self._row == other.get_row() and self._col == other.get_col()
		return False

