import unittest

from src.Game.game_manager import GameManager
from src.utils import parse_levels
from src.Player.test_player import TestPlayer

class Test_GameManager(unittest.TestCase):
	"""
	Shuffled snarl1.levels tiles with seed=1
	[(2, 7), (0, 2), (1, 3), (0, 1), (4, 5), (4, 0), (0, 5), (1, 1), 
	(2, 1), (3, 5), (4, 2), (2, 4), (4, 6), (2, 5), (3, 3), (2, 6), 
	(1, 2), (4, 1), (2, 2), (4, 3), (4, 7), (1, 6), (3, 2), (2, 3), 
	(1, 5), (1, 4), (0, 0), (1, 7), (0, 3), (0, 6), (3, 1), (3, 0), 
	(3, 6), (3, 4), (3, 7), (0, 7), (2, 0), (0, 4), (4, 4), (1, 0)]
	"""
	def test_eject(self):
		"""
		Test a player being properly ejected
		"""
		# Read levels, create game manager and test player
		level_jsons = parse_levels('resources/snarl1.levels')
		gm = GameManager(level_jsons, seed=1, local=True)
		p1 = TestPlayer("kyle", moves=[(2,3), (2,2)])
		# Register player and place actors
		gm.register_player(p1)
		gm._place_actors()
		# Confirm actors places correctly (first allowed random tile)
		state = gm._current_level.build_state()
		self.assertEqual(p1.get_position(), (1, 3))
		self.assertEqual(state['adversaries'][0]['position'], (1, 1))
		# Play first turn, ensure player moved correct location and zombie
		# moved closer to player
		gm._play_turn()
		state = gm._current_level.build_state()
		self.assertEqual(p1.get_position(), (2, 3))
		self.assertEqual(state['adversaries'][0]['position'], (1, 2))
		# Play another turn, ejecting player
		gm._play_turn()
		state = gm._current_level.build_state()
		self.assertEqual(p1.is_ejected(), True)
		self.assertEqual(state['adversaries'][0]['position'], (2, 2))
		self.assertEqual(gm._is_level_over(), True)
	
	def test_full_level(self):
		"""
		Test the game play functionality of whole snarl level
		"""
		# Read levels, create game manager and test player
		level_jsons = parse_levels('resources/snarl1.levels')
		gm = GameManager(level_jsons, seed=1, local=True)
		p1 = TestPlayer("kyle", moves=[(1,4), (1,4), (3,4), (3,2), (2,1), (2,3),
		(2,5), (2,6)])
		# Register player and place actors
		gm.register_player(p1)
		gm._place_actors()
		# Play 5 turns
		gm._play_turn()
		gm._play_turn()
		gm._play_turn()
		gm._play_turn()
		gm._play_turn()
		# Check that level was unlocked
		state = gm._current_level.build_state()
		self.assertEqual(state['exit-locked'], False)
		# Play three more turns
		gm._play_turn()
		gm._play_turn()
		gm._play_turn()
		# Check that player exited and level is over
		self.assertEqual(p1.is_exited(), True)
		self.assertEqual(gm._is_level_over(), True)
	
	def test_combat(self):
		"""
		Test the implementation of the combat system
		"""
		# Read levels, create game manager and test player
		level_jsons = parse_levels('resources/snarl1.levels')
		gm = GameManager(level_jsons, seed=1, local=True, combat=True)
		p1 = TestPlayer("kyle", moves=[(2,3), (2,2)])
		# Register player and place actors
		gm.register_player(p1)
		gm._place_actors()

		gm._play_turn()
		# Play another turn, injuring player
		gm._play_turn()
		state = gm._current_level.build_state()
		# Check that player did not move and their health decreased
		self.assertEqual(p1.get_health(), 40)
		self.assertEqual(p1.get_position(), (2, 2))
		self.assertEqual(state['adversaries'][0]['position'], (1, 2))
		
		# Play another turn, ejecting player
		gm._play_turn()
		state = gm._current_level.build_state()
		self.assertEqual(p1.is_ejected(), True)
		self.assertEqual(state['adversaries'][0]['position'], (2, 2))
	
	def test_start_level_low(self):
		"""
		Test starting a game at start level less than 1
		"""
		with self.assertRaises(Exception) as trial:
			GameManager([], 0)

		self.assertTrue("Invalid level start number." in str(trial.exception))
	
	def test_start_level_high(self):
		"""
		Test starting a game at start level greater than number of levels
		"""
		with self.assertRaises(Exception) as trial:
			GameManager([], 1)

		self.assertTrue("Invalid level start number." in str(trial.exception))
	
	def test_register_after_start(self):
		"""
		Test error raised if attempting to register a player after game began
		"""
		with self.assertRaises(Exception) as trial:
			# Generate game manager and two players
			level_jsons = parse_levels('resources/snarl1.levels')
			gm = GameManager(level_jsons, seed=1, local=True)
			p1 = TestPlayer("kyle", moves=[(2,3), (2,2)])
			p2 = TestPlayer("divo", moves=[(2,3), (2,2)])
			# Register one player and play game
			gm.register_player(p1)
			gm.play_game()
			# Attempt to register other player
			gm.register_player(p2)

		self.assertTrue('Cannot add player, game in progress' in str(trial.exception))
	
	def test_register_5_players(self):
		"""
		Test error raised if attempting to register more than 4 players
		"""
		with self.assertRaises(Exception) as trial:
			# Generate game manager and five players
			level_jsons = parse_levels('resources/snarl1.levels')
			gm = GameManager(level_jsons, seed=1, local=True)
			p1 = TestPlayer("kyle", moves=[(2,3), (2,2)])
			p2 = TestPlayer("divo", moves=[(2,3), (2,2)])
			p3 = TestPlayer("John", moves=[(2,3), (2,2)])
			p4 = TestPlayer("Evan", moves=[(2,3), (2,2)])
			p5 = TestPlayer("Bob", moves=[(2,3), (2,2)])
			# Register all players
			gm.register_player(p1)
			gm.register_player(p2)
			gm.register_player(p3)
			gm.register_player(p4)
			gm.register_player(p5)

		self.assertTrue('Cannot add player, 4 players registered' in str(trial.exception))

if __name__ == '__main__':
	unittest.main()