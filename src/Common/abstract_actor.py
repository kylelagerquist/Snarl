from abc import ABC, abstractmethod

class AbstractActor(ABC):
	"""
	Data representation of a Snarl actor

	Parameters
	----------
	name : str
		name of the actor
	"""
	def __init__(self, name, actor_type):
		self._name = name
		self._actor_type = actor_type
		self._row = None
		self._col = None
	
	def get_type(self):
		"""
		Retrieve the type of the actor

		Returns
		-------
		str
			type of the actor
		"""
		return self._actor_type
	
	def get_name(self, first_time=False):
		"""
		Retrieve the name of the actor

		Returns
		-------
		str
			name of actor
		"""
		return self._name
	
	def update_position(self, row, col):
		"""
		Updates the position of the actor
		
		Parameters
		----------
		row : int
			row index of the tile to move to
		col : int
			col index of the tile to move to
		"""
		if row < 0 or col < 0:
			raise ValueError("Row and column must be positive.")
		self._row = row
		self._col = col
	
	def get_row(self):
		"""
		Retrieve the row index of the actor

		Returns
		-------
		int
			row index of the actor
		"""
		return self._row

	def get_col(self):
		"""
		Retrieve the col index of the actor

		Returns
		-------
		int
			col index of the actor
		"""
		return self._col
	
	def get_position(self):
		"""
		Retrieves the row and col index of the actor as a tuple

		Returns
		-------
		(int, int)
			row and col index of the actor
		"""
		return (self._row, self._col)
	
	def get_position_JSON(self):
		"""
		Retrieve the actor-position JSON of the actor

		Returns
		-------
		dict
			actor-position JSON
		"""
		actor_position_json = {
			'type': self.get_type(), 
			'name': self.get_name(),
			'position': self.get_position()
		}
		return actor_position_json
	
	def disconnect(self):
		"""
		Close the actors socket, if remotely connected
		"""
		pass
	
	def __str__(self):
		return f'{self.get_type()} - {self.get_name()} at {self.get_position()}'
	
	def __repr__(self):
		return f'{self.get_type()} - {self.get_name()} at {self.get_position()}'
