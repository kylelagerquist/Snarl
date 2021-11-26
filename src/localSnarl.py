import argparse
import json
from Player.local_user import LocalUser
from Observer.local_observer import LocalObserver
from Game.model.game_manager import GameManager
from Game.model.game_manager import InteractionHandler

def parse_levels(file_name):
	jsons = []
	json_strs = []

	with open(file_name) as f:
		for line in f:
			if line != '\n':
				json_strs.append(line.strip())
			else:
				as_json = json.loads(' '.join(json_strs))
				jsons.append(as_json)
				json_strs = []

	return jsons


if __name__ == '__main__':
	# Create the command line parser
	parser = argparse.ArgumentParser(allow_abbrev=False)
	parser.add_argument("--levels", type=str,
						help="File containing JSON level specs", default='snarl.levels')
	parser.add_argument("--players", type=int, help="Number of players",
						choices=[1, 2, 3, 4], default=1)
	parser.add_argument("--start", type=int,
						help="Level to start from", default=1)
	parser.add_argument("--observe", action='store_true',
											help="Whether to show observer view (full level)")
	args = parser.parse_args()

	# Parse all of the level JSONs
	all_jsons = parse_levels(args.levels)

	num_levels = all_jsons[0]
	levels = all_jsons[1:]

	# Generate the game manager and interaction handler
	manager = GameManager(levels, start_level_num=args.start)


	# If the user wishes to observe, register observer and set players to 1 
	if args.observe:
		args.players = 1
		observer = LocalObserver()
		manager.register_observer(observer)

	# Add all of the players
	for player_num in range(args.players):
		while True:
			new_player = LocalUser()
			add_result = manager.add_player(new_player)
			if add_result:
				break
	
	# Start the game
	manager.play_game()


