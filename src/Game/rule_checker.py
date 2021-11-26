class RuleChecker:
	def __init__(self, level, combat=False):
		self._level = level
		self._combat = combat

	def player_move_result(self, player, row, col):
		"""
		Retrieves the result of the player attempting to move to the given pos

		Parameters
		----------
		player : AbstractPlayer
			Player to move
		row : int
			Row index of tile to move to
		col : int
			Col index of tile to move to
		
		Returns
		-------
		str
			The result of the move
		"""
		tile = self._get_tile(row, col)
		# Player is not part of the game
		if player is None:
			return 'Nonexistent'

		# Tile does not exist
		if tile is None:
			return "Invalid"
		# Tile outside player reach
		elif abs(player.get_row() - row) + abs(player.get_col() - col) > 2:
			return "Invalid"
		# Tile is current position, skipping turn
		elif player.get_position() == (row, col):
			return "OK"
		# Tile is a player
		elif tile.get_person() is not None and tile.get_person().get_type() == 'player':
			return "Invalid"
		# Tile is wall
		elif tile.get_type() == 'wall':
			return "Invalid"
		# Tile is unlocked exit
		elif tile.is_unlocked():
			return "Exit"
		# Tile has key
		elif tile.has_key():
			return 'Key'
		# Tile is an adversary
		elif tile.get_person() is not None and tile.get_person().get_type() != 'player':
			damage = tile.get_person().get_damage()
			if self._combat:
				health = player.get_health()
			else:
				health = 1

			if health - damage <= 0:
					return "Eject"
			else:
				return f"Damage-{damage}"
		else:
			return 'OK'
	
	def adversary_move_result(self, adversary, row, col):
		"""
		Returns the result of the given adversary moving to the given pos

		Parameters
		----------
		adversary : AbstractAdversary
			Adversary to move
		row : int
			Row index of tile to move to
		col : int
			Col index of tile to move to
		
		Returns
		-------
		str
			Result of the move
		"""
		tile = self._get_tile(row, col)

		# Tile does not exist
		if tile is None:
			return "Invalid"
		# Tile outside adversary reach
		elif abs(adversary.get_row() - row) + abs(adversary.get_col() - col) > 1:
			return "Invalid"
		# Check if attempting to skip move, but valid move available
		elif adversary.get_row() == row and adversary.get_col() == col:
			for p in [(row, col-1),(row-1, col),(row, col+1),(row+1,col)]:
				if self.adversary_move_result(adversary, p[0], p[1]) != "Invalid":
					return "Invalid"
		# Tile contains adversary
		elif tile.get_person() is not None and tile.get_person().get_type() != 'player':
			return "Invalid"
		# Tile is wall and adversary is ghost
		elif tile.get_person() is not None and adversary.get_type() == 'ghost':
			return "Teleport"
		# Tile is wall
		elif tile.get_type() == 'wall':
			return "Invalid"
		# Adversary is zombie and tile is door
		elif adversary.get_type() == 'zombie' and tile.get_type() == 'door':
			return "Invalid"
		# Tile not in room
		elif not self._level.tile_in_room(row, col):
			return "Invalid"
		# Tile contains player
		elif tile.get_person() is not None and tile.get_person().get_type() == 'player':
			damage = adversary.get_damage()
			if self._combat:
				health = tile.get_person().get_health()
			else:
				health = 1
			

			if health - damage <= 0:
					return "Eject"
			else:
				return f"Damage-{damage}"
		# Valid move
		else:
			return 'OK'
		
	def allowed_actor_placement(self, pos):
		"""
		Determines whether the actor is allowed to be placed on the given location

		Parameters
		----------
		pos : (int, int)
			row, col index of tile to place actor

		Returns
		-------
		bool
			Whether the actor can be placed on the tile
		"""
		tile_to_add = self._get_tile(pos[0], pos[1])
		# Tile is not in level
		if tile_to_add is None:
			return False
		# Tile has object
		elif tile_to_add.has_key() or tile_to_add.is_exit():
			return False
		# Tile is wall or door
		elif tile_to_add.get_type() != 'space':
			return False
		# Tile is not in room
		elif not self._level.tile_in_room(pos[0], pos[1]):
			return False
		# Tile is occupied
		elif tile_to_add.get_person() is not None:
			return False
		else:
			return True

	def _get_tile(self, row, col):
		"""
		Retrieve the tile from the given row, col index

		Parameters
		----------
		row : int
			row index of the tile
		col : int
			col index of the tile

		Returns
		-------
		Tile
			tile at the given position
		"""
		try:
			return self._level.get_tile(row, col)
		except:
			return None



