from abc import ABC, abstractmethod
from .abstract_actor import AbstractActor
from ..Game.state import State
import random

class AbstractAdversary(AbstractActor):
	def __init__(self, name, adv_type, damage):
		self._damage = damage
		if name is None:
			self._name = str(random.randint(1,1000000))
		else:
			self._name = name
		self._state = None
		super().__init__(self._name, actor_type=adv_type)
	
	def update_state(self, state):
		"""
		Updates the adversary's knowledge of the game state

		Parameters
		----------
		state : dict
			JSON object containing state data such as the level, players, 
			adversaries, and exit status
		"""
		self._state = State(state)
	
	def get_damage(self):
		"""
		Retrieve the amount of damage the adversary can disburse

		Returns
		-------
		int
			Amount of damage the adversary can give
		"""
		return self._damage

	@abstractmethod
	def request_move(self):
		"""
		Requests a move from the adversary

		Returns
		-------
		(int, int)
			Row and column index to move to
		"""
		pass

	
