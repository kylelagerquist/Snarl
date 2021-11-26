import socket
import json
import sys
import threading
import os

from ..Game.game_manager import GameManager
from ..Player.remote_player import RemotePlayer
from ..Observer.local_observer import LocalObserver
from ..Adversary.remote_adversary import RemoteAdversary

class Server:
	"""
	Server responsible for accepting client connections and beginning game of Snarl

	Parameters
	----------
	host : str
		IP address to run server on
	port : int
		Port to accept clients on
	levels : List[dict]
		List of level JSON objects to use in game
	max_players : int, default 4
		Max number of players to allow in the game
	timeout : int, default 30
		Max number of seconds to wait in between client connections before starting
		game
	combat : bool, default False
		Whether to use the combat system, or have players immidiately ejected on
		adversary contact
	max_games : int, default 1
		Number of games to run
	remote_adversaries : bool, default False
		Whether to allow remote adversaries to join
	observe : bool, default False
		Whether to display all game updates on the server
	"""
	def __init__(self, host, port, levels, max_players=4, timeout=30, combat=False,
	max_games=1, remote_adversaries=False, observe=False):
		if max_players > 4:
			raise ValueError('Max players cannot exceed 4')
		
		self._max_players = max_players
		self._timeout = timeout
		self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self._connections = []
		self._levels = levels
		self._combat = combat
		self._max_games = max_games
		self._remote_adversaries = remote_adversaries
		self._observe = observe

		try:
			self._socket.bind((host, port))
		except OSError:
			print('Address already in use')
			sys.exit()
		
		# Initialize log file
		server_data = {"player_names": [], "player_scores": []}
		server_log_path = os.path.join(os.getcwd(), 'src/server_log.json')
		with open(server_log_path, 'w') as server_file:
			json.dump(server_data, server_file)
		
	def run(self):
		"""
		Run the server
		"""
		# Begin accepting client connections
		self._socket.listen()
		threads = []

		for _ in range(self._max_games):
			# Wait for initial player
			self._socket.settimeout(None)
			initial_player, adversaries = self._wait_for_players(1)

			# Wait for additional players
			self._socket.settimeout(self._timeout)

			try:
				more_players, more_adversaries = self._wait_for_players(self._max_players - 1)
			except socket.timeout:
				more_players = []
				more_adversaries = []
			
			players = initial_player + more_players
			adversaries = adversaries + more_adversaries

			# Start the game once all players have connected
			t = threading.Thread(target=self._new_game, args=(players, 
			adversaries, len(threads) + 1))

			threads.append(t)
			t.start()
		
		for x in threads:
			x.join()

		# Clost all connections at conclusion of all games
		for conn in self._connections:
			conn.close()
	
	def _wait_for_players(self, count):
		"""
		Waits for players and adversaries to connect

		Parameters
		----------
		count : int
			Max number of players to wait for to connect
		
		Returns
		-------
		List[AbstractPlayer], List[AbstractAdversary]
			Lists of players and adversaries that connected to server
		"""
		players = []
		adversaries = []

		# Wait for as many players in count 
		while len(players) < count:
			# Accept a new connection
			conn, addr = self._socket.accept()
			# Ask for connection to identify themselves
			conn.sendall(json.dumps("identify").encode())
			conn_type = json.loads(conn.recv(4096).decode())

			if conn_type == "player":
				# Create new user
				player = RemotePlayer(conn)
				# Store the player
				players.append(player)
				# Save the socket
				self._connections.append(conn)
			elif conn_type == "adversary" and self._remote_adversaries:
				# Create new remote adversary
				adversary = RemoteAdversary(conn)
				# Store the adversary
				adversaries.append(adversary)
				# Save the socket
				self._connections.append(conn)
			else:
				conn.close()

		return players, adversaries
	
	def _new_game(self, players, adversaries, game_id):
		"""
		Begin a new game of Snarl with the given players

		Parameters
		----------
		players : List[AbstractPlayer]
			Players to be registered to the game
		adversaries : List[AbstractAdversary]
			Adversaries to be registered to the game
		game_id : int
			ID number of the game
		"""
		manager = GameManager(self._levels, combat=self._combat, game_id=game_id)

		for player in players:
			manager.register_player(player)
		
		for adversary in adversaries:
			manager.register_adversary(adversary)
		
		if self._observe:
			manager.register_observer(LocalObserver())
		
		manager.play_game()

