from ..Common.abstract_observer import AbstractObserver
from ..Game.state import State
import json

class LocalObserver(AbstractObserver):
	def __init__(self):
		self._state = None

	def update_state(self, state_update):
		self._state = State(state_update)
		self.render_view()
	
	def render_view(self):
		
		if self._state is None:
			print('No state to render')
			return
		
		layout = self._state.get_layout()
		state_json = self._state.get_json()

		other_things = state_json['level']['objects'] + state_json['players'] + state_json['adversaries']
		
		for thing in other_things:
			symbol = self._get_symbol(thing['type'])
			if symbol is not None:
				layout[thing['position'][0]][thing['position'][1]] = symbol
		
		for row in layout:
			print(' '.join([str(tile) for tile in row]))
		print('\n')
	
	def _get_symbol(self, actor_obj_type):
		actor_obj_map = {
			"key": "K",
			"exit": "E",
			"player": "P",
			"zombie": "Z",
			"ghost": "G",
		}
		if actor_obj_type in actor_obj_map:
			return actor_obj_map[actor_obj_type]
		else:
			return None