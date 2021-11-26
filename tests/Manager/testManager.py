from model.game_manager import GameManager
import json, sys

if __name__ == "__main__":
	# Parse input into JSON
	user_input = sys.stdin.read()
	user_input_json = json.loads(user_input)

	# Retrieve the items from the user input
	name_list = user_input_json[0]
	level_json = user_input_json[1]
	turns = user_input_json[2]
	initial_pos = user_input_json[3]
	actor_move_lists = user_input_json[4]

	# Build the game manager
	manager = GameManager([level_json])

	# Register players and adversaries
	for pos_ind in range(len(initial_pos)):
		pos = initial_pos[pos_ind]
		if pos_ind < len(name_list):
			manager.add_player(name_list[pos_ind], pos[0], pos[1])
		else:
			manager.add_adversary(f'adversary{pos_ind}', 'zombie', pos[0], pos[1])
	
	# Track the manager trace entries
	manager_trace = []

	# Record inital player updates
	updates = manager.issue_player_updates()
	for update in updates:
		manager_trace.append([update[0], update[1]])
	
	# Keep track of players move number
	player_move_num = dict(zip(name_list, [0] * len(name_list)))
	total_moves = 0
	previous_player_ind = -1
	move_performed = False
	
	while True:
		# Retrieve which player's turn it is and their respective moves
		player_up_ind = manager.get_current_turn_ind()
		player_up_name = name_list[player_up_ind]
		actor_moves = actor_move_lists[player_up_ind]

		# Full turn has not been completed
		if player_up_ind > previous_player_ind:
			previous_player_ind = player_up_ind
		# Same player is up after invalid move
		elif player_up_ind == previous_player_ind and not move_performed:
			previous_player_ind = player_up_ind
		# Back to the start of the order, turn has been completed
		else:
			total_moves += 1
			previous_player_ind = player_up_ind
			# If total turns exceeds max turns to perform, break out of loop
			if total_moves > turns:
				print('performed max turns')
				break

		# Break out of the loop if all their moves have been exhasuted
		if player_move_num[player_up_name] >= len(actor_moves):
			print(f'{player_up_name} out of turns')
			break
		else:
			actor_move = actor_moves[player_move_num[player_up_name]]
		
		
		# Retrieve the result of this players move
		move_result = manager.progress_game(player_up_name, actor_move['to'])

		# If it was an invalid move, continue with their next move
		if move_result in ('Nonexistent', 'Invalid'):
			move_performed = False
			player_move_num[player_up_name] += 1
			continue
		# If it was a valid move, record the result and issue player updates
		else:
			move_performed = True
			manager_trace.append([player_up_name, actor_move, move_result])
			player_move_num[player_up_name] += 1

			updates = manager.issue_player_updates()
			for update in updates:
				manager_trace.append([update[0], update[1]])
		
		# If the level is over after the valid player move, break out of the loop
		if manager.level_is_over():
			print('level is over')
			break
	
	as_json = json.dumps([manager.build_state(), manager_trace])
	print(as_json)



		

