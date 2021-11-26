import unittest

from src.Game.game_manager import GameManager
from src.Game.rule_checker import RuleChecker
from src.utils import parse_levels
from src.Player.test_player import TestPlayer

class Test_RuleChecker(unittest.TestCase):
	"""
		{'type': 'state', 'level': 
		{'type': 'level', 'rooms': 
		[{'type': 'room', 'origin': [0, 0], 'bounds': 
		{'rows': 5, 'columns': 8}, 'layout': 
		[[0, 0, 0, 0, 0, 0, 0, 0], 
		[0, 1, 1, 1, 1, 1, 1, 0], 
		[0, 1, 1, 1, 1, 1, 1, 0], 
		[0, 1, 1, 1, 1, 1, 1, 0], 
		[0, 0, 0, 0, 0, 0, 0, 0]]}], 
		
		'hallways': [], 
		'objects': [{'type': 'key', 'position': (2, 1)},
		{'type': 'exit', 'position': (2, 6)}]}, 
		'players': [{'type': 'player', 'name': 'kyle', 'position': (1, 3)}], 
		'adversaries': [{'type': 'zombie', 'name': '360171', 'position': (1, 1)}], 
		'exit-locked': True}
	"""
	def test_invalid_move_player(self):
		"""
		Test moving player to tile that does not exist
		"""
		# Read levels, create game manager and test player
		level_jsons = parse_levels('resources/snarl1.levels')
		gm = GameManager(level_jsons, seed=1, local=True)
		p1 = TestPlayer("kyle", moves=[(2,3), (2,2)])
		# Register player and place actors
		gm.register_player(p1)
		gm._place_actors()
		# Confirm invalid move to move player to non-existent tile
		rule_checker = RuleChecker(gm._current_level)
		move = rule_checker.player_move_result(p1, -5, 100)
		self.assertEqual(move, "Invalid")

	def test_out_of_reach_player(self):
		"""
		Test moving player to tiles that are out of their reach
		"""
		# Read levels, create game manager and test player
		level_jsons = parse_levels('resources/snarl1.levels')
		gm = GameManager(level_jsons, seed=1, local=True)
		p1 = TestPlayer("kyle", moves=[(2,3), (2,2)])
		# Register player and place actors
		gm.register_player(p1)
		gm._place_actors()
		# Confirm invalid move to move player to tiles out of reach
		rule_checker = RuleChecker(gm._current_level)
		self.assertEqual(rule_checker.player_move_result(p1, 2, 1), "Invalid")
		self.assertEqual(rule_checker.player_move_result(p1, 3, 1), "Invalid")
		self.assertEqual(rule_checker.player_move_result(p1, 3, 2), "Invalid")
		self.assertEqual(rule_checker.player_move_result(p1, 3, 4), "Invalid")
		self.assertEqual(rule_checker.player_move_result(p1, 3, 5), "Invalid")
		self.assertEqual(rule_checker.player_move_result(p1, 2, 5), "Invalid")
		self.assertEqual(rule_checker.player_move_result(p1, 1, 6), "Invalid")
	
	def test_invalid_move_wall_player(self):
		"""
		Test moving player to tile that is a wall
		"""
		# Read levels, create game manager and test player
		level_jsons = parse_levels('resources/snarl1.levels')
		gm = GameManager(level_jsons, seed=1, local=True)
		p1 = TestPlayer("kyle", moves=[(2,3), (2,2)])
		# Register player and place actors
		gm.register_player(p1)
		gm._place_actors()
		# Confirm invalid move to move player to tile that is a wall
		rule_checker = RuleChecker(gm._current_level)
		move = rule_checker.player_move_result(p1, 0, 0)
		self.assertEqual(move, "Invalid")
	
	def test_skip_turn_player(self):
		"""
		Test skipping a player turn
		"""
		# Read levels, create game manager and test player
		level_jsons = parse_levels('resources/snarl1.levels')
		gm = GameManager(level_jsons, seed=1, local=True)
		p1 = TestPlayer("kyle", moves=[(2,3), (2,2)])
		# Register player and place actors
		gm.register_player(p1)
		gm._place_actors()
		# Confirm OK move when skipping player turn
		rule_checker = RuleChecker(gm._current_level)
		self.assertEqual(rule_checker.player_move_result(p1, 1, 3), "OK")
	
	def test_locked_exit_player(self):
		"""
		Test moving player to exit that is locked
		"""
		# Read levels, create game manager and test player
		level_jsons = parse_levels('resources/snarl1.levels')
		gm = GameManager(level_jsons, seed=1, local=True)
		p1 = TestPlayer("kyle", moves=[(1,5), (2,2)])
		# Register player and place actors
		gm.register_player(p1)
		gm._place_actors()
		gm._play_turn()
		# Confirm player does not exit when moving to locked exit
		rule_checker = RuleChecker(gm._current_level)
		self.assertEqual(rule_checker.player_move_result(p1, 2, 6), "OK")
	
	def test_key_player(self):
		"""
		Test moving player to a key
		"""
		# Read levels, create game manager and test player
		level_jsons = parse_levels('resources/snarl1.levels')
		gm = GameManager(level_jsons, seed=1, local=True)
		p1 = TestPlayer("kyle", moves=[(3,3),(3,2),(2,1)])
		# Register player and place actors
		gm.register_player(p1)
		gm._place_actors()
		gm._play_turn()
		gm._play_turn()
		# Confirm player picks up key
		rule_checker = RuleChecker(gm._current_level)
		self.assertEqual(rule_checker.player_move_result(p1, 2, 1), "Key")
	
	def test_eject_player(self):
		"""
		Test moving player to an adversary without combat system
		"""
		# Read levels, create game manager and test player
		level_jsons = parse_levels('resources/snarl1.levels')
		gm = GameManager(level_jsons, seed=1, local=True)
		p1 = TestPlayer("kyle", moves=[(3,3),(3,2),(2,1)])
		# Register player and place actors
		gm.register_player(p1)
		gm._place_actors()
		# Confirm player ejected
		rule_checker = RuleChecker(gm._current_level)
		self.assertEqual(rule_checker.player_move_result(p1, 1, 1), "Eject")
	
	def test_eject_combat_player(self):
		"""
		Test moving player to an adversary with combat system
		"""
		# Read levels, create game manager and test player
		level_jsons = parse_levels('resources/snarl1.levels')
		gm = GameManager(level_jsons, seed=1, local=True)
		p1 = TestPlayer("kyle", moves=[(3,3),(3,2),(2,1)])
		# Register player and place actors
		gm.register_player(p1)
		gm._place_actors()
		# Confirm player recieves damage
		rule_checker = RuleChecker(gm._current_level, combat=True)
		self.assertEqual(rule_checker.player_move_result(p1, 1, 1), "Damage-60")
	
	def test_actor_placement_invalid(self):
		"""
		Test invalid actor placements
		"""
		# Read levels, create game manager and test player
		level_jsons = parse_levels('resources/snarl1.levels')
		gm = GameManager(level_jsons, seed=1, local=True)
		p1 = TestPlayer("kyle", moves=[(3,3),(3,2),(2,1)])
		# Register player and place actors
		gm.register_player(p1)
		gm._place_actors()
		
		rule_checker = RuleChecker(gm._current_level, combat=True)
		# Placing actor on adversary
		self.assertEqual(rule_checker.allowed_actor_placement((1,1)), False)
		# Placing actor on player
		self.assertEqual(rule_checker.allowed_actor_placement((1,3)), False)
		# Placing actor on key
		self.assertEqual(rule_checker.allowed_actor_placement((2,1)), False)
		# Placing actor on exit
		self.assertEqual(rule_checker.allowed_actor_placement((2,6)), False)
		# Placing actor on non existent tile
		self.assertEqual(rule_checker.allowed_actor_placement((-1,6)), False)
		# Placing actor on wall
		self.assertEqual(rule_checker.allowed_actor_placement((0,0)), False)
	
	
	
	
if __name__ == '__main__':
	unittest.main()