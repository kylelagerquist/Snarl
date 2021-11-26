import json
import random
import math
import os.path

from .level import Level
from ..Adversary.local_zombie import LocalZombie
from ..Adversary.local_ghost import LocalGhost
from .rule_checker import RuleChecker
from ..utils import build_player_update, send_level_start, send_end_level

class GameManager:
	"""
	Data representation of a Game Manager for Snarl.

	Parameters
	----------
	levels : List[level_json]
		List of levels representing the levels the players must progress through
	start_level_num : int, default 1
		Level to start on, first level is level 1
	combat : bool, default False
		Whether or not use the HP system, if false players ejected on adversary
		contact
	seed : int, default None
		Seed to use for randomization of tiles for actor placement
	local : bool, default False
		Whether game is being ran without server
	game_id : int, default 0
		ID to used to distinguish game
	"""
	def __init__(self, level_jsons, start_level_num=1, combat=False, seed=None, 
	local=False, game_id = 0):
		if start_level_num < 1 or start_level_num > len(level_jsons):
			raise ValueError("Invalid level start number.")

		self._levels = [Level(level_json) for level_json in level_jsons]
		self._level_num = start_level_num
		self._players = [] # Players registered
		self._adversaries = [] # Adversaries in current level
		self._remote_adversaries = [] # Remote adversaries registered
		self._observers = [] # Observers
		self._game_in_progress = False # Whether game is in progress
		self._current_level = self._levels[start_level_num - 1]
		self._combat = combat
		self._seed = seed
		self._id = game_id

		# If game is being ran without server, need to reset server_log file
		if local:
			server_data = {"player_names": [], "player_scores": []}
			server_log_path = os.path.join(os.getcwd(), 'src/server_log.json')
			with open(server_log_path, 'w') as server_file:
				json.dump(server_data, server_file)
		print(f'Game {self._id}: Intialized')
	
	def register_player(self, player):
		"""
		Registers the player to the game

		Parameters
		----------
		player : AbstractPlayer
			Player to register
		"""
		if self._game_in_progress:
			raise ValueError('Cannot add player, game in progress')
		if len(self._players) >= 4:
			raise ValueError('Cannot add player, 4 players registered')

		# Send a welcome message to the player
		github = "https://github.ccs.neu.edu/CS4500-S21/Londorthel/"
		server_welcome = {"type": "welcome", "info": github}
		player.send_message(json.dumps(server_welcome))

		# Open server log to get names in use across server
		server_log_path = os.path.join(os.getcwd(), 'src/server_log.json')
		with open(server_log_path) as server_file:
			server_data = json.load(server_file)

		# Ask player up to 5 times for unique name
		for _ in range(5):
			# Request name
			name = player.get_name(first_time=True)

			# Check if name is unique
			if name not in server_data['player_names']:
				self._players.append(player)

				server_data['player_names'].append(name)
				# Add name to the server log
				with open(server_log_path, 'w') as server_file:
					json.dump(server_data, server_file)
				
				print(f'Game {self._id}: {name} Added')
				return True
	
	def register_adversary(self, adversary):
		"""
		Registers the remote adversary connection to the game. Will be used as
		adversary if spot is available

		Parameters
		----------
		adversary : RemoteAdversary
			Adversary to register
		"""
		self._remote_adversaries.append(adversary)
		print(f'Game {self._id}: Remote Adversary Added')
	
	def register_observer(self, observer):
		"""
		Registers the given observer

		Parameters
		----------
		observer : AbstractObserver
			Observer to register
		"""
		self._observers.append(observer)

	def play_game(self):
		"""
		Starts the level and continues gameplay by prompting actors to provide
		a move until the level is over
		"""
		self._game_in_progress = True
		# Place all players and actors in new level
		self._place_actors()
		# Send level start JSONS
		send_level_start(self._players, self._level_num)
		# Issue updates to all players and observers
		self.update_observers()
		self.update_players()
		# Continue gameplay until level is over
		while not self._is_level_over():
			self._play_turn()
		send_end_level(self._players, self._current_level.who_unlocked())
		# Level is over, decide what to do next
		self._next_level()
	
	def _play_turn(self):
		"""
		A single turn is comprised of accepting a move from each active player
		and then each adversary
		"""
		for player in self._players:
			if self._is_level_over():
				return
			if not player.is_active():
				continue
			
			# Ask the player for up to 5 moves before skipping
			for _ in range(5):
				move = player.request_move()
				move_result = self.move_player(player, move[0], move[1])
				player.send_message(json.dumps(move_result))
				print(f'Game {self._id}: {player.get_name()} move to {move} ({move_result})')

				if move_result not in ('Nonexistent', 'Invalid'):
					self.update_players()
					self.update_observers()
					break
		
		for adversary in self._adversaries:
			if self._is_level_over():
				return
			adversary.update_state(self._current_level.build_state())
			for _ in range(5):
				move = adversary.request_move()
				move_result = self.move_adversary(adversary, move[0], move[1])
				print(f'Game {self._id}: {adversary.get_name()} move to {move} ({move_result})')

				if move_result not in ('Nonexistent', 'Invalid'):
					self.update_players()
					self.update_observers()
					break
	
	def _place_actors(self):
		"""
		Places all of the players and creates adversaries to be added to valid
		tiles
		"""
		self._adversaries = self._get_adversaries()	
		tile_pos = [t.get_position() for t in self._current_level.get_tiles()]
		random.Random(self._seed).shuffle(tile_pos)
		
		for actor in self._players + self._adversaries:
			rule_checker = RuleChecker(self._current_level, self._combat)
			while True:
				try:
					rand_pos = tile_pos.pop(0)
				except:
					raise ValueError('Not enough tiles to place actors.')

				if rule_checker.allowed_actor_placement(rand_pos):
					actor.update_position(rand_pos[0], rand_pos[1])
					tile = self._current_level.get_tile(rand_pos[0], rand_pos[1])
					tile.add_person(actor)
					break
	
	def _get_adversaries(self):
		num_zombies = math.floor(self._level_num / 2 + 1)
		num_ghosts = math.floor((self._level_num - 1) / 2)
		adversaries = ['zombie'] * num_zombies + ['ghost'] * num_ghosts

		for i in range(len(adversaries)):
			if i < len(self._remote_adversaries):
				remote_adversary = self._remote_adversaries[i]
				remote_adversary.declare_type(adversaries[i])
				actor_to_add = remote_adversary
			elif adversaries[i] == 'zombie':
				actor_to_add = LocalZombie()
			else:
				actor_to_add = LocalGhost()
			
			adversaries[i] = actor_to_add

		return adversaries
	
	def end_game(self):
		"""
		Compile the end game JSON to be sent to all the players
		"""
		# Retrieve all player scores in this game
		player_scores = [p.get_player_score_json() for p in self._players]

		# Retrieve scores from other games
		server_log_path = os.path.join(os.getcwd(), 'src/server_log.json')
		with open(server_log_path, 'r') as server_file:
			server_data = json.load(server_file)
		
		# Add this games scores and output new file
		server_data['player_scores'] += player_scores
		with open(server_log_path, 'w') as server_file:
			json.dump(server_data, server_file)

		end_game_json = {"type": "end-game", "scores": player_scores}
		server_scores_json = {
			"type": "server-scores", 
			"scores": server_data['player_scores']
		}
		 
		for p in self._players:
			p.send_message(json.dumps(end_game_json))
			p.send_message(json.dumps(server_scores_json))
		
		# Disconnect all players
		for actor in self._players + self._remote_adversaries:
			actor.disconnect()

	def _next_level(self):
		"""
		Progresses the game at the end of the level by either moving to the 
		next level or ending the game
		"""
		successful = False

		# Check if any player exited
		for player in self._players:
			if player.is_exited():
				successful = True
		
		# All players ejected, game over
		if not successful:
			print(f'Game {self._id}: Game over, unsuccessful')
			self.end_game()
		# A player exited and it was the last level
		elif self._level_num == len(self._levels):
			print(f'Game {self._id}: Game over, successful')
			self.end_game()
		# A player exited, move to next level:
		else:
			print(f'Game {self._id}: Level {self._level_num} complete')
			self._level_num += 1
			self._current_level = self._levels[self._level_num - 1]

			for player in self._players:
				player.return_to_game()

			self.play_game()
			
	def _is_level_over(self):
		"""
		Determines if a level is over (all players ejected or exited)
		"""
		for player in self._players:
			if player.is_active():
				return False
		return True
	
	def update_players(self):
		"""
		Update all the players
		"""
		for player in self._players:
			if not player.is_active():
				continue
			player_update = build_player_update(player, self._current_level)
			player.update_state(player_update)
	
	def move_player(self, player, row, col):
		"""
		Moves a player to the given tile

		Parameters
		----------
		player : AbstractPlayer
			Player to move
		row : int
			row index of the tile to move to
		col : int
			col index of the tile to move to
		"""
		rule_checker = RuleChecker(self._current_level, self._combat)
		move_result = rule_checker.player_move_result(player, row, col)
		
		# The player does not exist in the game, or it is an invalid point
		if move_result in ('Nonexistent', 'Invalid'):
			return move_result

		from_tile = self._current_level.get_tile(player.get_row(), player.get_col())
		to_tile = self._current_level.get_tile(row, col)
		
		# Player was ejected, remove them from their tile, and update status
		if move_result == 'Eject':
			from_tile.remove_person()
			player.eject()
		# Player has exited, remove them from their tile, and update status
		elif move_result == 'Exit':
			from_tile.remove_person()
			player.exit()
		# Player landed on key, remove key, unlock exit, update player and tile
		elif move_result == 'Key':
			self._current_level.remove_key(player.get_name())
			self._current_level.unlock_exit()
			from_tile.remove_person()
			to_tile.add_person(player)
			player.update_position(row, col)
		# Other valid move, update player and tile
		elif move_result == 'OK':
			from_tile.remove_person()
			to_tile.add_person(player)
			player.update_position(row, col)
		# Player recieved damage, remain on tile update health
		elif 'Damage' in move_result:
			amount = int(move_result.split('-')[-1])
			player.reduce_health(amount)

		return move_result
	
	def move_adversary(self, adversary, row, col):
		"""
		Attempt to move an adversary to the given row and col. Remain put if the
		tile is occupied by a player and the adversary can not inflict enough
		damage to eject the player

		Parameters
		----------
		adversary : AbsractAdversary
			adversary to move
		row : int
			row index to move to
		col : int
			col index to move to
		
		Returns
		-------
		str
			Result of the move
		"""
		rule_checker = RuleChecker(self._current_level, self._combat)
		move_result = rule_checker.adversary_move_result(adversary, row, col)

		# The player does not exist in the game, or it is an invalid point
		if move_result in ('Nonexistent', 'Invalid'):
			return move_result
		
		from_tile = self._current_level.get_tile(adversary.get_row(), adversary.get_col())
		to_tile = self._current_level.get_tile(row, col)

		# Adversary landed on player
		if move_result == 'Eject':
			to_tile.get_person().eject()
			to_tile.remove_person()
			to_tile.add_person(adversary)
			from_tile.remove_person()
			adversary.update_position(row, col)
		# Adversary dealt damage to player
		elif 'Damage' in move_result:
			amount = int(move_result.split('-')[-1])
			to_tile.get_person().reduce_health(amount)
		# Valid move
		elif move_result == 'OK':
			from_tile.remove_person()
			to_tile.add_person(adversary)
			adversary.update_position(row, col)
		# Adversary is ghost, moved to wall, needs to teleport
		elif move_result == 'Teleport':
			tile_pos = [t.get_position() for t in self._current_level.get_tiles()]
			random.Random().shuffle(tile_pos)

			for p in tile_pos:
				if rule_checker.allowed_actor_placement(p):
					from_tile.remove_person()
					self._current_level.get_tile(p[0], p[1]).add_person(adversary)
					adversary.update_position(p[0], p[1])
					break
		
		return move_result
	
	def update_observers(self):
		"""
		Update all observers
		"""
		for observer in self._observers:
			print(f'GAME {self._id}: VIEW')
			observer.update_state(self._current_level.build_state())


	

		