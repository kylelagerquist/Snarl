from ..Common.abstract_player import AbstractPlayer

class TestPlayer(AbstractPlayer):
	"""
	Test player which is given list of moves to supply

	Parameters
	----------
	name : str
		Name of the player
	moves : List[(int, int)]
		List of row, col indices for player to move to
	"""
	def __init__(self, name, moves):
		self._name = name
		self._moves = moves
		super().__init__(name)
	
	def request_move(self):
		"""
		Returns the next move in the players move list, or their current location
		if out of moves

		Returns
		-------
		(int, int)
			row, col index to move to
		"""
		try:
			move = self._moves.pop(0)
		except IndexError:
			move = self.get_position()
		
		return move
	
	def render_view(self):
		"""
		Render's the player's current knowledge of the state
		"""
		pass
		





