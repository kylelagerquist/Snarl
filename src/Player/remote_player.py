import socket
import json
import time
import sys

from ..Common.abstract_player import AbstractPlayer

class RemotePlayer(AbstractPlayer):
	"""
	Supports use of remote player player, where moves are requested via its socket

	Parameters
	----------
	sock : socket.SocketType
		Socket connection to the server
	"""
	def __init__(self, sock):
		self._socket = sock
		super().__init__(None)

	def get_name(self, first_time=False):
		"""
		If name has not been set, request a name from the client

		Returns
		-------
		str
			Name of player
		"""
		if first_time:
			self._send(json.dumps("name"))
			name = json.loads(self._receive())
			self._name = name
			
		return self._name
	
	def update_state(self, state: dict):
		"""
		Updates the players knowledge of the game state
		"""
		self._send(json.dumps(state))

	def request_move(self):
		"""
		Requests a move from the client

		Returns
		-------
		(int, int)
			row, column indices to move to
		"""
		self._send(json.dumps("move"))
		move = self._receive()
		as_json = json.loads(move)
		return as_json['to']
	
	def render_view(self):
		"""
		Render's the player's current knowledge of the state
		"""
		pass
	
	def send_message(self, msg):
		"""
		Sends the given message to the client

		Parameters
		----------
		msg : str
			Message to send to player
		"""
		self._send(msg)
	
	def _send(self, msg):
		"""
		Sends the message through the socket

		Parameters
		----------
		msg : str
			Message to send to player
		"""
		# Attempt to send message to client, disconnect if client shut down
		try:
			self._socket.send(msg.encode())
		except ConnectionResetError:
			self.disconnect()
		
		time.sleep(1)
	
	def _receive(self):
		"""
		Recieves a message through the socket

		Returns
		----------
		str
			Message recieved from socket
		"""
		# Attempt to recieve message, disconnect if client shut down
		try:
			data = self._socket.recv(4096)
		except ConnectionResetError:
			self.disconnect()
		# Server sent empty bytes, disconnect signal
		if not data:
			self.disconnect()
		response = data.decode()
		return response
	
	def disconnect(self):
		"""
		Close the actors socket, if remotely connected
		"""
		self._socket.close()
		sys.exit()
