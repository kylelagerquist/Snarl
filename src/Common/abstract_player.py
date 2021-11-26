from abc import ABC, abstractmethod
from .abstract_actor import AbstractActor

class AbstractPlayer(AbstractActor):
	def __init__(self, name):
		self._player_state = None
		self._ejected = False
		self._exited = False
		self._times_exited = 0
		self._times_ejected = 0
		self._keys_found = 0
		self._health = 100
		super().__init__(name, actor_type="player")
	
	def update_state(self, state: dict):
		"""
		Updates the players knowledge of the game state
		"""
		self._player_state = state

	@abstractmethod
	def request_move(self):
		"""
		Requests the user to input a move to be sent to manager to be handled
		"""
		pass
	
	@abstractmethod
	def render_view(self):
		"""
		Render's the player's current knowledge of the state
		"""
		pass
	
	
	def send_message(self, msg):
		"""
		Send the given message to the player

		Parameters
		----------
		msg : str
			Message to be sent
		"""
		pass
	
	def reduce_health(self, points_to_remove: int):
		"""
		Remove the given amount of health points from the player
		"""
		self._health -= points_to_remove
	
	def get_health(self):
		"""
		Retrieve the players health
		"""
		return self._health
	
	def eject(self):
		"""
		Change the player's ejected status
		"""
		self._ejected = True
		self._row = None
		self._col = None
		self._times_ejected += 1

	def is_ejected(self):
		"""
		Return whether the player has been ejected from the level

		Returns
		-------
		bool
			Whether the player has been ejected
		"""
		return self._ejected

	def exit(self):
		"""
		Change the player's status to exited
		"""
		self._exited = True
		self._row = None
		self._col = None
		self._times_exited += 1

	def is_exited(self):
		"""
		Return whether the player has exited from the level

		Returns
		-------
		bool
			Whether the player has been ejected
		"""
		return self._exited
	
	def found_key(self):
		"""
		Increase number of keys the player has found
		"""
		self._keys_found += 1
	
	def return_to_game(self):
		"""
		Returns the player to the game
		"""
		self._ejected = False
		self._exited = False
		self._health = 100
	
	def is_active(self):
		"""
		Retrieve whether a player's active in the game 

		Return
		------
		bool
			Whether the player is not ejected and not exited
		"""
		return not (self._ejected or self._exited)
	
	def get_player_score_json(self):
		"""
		Retrieves the (player-score) JSON object

		Returns
		-------
		dict
			(player-score) dict
		"""
		player_score_json = {
			"type": "player-score",
			"name": self._name,
			"exits": self._times_exited,
			"ejects": self._times_ejected,
			"keys": self._keys_found
		}
		return player_score_json