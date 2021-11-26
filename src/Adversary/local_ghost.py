from ..Common.abstract_adversary import AbstractAdversary
from ..Game.state import State

class LocalGhost(AbstractAdversary):
	"""
	Data representation for a local ghost adversary in Snarl which automatically
	provides moves based upon the state of the game

	Parameters
	----------
	name : str
		Name of the adversary
	"""
	def __init__(self, name=None):
		super().__init__(name, adv_type='ghost', damage=40)
	
	def update_state(self, state):
		"""
		Updates the ghost's knowledge of the game state

		Parameters
		----------
		state : state-dict
			(state) JSON object
		"""
		self._state = State(state)

		# Locate this adversaries location in the level and update its position
		for adversary in state['adversaries']:
			if adversary['name'] == self._name:
				self._row = adversary['position'][0]
				self._col = adversary['position'][1]
	
	def request_move(self):
		"""
		Requests a move from the adversary

		Returns
		-------
		(int, int)
			Row and column index to move to
		"""
		valid_moves = self._get_valid_moves()
		# Skip move if there are no valid moves
		if valid_moves == []:
			return self.get_position()
		
		player_in_room_pos = self._state.players_in_room(self.get_position())
		
		# No player in room, move to wall or first valid tile
		if player_in_room_pos == []:
			for move_pos in valid_moves:
				tile = self._state.get_tile(move_pos)
				if tile == 0:
					return move_pos
			return valid_moves[0]
		# Player in room, only valid tiles are wall
		elif all(self._state.get_tile(p) == 0 for p in valid_moves):
			return valid_moves[0]
		# Player in room, move closer to them
		else:
			closest = None
			dist = 999999999999
			for player_pos in player_in_room_pos:
				for move_pos in valid_moves:
					tile = self._state.get_tile(move_pos)
					if tile == 0:
						continue
					calc = ((player_pos[0] - move_pos[0])**2 + (player_pos[1] - move_pos[1])**2) ** .5
					if calc < dist:
						closest = move_pos
						dist = calc
			return closest

	def _get_valid_moves(self):
		"""
		Retreive valid positions a ghost can move to. Must be space or wall within
		one tile, not occupied by adversary

		Returns
		-------
		List[(int, int)]
			Valid row, column indices ghost can move to
		"""
		card_pos = [
			(self._row + 1, self._col),
			(self._row, self._col + 1),
			(self._row - 1, self._col),
			(self._row, self._col - 1),
		]
		valid = []

		for pos in card_pos:
			tile = self._state.get_tile(pos)
			# Tile is out of bounds or door
			if tile is None or tile == 2:
				continue
			# Tile is occupied by adversary
			elif self._state.tile_has_adversary(pos):
				continue
			else:
				valid.append(pos)
		return valid