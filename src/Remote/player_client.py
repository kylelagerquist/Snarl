import json
import socket
import sys

from ..Player.local_player import LocalPlayer

class PlayerClient:
	"""
	Client responsible for connecting to server, sending and recieving messages
	for remote player

	Parameters
	----------
	host : str
		IP address to connect to server at
	port : int
		Port to connect to server at
	"""
	def __init__(self, host, port):
		self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self._player = LocalPlayer()
		self._host = host
		self._port = port
	
	def run(self):
		"""
		Runs the client application responsible for sending/recieving messages
		"""
		# Attempt to connect to server and identify as player
		try:
			self._socket.connect((self._host, self._port))
		except ConnectionRefusedError:
			print("Unable to connect")
			sys.exit()
		# Continue to check for messages from server
		while True:
			data = self._receive()
			try:
				req = json.loads(data)
			except Exception as e:
				print(e)
				print(req)

			# Indentify request
			if req == 'identify':
				self._send(json.dumps("player"))
			# Name request
			elif req == 'name':
				name = self._player.get_name(first_time=True)
				self._send(json.dumps(name))
			# Welcome message
			elif self.is_server_welcome(req):
				print("Server Info: ", req['info'])
			# Level start
			elif self.is_start_level(req):
				print("Starting level: ", req['level'])
				print("Players in game: ", ', '.join(req['players']))
			# Player update
			elif self.is_player_update(req):
				if req['message'] is not None:
					print(req['message'])
				self._player.update_state(req)
			# Move request
			elif req == 'move':
				move_pos = self._player.request_move()
				self._send(json.dumps({ "type": "move", "to": move_pos}))
			# Move result, not damage
			elif req in ("OK", "Key", "Exit", "Eject", "Invalid"): 
				print("Move result: ", req)
			# End level message
			elif self.is_end_level(req):
				print("Level Ended")
				print("="*20)
				print("Key picked up by: ", req['key'])
				print("Players exited: ", ', '.join(req['exits']))
				print("Players ejected: ", ', '.join(req['ejects']))
			# End game message
			elif self.is_end_game(req):
				print("Game Ended")
				for player_score in req['scores']:
					print("Name: ", player_score['name'])
					print("Exits: ", player_score['exits'])
					print("Ejects: ", player_score['ejects'])
					print("Keys: ", player_score['keys'])
					print("="*20)
			# Server scores message
			elif self.is_server_scores(req):
				self.print_scores(req['scores'])
			# Move result for damage
			elif 'Damage' in req:
				print(f'Damage taken: {req.split("-")[-1]} HP')
			else:
				print("Invalid request:", req)
			
			print()
	
	@staticmethod
	def is_server_welcome(req):
		fields = (
			type(req) == dict and
			"type" in req and
			"info" in req and 
			req['type'] == "welcome"
		)
		return fields
	
	@staticmethod
	def is_start_level(req):
		fields = (
			type(req) == dict and
			"type" in req and
			"level" in req and
			"players" in req and
			req['type'] == "start-level"
		)
		return fields
	
	@staticmethod
	def is_player_update(req):
		fields = (
			type(req) == dict and
			"type" in req and
			"layout" in req and
			"position" in req and
			"objects" in req and
			"actors" in req and
			"message" in req and
			req['type'] == "player-update"
		)
		return fields
	
	@staticmethod
	def is_end_level(req):
		fields = (
			type(req) == dict and
			"type" in req and
			"key" in req and
			"exits" in req and
			"ejects" in req and
			req['type'] == "end-level"
		)
		return fields
	
	@staticmethod
	def is_end_game(req):
		fields = (
			type(req) == dict and
			"type" in req and
			"scores" in req and
			req['type'] == "end-game"
		)
		return fields
		
	@staticmethod
	def is_server_scores(req):
		fields = (
			type(req) == dict and
			"type" in req and
			"scores" in req and
			req['type'] == "server-scores"
		)
		return fields
	
	def print_scores(self, player_score_list):
		"""
		Prints the server leaderboard

		Parameters
		----------
		player_score_list : List[dict]
			List of player score objects from around the server
		"""

		# Sort the player scores by exits, ejects, and keys
		exits = sorted(player_score_list, key=lambda score: score['exits'])
		ejects = sorted(player_score_list, key=lambda score: score['ejects'], reverse=True)
		keys = sorted(player_score_list, key=lambda score: score['keys'])
		# Print all the rankings
		print("="*20)
		print("Snarl Server Exits Leaderboard:")
		for p in exits:
			print(f'{p["name"]} ({p["exits"]})')
		print("="*20)
		print("Snarl Server Ejects Leaderboard:")
		for p in ejects:
			print(f'{p["name"]} ({p["ejects"]})')
		print("="*20)
		print("Snarl Server Keys Leaderboard:")
		for p in keys:
			print(f'{p["name"]} ({p["keys"]})')

	def _send(self, msg):
		"""
		Send the given message to the server

		Parameters
		----------
		msg : str
			Message to send to server
		"""
		# Attempt to send message to server, disconnect if server shut down
		try:
			self._socket.sendall(msg.encode())
		except ConnectionResetError:
			self._disconnect()

	def _receive(self):
		"""
		Recieve data from the server

		Returns
		-------
		str
			Message recieved from the server
		"""
		# Attempt to recieve message, disconnect if server shut down
		try:
			data = self._socket.recv(4096)
		except ConnectionResetError:
			self._disconnect()
		# Server sent empty bytes, disconnect signal
		if not data:
			self._disconnect()
		response = data.decode()
		return response
	
	def _disconnect(self):
		"""
		Close the socket and program
		"""
		self._socket.close()
		sys.exit()
