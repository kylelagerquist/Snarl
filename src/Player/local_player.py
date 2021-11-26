import json

from ..Common.abstract_player import AbstractPlayer

class LocalPlayer(AbstractPlayer):
	"""
	Supports use of local player, where moves are supplied via STDIN and their
	knowledge of the game is viewed through STDOUT
	"""
	def __init__(self):
		super().__init__(None)
	
	def get_name(self, first_time=False):
		"""
		Retrieve the players name, or ask them to set their name if they have not

		Returns
		-------
		str
			Name of the player
		"""
		if not first_time:
			return self._name
			
		while True:
			name = input('Enter name: ')
			
			# Check if name only contains alpha-numeric characters
			if name.isalnum():
				self._name = name
				return name
			else:
				print('Invalid name: alpha-numeric characters only')
	
	def request_move(self):
		"""
		Prompts the user to enter a row and column index to move to

		Returns
		-------
		(int, int)
			Row and column index for player to move to
		"""
		self.render_view()
		row = None
		col = None
		# Continue asking player for move until valid row col index entered
		while True:
			if row is None:
				user_input = input('Enter row index to move to: ')
				try:
					user_input = int(user_input)
					row = user_input
				except:
					continue
			elif col is None:
				user_input = input('Enter col index to move to: ')
				try:
					user_input = int(user_input)
					col = user_input
				except:
					continue
			else:
				break
		row = self._player_state['position'][0] + row - 2
		col = self._player_state['position'][1] + col - 2
		return (row, col)
	
	def render_view(self):
		"""
		Renders the player's knowledge of the level
		"""
		print(f'\nPLAYER ({self._name}) VIEW')
		if self._player_state is None:
			print('No state to render')
			return
		print(f'HEALTH: {self._player_state["health"]}')
		layout_rows = self._player_state['layout']

		for thing in self._player_state['objects'] + self._player_state['actors']:
			symbol = self._get_symbol(thing['type'])
			if symbol is not None:
				if thing['position'][0] is None:
					print(thing)
					continue
				row = 2 + thing['position'][0] - self._player_state['position'][0]
				col = 2 + thing['position'][1] - self._player_state['position'][1]
			
				layout_rows[row][col] = symbol
				
		for row in layout_rows:
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