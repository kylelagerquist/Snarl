
import unittest

from src.Adversary.local_zombie import LocalZombie

class Test_LocalZombie(unittest.TestCase):
    def test_zombie_middle(self):
        """
        Test a zombies valid moves and response move given the current state
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
                {'type': 'zombie', 'name': '182436', 'position': (3, 4)},
                {'type': 'zombie', 'name': '774215', 'position': (1, 2)},  
                {'type': 'zombie', 'name': '251812', 'position': (1, 3)}], 
            'exit-locked': True
            }
        zombie = LocalZombie('182436')
        zombie.update_state(state)
        # Correct ghost position
        self.assertEqual(zombie.get_position(), (3, 4))
        # Ghost has 4 valid moves
        self.assertEqual(zombie._get_valid_moves(), [(4,4), (3,5),(2,4),(3,3)])
        # Ghost returns move closest to player in room
        self.assertEqual(zombie.request_move(), (3,3))
    
    def test_zombie_no_moves(self):
        """
        Test a zombies valid moves and response move given the current state
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
                {'type': 'zombie', 'name': '182436', 'position': (1, 1)},
                {'type': 'zombie', 'name': '774215', 'position': (1, 2)},  
                {'type': 'zombie', 'name': '251812', 'position': (2, 1)}], 
            'exit-locked': True
            }
        zombie = LocalZombie('182436')
        zombie.update_state(state)
        # Zombie has no valid moves, cornered by other adversaries
        self.assertEqual(zombie._get_valid_moves(), [])
        # Zombie stays put
        self.assertEqual(zombie.request_move(), (1,1))
    
    def test_zombie_methods(self):
        """
        Test methods implemented by the zombie
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
                {'type': 'zombie', 'name': '182436', 'position': (1, 1)},
                {'type': 'zombie', 'name': '774215', 'position': (1, 2)},  
                {'type': 'zombie', 'name': '251812', 'position': (2, 1)}], 
            'exit-locked': True
            }
        zombie = LocalZombie('182436')
        zombie.update_state(state)
        # Zombie type
        self.assertEqual(zombie.get_type(), "zombie")
        # Zombie name
        self.assertEqual(zombie.get_name(), "182436")
        # Zombie row
        self.assertEqual(zombie.get_row(), 1)
        # Zombie column
        self.assertEqual(zombie.get_col(), 1)
        # Zombie position
        self.assertEqual(zombie.get_position(), (1,1))
        # Zombie position JSON
        pos_json = {
			'type': "zombie", 
			'name': "182436",
			'position': (1,1)
		}
        self.assertEqual(zombie.get_position_JSON(), pos_json)
        # Zombie damage
        self.assertEqual(zombie.get_damage(), 60)
        # Update zombies position
        zombie.update_position(1,2)
        self.assertEqual(zombie.get_position(), (1,2))
    
    def test_update_state(self):
        """
        Test zombies state is successfully updated
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
                {'type': 'zombie', 'name': '182436', 'position': (1, 1)},
                {'type': 'zombie', 'name': '774215', 'position': (1, 2)},  
                {'type': 'zombie', 'name': '251812', 'position': (2, 1)}], 
            'exit-locked': True
            }
        zombie = LocalZombie('182436')
        # No position before state update
        self.assertEqual(zombie.get_position(), (None, None))
        # Update state
        zombie.update_state(state)
        # State was updated
        self.assertEqual(zombie.get_position(), (1, 1))
    

        
    


if __name__ == '__main__':
    unittest.main()