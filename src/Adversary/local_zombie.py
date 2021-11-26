from ..Common.abstract_adversary import AbstractAdversary
from ..Game.state import State
import random


class LocalZombie(AbstractAdversary):
	"""
	Data representation for a local zombie adversary in Snarl which automatically
	provides moves based upon the state of the game

	Parameters
	----------
	name : str
		Name of the adversary
	"""
	def __init__(self, name=None):
		super().__init__(name, adv_type='zombie', damage=60)
	
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
		# No player in room, random move
		if player_in_room_pos == []:
			return random.choice(valid_moves)
		# Player in room, move closer to them
		else:
			closest = None
			dist = 999999999999
			for player_pos in player_in_room_pos:
				for move_pos in valid_moves:
					calc = ((player_pos[0] - move_pos[0])**2 + (player_pos[1] - move_pos[1])**2) ** .5
					if calc < dist:
						closest = move_pos
						dist = calc
			return closest
	
	def _get_valid_moves(self):
		"""
		Zombies can move on spaces, not occupied by another adversary, within
		one tile
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
			# Tile cannot be a door or a wall
			if tile is None or tile != 1:
				continue
			# Tile is occupied by adversary
			elif self._state.tile_has_adversary(pos):
				continue
			else:
				valid.append(pos)
		return valid