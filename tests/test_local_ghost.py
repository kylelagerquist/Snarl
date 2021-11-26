
import unittest

from src.Adversary.local_ghost import LocalGhost

class Test_LocalGhost(unittest.TestCase):
    def test_ghost_middle(self):
        """
        Test a ghosts valid moves and response move given the current state
        """
        state = {
            'type': 'state', 
            'level': {
                'type': 'level', 
                'rooms': [
                    {'type': 'room', 
                    'origin': [0, 0], 
                    'bounds': {'rows': 6, 'columns': 8}, 
                    'layout': [
                        [0, 0, 0, 0, 0, 0, 0, 0], 
                        [0, 1, 1, 1, 1, 1, 1, 0], 
                        [0, 1, 1, 1, 1, 1, 1, 0], 
                        [0, 1, 1, 1, 1, 1, 1, 0], 
                        [0, 1, 1, 1, 1, 1, 1, 0], 
                        [0, 0, 0, 0, 0, 0, 0, 0]]}], 
                'hallways': [], 
                'objects': [
                    {'type': 'key', 'position': (2, 1)}, 
                    {'type': 'exit', 'position': (2, 6)}]}, 
            'players': [{'type': 'player', 'name': 'k', 'position': (1, 1)}], 
            'adversaries': [
                {'type': 'ghost', 'name': '182436', 'position': (3, 4)},
                {'type': 'zombie', 'name': '774215', 'position': (1, 2)},  
                {'type': 'zombie', 'name': '251812', 'position': (1, 3)}], 
            'exit-locked': True
            }
        ghost = LocalGhost('182436')
        ghost.update_state(state)
        # Correct ghost position
        self.assertEqual(ghost.get_position(), (3, 4))
        # Ghost has 4 valid moves
        self.assertEqual(ghost._get_valid_moves(), [(4,4), (3,5),(2,4),(3,3)])
        # Ghost returns move closest to player in room
        self.assertEqual(ghost.request_move(), (3,3))
    
    def test_ghost_cornered(self):
        """
        Test a ghosts valid moves and response move given the current state
        """
        state = {
            'type': 'state', 
            'level': {
                'type': 'level', 
                'rooms': [
                    {'type': 'room', 
                    'origin': [0, 0], 
                    'bounds': {'rows': 6, 'columns': 8}, 
                    'layout': [
                        [0, 0, 0, 0, 0, 0, 0, 0], 
                        [0, 1, 1, 1, 1, 1, 1, 0], 
                        [0, 1, 1, 1, 1, 1, 1, 0], 
                        [0, 1, 1, 1, 1, 1, 1, 0], 
                        [0, 1, 1, 1, 1, 1, 1, 0], 
                        [0, 0, 0, 0, 0, 0, 0, 0]]}], 
                'hallways': [], 
                'objects': [
                    {'type': 'key', 'position': (2, 1)}, 
                    {'type': 'exit', 'position': (2, 6)}]}, 
            'players': [{'type': 'player', 'name': 'k', 'position': (3, 1)}], 
            'adversaries': [
                {'type': 'ghost', 'name': '182436', 'position': (1, 1)},
                {'type': 'zombie', 'name': '774215', 'position': (1, 2)},  
                {'type': 'zombie', 'name': '251812', 'position': (2, 1)}], 
            'exit-locked': True
            }
        ghost = LocalGhost('182436')
        ghost.update_state(state)
        # Ghost has two valid moves at walls, cornered by other adversaries
        self.assertEqual(ghost._get_valid_moves(), [(0,1), (1,0)])
        # Ghost moves to wall to teleport
        self.assertEqual(ghost.request_move(), (0,1))
    
    def test_ghost_no_moves(self):
        """
        Test a ghost stays put when no valid moves
        """
        state = {
            'type': 'state', 
            'level': {
                'type': 'level', 
                'rooms': [
                    {'type': 'room', 
                    'origin': [0, 0], 
                    'bounds': {'rows': 6, 'columns': 8}, 
                    'layout': [
                        [0, 0, 0, 0, 0, 0, 0, 0], 
                        [0, 1, 1, 1, 1, 1, 1, 0], 
                        [0, 1, 1, 1, 1, 1, 1, 0], 
                        [0, 1, 1, 1, 1, 1, 1, 0], 
                        [0, 1, 1, 1, 1, 1, 1, 0], 
                        [0, 0, 0, 0, 0, 0, 0, 0]]}], 
                'hallways': [], 
                'objects': [
                    {'type': 'key', 'position': (2, 1)}, 
                    {'type': 'exit', 'position': (2, 6)}]}, 
            'players': [{'type': 'player', 'name': 'k', 'position': (1, 1)}], 
            'adversaries': [
                {'type': 'ghost', 'name': '182436', 'position': (3, 4)},
                {'type': 'zombie', 'name': '774215', 'position': (3, 3)},
                {'type': 'zombie', 'name': '774215', 'position': (2, 4)},
                {'type': 'zombie', 'name': '774215', 'position': (4, 4)},  
                {'type': 'zombie', 'name': '251812', 'position': (3, 5)}], 
            'exit-locked': True
            }
        ghost = LocalGhost('182436')
        ghost.update_state(state)
        # Ghost has no valid moves
        self.assertEqual(ghost._get_valid_moves(), [])
        # Ghost stays at same space
        self.assertEqual(ghost.request_move(), (3,4))
    
    def test_ghost_teleport(self):
        """
        Test a ghost moves to wall tile when no player in room
        """
        state = {
            'type': 'state', 
            'level': {
                'type': 'level', 
                'rooms': [
                    {'type': 'room', 
                    'origin': [0, 0], 
                    'bounds': {'rows': 6, 'columns': 8}, 
                    'layout': [
                        [0, 0, 0, 0, 0, 0, 0, 0], 
                        [0, 1, 1, 1, 1, 1, 1, 0], 
                        [0, 1, 1, 1, 1, 1, 1, 0], 
                        [0, 1, 1, 1, 1, 1, 1, 0], 
                        [0, 1, 1, 1, 1, 1, 1, 0], 
                        [0, 0, 0, 0, 0, 0, 0, 0]]},
                    {'type': 'room', 
                    'origin': [10, 0], 
                    'bounds': {'rows': 6, 'columns': 8}, 
                    'layout': [
                        [0, 0, 0, 0, 0, 0, 0, 0], 
                        [0, 1, 1, 1, 1, 1, 1, 0], 
                        [0, 1, 1, 1, 1, 1, 1, 0], 
                        [0, 1, 1, 1, 1, 1, 1, 0], 
                        [0, 1, 1, 1, 1, 1, 1, 0], 
                        [0, 0, 0, 0, 0, 0, 0, 0]]}], 
                'hallways': [], 
                'objects': [
                    {'type': 'key', 'position': (2, 1)}, 
                    {'type': 'exit', 'position': (2, 6)}]}, 
            'players': [{'type': 'player', 'name': 'k', 'position': (1, 1)}], 
            'adversaries': [
                {'type': 'ghost', 'name': '182436', 'position': (11, 1)}], 
            'exit-locked': True
            }
        ghost = LocalGhost('182436')
        ghost.update_state(state)
        # Ghost has four valid moves
        self.assertEqual(ghost._get_valid_moves(), [(12,1), (11,2), (10,1), (11,0)])
        # Ghost moves to wall space to be able to teleport
        self.assertEqual(ghost.request_move(), (10,1))
    
    def test_ghost_methods(self):
        """
        Test methods implemented by the ghost
        """
        state = {
            'type': 'state', 
            'level': {
                'type': 'level', 
                'rooms': [
                    {'type': 'room', 
                    'origin': [0, 0], 
                    'bounds': {'rows': 6, 'columns': 8}, 
                    'layout': [
                        [0, 0, 0, 0, 0, 0, 0, 0], 
                        [0, 1, 1, 1, 1, 1, 1, 0], 
                        [0, 1, 1, 1, 1, 1, 1, 0], 
                        [0, 1, 1, 1, 1, 1, 1, 0], 
                        [0, 1, 1, 1, 1, 1, 1, 0], 
                        [0, 0, 0, 0, 0, 0, 0, 0]]}], 
                'hallways': [], 
                'objects': [
                    {'type': 'key', 'position': (2, 1)}, 
                    {'type': 'exit', 'position': (2, 6)}]}, 
            'players': [{'type': 'player', 'name': 'k', 'position': (3, 1)}], 
            'adversaries': [
                {'type': 'ghost', 'name': '182436', 'position': (1, 1)},
                {'type': 'zombie', 'name': '774215', 'position': (1, 2)},  
                {'type': 'zombie', 'name': '251812', 'position': (2, 1)}], 
            'exit-locked': True
            }
        ghost = LocalGhost('182436')
        ghost.update_state(state)
        # Ghost type
        self.assertEqual(ghost.get_type(), "ghost")
        # Ghost name
        self.assertEqual(ghost.get_name(), "182436")
        # Ghost row
        self.assertEqual(ghost.get_row(), 1)
        # Ghost column
        self.assertEqual(ghost.get_col(), 1)
        # Ghost position
        self.assertEqual(ghost.get_position(), (1,1))
        # Ghost position JSON
        pos_json = {
			'type': "ghost", 
			'name': "182436",
			'position': (1,1)
		}
        self.assertEqual(ghost.get_position_JSON(), pos_json)
        # Ghost damage
        self.assertEqual(ghost.get_damage(), 40)
        # Update ghost position
        ghost.update_position(1,2)
        self.assertEqual(ghost.get_position(), (1,2))
    
    def test_update_state(self):
        """
        Test ghost state is successfully updated
        """
        state = {
            'type': 'state', 
            'level': {
                'type': 'level', 
                'rooms': [
                    {'type': 'room', 
                    'origin': [0, 0], 
                    'bounds': {'rows': 6, 'columns': 8}, 
                    'layout': [
                        [0, 0, 0, 0, 0, 0, 0, 0], 
                        [0, 1, 1, 1, 1, 1, 1, 0], 
                        [0, 1, 1, 1, 1, 1, 1, 0], 
                        [0, 1, 1, 1, 1, 1, 1, 0], 
                        [0, 1, 1, 1, 1, 1, 1, 0], 
                        [0, 0, 0, 0, 0, 0, 0, 0]]}], 
                'hallways': [], 
                'objects': [
                    {'type': 'key', 'position': (2, 1)}, 
                    {'type': 'exit', 'position': (2, 6)}]}, 
            'players': [{'type': 'player', 'name': 'k', 'position': (3, 1)}], 
            'adversaries': [
                {'type': 'ghost', 'name': '182436', 'position': (1, 1)},
                {'type': 'zombie', 'name': '774215', 'position': (1, 2)},  
                {'type': 'zombie', 'name': '251812', 'position': (2, 1)}], 
            'exit-locked': True
            }
        ghost = LocalGhost('182436')
        # No position before state update
        self.assertEqual(ghost.get_position(), (None, None))
        # Update state
        ghost.update_state(state)
        # State was updated
        self.assertEqual(ghost.get_position(), (1, 1))

if __name__ == '__main__':
    unittest.main()