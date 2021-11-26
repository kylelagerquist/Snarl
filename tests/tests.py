import unittest
from src.Game.model.room import Room
from src.Game.model.tile import *
from src.Game.model.hallway import Hallway
from src.Game.model.level_generator import LevelGenerator
from src.Game.model.level import Level
from src.Game.game_manager import GameManager

class TestRoom(unittest.TestCase):
	def test_negative_x(self):
		with self.assertRaises(Exception) as trial:
			new_room = Room(-3, 4, ["000", "111", "000"])

		self.assertTrue("Origin row and column must be positive." in str(trial.exception))

	def test_negative_y(self):
		with self.assertRaises(Exception) as trial:
			new_room = Room(3, -4, ["000", "111", "000"])

		self.assertTrue("Origin row and column must be positive." in str(trial.exception))

	def test_non_rectangle(self):
		with self.assertRaises(Exception) as trial:
			new_room = Room(3, 4, ["000", "1111", "000"])

		self.assertTrue('Invalid room formation, not Rectangular.' in str(trial.exception))

	def test_invalid_tile(self):
		with self.assertRaises(Exception) as trial:
			new_room = Room(3, 4, ["000", "113", "000"])

		self.assertTrue('3 is not a valid tile character.' in str(trial.exception))

	def test_add_room_door_middle(self):
		with self.assertRaises(Exception) as trial:
			new_room = Room(0, 0, ["000", "111", "000"])
			new_room.add_room_door(1, 1)

		self.assertTrue('Cannot add room door to (1, 1), not on boundary.' in str(trial.exception))

	def test_add_room_door_valid(self):
		new_room = Room(0, 0, ["000", "111", "000"])
		new_room.add_room_door(2, 1)
		out = "000\n111\n020"

		self.assertEqual(new_room.__str__(), out)

	def test_is_on_boundary_outside(self):
		new_room = Room(0, 0, ["000", "111", "000"])
		self.assertEqual(new_room.is_on_boundary(5, 5), False)

	def test_is_on_boundary_inside(self):
		new_room = Room(0, 0, ["000", "111", "000"])
		self.assertEqual(new_room.is_on_boundary(1,1), False)

	def test_is_on_boundary_true(self):
		new_room = Room(0, 0, ["000", "111", "000"])
		self.assertEqual(new_room.is_on_boundary(2, 2), True)

	def test_is_on_boundary_true1(self):
		new_room = Room(4, 5, ["000", "111", "000"])
		self.assertEqual(new_room.is_on_boundary(6, 5), True)

	def test_get_height(self):
		new_room = Room(0, 0, ["000", "111", "000"])
		self.assertEqual(new_room.get_height(), 3)

	def test_get_width(self):
		new_room = Room(0, 0, ["0000", "1110", "0000"])
		self.assertEqual(new_room.get_width(), 4)

	def test_get_row(self):
		new_room = Room(3, 4, ["0000", "1110", "0000"])
		self.assertEqual(new_room.get_row(), 3)

	def test_get_col(self):
		new_room = Room(3, 4, ["0000", "1110", "0000"])
		self.assertEqual(new_room.get_col(), 4)

	def test_get_tiles(self):
		new_room = Room(0, 0, ["000", "012", "020"])
		tiles = [Wall(0,0), Wall(0,1), Wall(0,2), Wall(1,0), Space(1,1), Door(1,2), Wall(2,0),
			Door(2,1), Wall(2,2)]
		self.assertEqual(new_room.get_tiles(),tiles)

	def test_correct_build(self):
		new_room = Room(0, 0, ["000", "012", "121"])
		out = "000\n012\n121"
		self.assertEqual(new_room.__str__(), out)

	def test_sort(self):
		new_room1 = Room(0, 5, ["000", "012", "121"])
		new_room2 = Room(3, 3, ["000", "012", "121"])

		self.assertEqual(sorted([new_room1, new_room2]), [new_room2, new_room1])

	def test_sort1(self):
		new_room1 = Room(0, 5, ["000", "012", "020"])
		new_room2 = Room(5, 0, ["000", "012", "020"])

		self.assertEqual(sorted([new_room1, new_room2]), [new_room1, new_room2])


class TestHallway(unittest.TestCase):
	def test_same_start_end(self):
		with self.assertRaises(Exception) as trial:
			new_hallway = Hallway((3,4), (3,4))

		self.assertTrue("Hallway cannot start and stop on same tile." in str(trial.exception))

	def test_invalid_start_point(self):
		with self.assertRaises(Exception) as trial:
			new_hallway = Hallway((4,5,6), (3,4))

		self.assertTrue("(4, 5, 6) is an invalid coordinate." in str(trial.exception))

	def test_invalid_start_point1(self):
		with self.assertRaises(Exception) as trial:
			new_hallway = Hallway((4,-5), (3,4))

		self.assertTrue("(4, -5) is an invalid coordinate." in str(trial.exception))

	def test_invalid_end_point(self):
		with self.assertRaises(Exception) as trial:
			new_hallway = Hallway((4,5), (3,4, 5))

		self.assertTrue("(3, 4, 5) is an invalid coordinate." in str(trial.exception))

	def test_invalid_end_point1(self):
		with self.assertRaises(Exception) as trial:
			new_hallway = Hallway((4,5), (3,-4))

		self.assertTrue("(3, -4) is an invalid coordinate." in str(trial.exception))

	def test_invalid_waypoint(self):
		with self.assertRaises(Exception) as trial:
			new_hallway = Hallway((4,5), (3,4), [(1,2,3)])

		self.assertTrue("(1, 2, 3) is an invalid coordinate." in str(trial.exception))

	def test_invalid_waypoint1(self):
		with self.assertRaises(Exception) as trial:
			new_hallway = Hallway((4,5), (3,4), [(1,-2)])

		self.assertTrue("(1, -2) is an invalid coordinate." in str(trial.exception))

	def test_diagonal_hallway(self):
		with self.assertRaises(Exception) as trial:
			new_hallway = Hallway((3,4), (6,9))

		self.assertTrue("Hallway is not straight between (6, 9) and (3, 4)" in str(trial.exception))

	def test_diagonal_hallway2(self):
		with self.assertRaises(Exception) as trial:
			new_hallway = Hallway((3,4), (6,9), [(4,4), (5,5)])
		
		self.assertTrue("Hallway is not straight between (5, 5) and (4, 4)" in str(trial.exception))

	def test_staight_row(self):
		with self.assertRaises(Exception) as trial:
			new_hallway = Hallway((3, 4), (6, 4), [(5, 4)])

		self.assertTrue("Waypoint (5, 4) is not a corner." in str(trial.exception))

	def test_overlapping_hallway(self):
		with self.assertRaises(Exception) as trial:
			new_hallway = Hallway((3,4), (6,9), [(10,4), (10,2), (6,2)])

		self.assertTrue('Hallway overlaps with itself.' in str(trial.exception))

	def test_get_max_width(self):
		new_hallway = Hallway((3,4), (6,9), [(10,4), (10,9)])
		self.assertEqual(new_hallway.get_max_width(), 9)

	def test_get_max_height(self):
		new_hallway = Hallway((3,4), (6,9), [(10,4), (10,20), (6,20)])
		self.assertEqual(new_hallway.get_max_height(), 10)

	def test_get_start_pos(self):
		new_hallway = Hallway((3,4), (6,9), [(10,4), (10,20), (6,20)])
		self.assertEqual(new_hallway.get_start_pos(), (3,4))

	def test_get_end_pos(self):
		new_hallway = Hallway((3,4), (6,9), [(10,4), (10,20), (6,20)])
		self.assertEqual(new_hallway.get_end_pos(), (6, 9))

	def test_get_tiles(self):
		new_hallway = Hallway((3,4), (6,9), [(6,4)])
		out = [Space(4,4), Space(5,4), Space(6,4), Space(6,5), Space(6,6), Space(6,7),
		Space(6,8)]
		self.assertCountEqual(new_hallway.get_tiles(), out)

class TestMoves(unittest.TestCase):
	def test_invalid_player_name(self):
		r1 = Room(3, 1, ['0020', '0110', '0110', '0200'])
		r2 = Room(10, 5, ['00000', '01110', '21110', '01110', '00000'])
		r3 = Room(4, 14, ['00200', '01110', '01110', '01110', '00000'])
		h1 = Hallway((3,3), (4,16), [(1,3), (1,16)])
		h2 = Hallway((6,2), (12,5), [(12,2)])
		lev1_gen = LevelGenerator(rooms=[r1, r2, r3], hallways=[h1, h2])
		lev1 = Level(lev1_gen)
		lev1.add_key(4, 2)
		lev1.add_exit(7, 17)
		manager = GameManager([lev1])
		manager.add_player("p1", 7, 17)
		manager.add_adversary("a1", "zombie", 11, 6)
		out = manager.player_move('p2', (4, 2))
		self.assertEqual(out, '["Failure", "Player ", "p2", " is not a part of the game."]')

	def test_invalid_player_move(self):
		r1 = Room(3, 1, ['0020', '0110', '0110', '0200'])
		r2 = Room(10, 5, ['00000', '01110', '21110', '01110', '00000'])
		r3 = Room(4, 14, ['00200', '01110', '01110', '01110', '00000'])
		h1 = Hallway((3,3), (4,16), [(1,3), (1,16)])
		h2 = Hallway((6,2), (12,5), [(12,2)])
		lev1_gen = LevelGenerator(rooms=[r1, r2, r3], hallways=[h1, h2])
		lev1 = Level(lev1_gen)
		lev1.add_key(4, 2)
		lev1.add_exit(7, 17)
		manager = GameManager([lev1])
		manager.add_player("p1", 7, 17)
		manager.add_adversary("a1", "zombie", 11, 6)
		out = manager.player_move('p1', (4, 4))
		self.assertEqual(out, '["Failure", "The destination position ", [4, 4], " is invalid."]')




if __name__ == '__main__':
	unittest.main()
















