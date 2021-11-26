import json
import time
import sys 

from ..Common.abstract_adversary import AbstractAdversary
from ..Adversary.local_zombie import LocalZombie
from ..Adversary.local_ghost import LocalGhost 

class RemoteAdversary(AbstractAdversary):
	"""
	Data representation for a remote adversary in Snarl which is responsibile
	for facilitating sending/recieving messages from the remote adversary client

	Parameters
	----------
	sock : socket.SocketType
		Socket connection of remote adversary connection
	"""
	def __init__(self, sock):
		self._socket = sock
		super().__init__(name=None, adv_type=None, damage=None)

	def update_state(self, state_update: dict):
		"""
		Updates the adversary's knowledge of the game state
		"""
		self._send(json.dumps(state_update))
	
	def request_move(self):
		"""
		Requests a move from the adversary

		Returns
		-------
		(int, int)
			Row and column index to move to
		"""
		self._send(json.dumps("move"))
		move = self._receive()
		as_json = json.loads(move)
		return as_json['to']
	
	def declare_type(self, adversary_type):
		"""
		Changes the adversary type to Ghost or Zombie, declares damage, updates
		client with adversary type

		Parameters
		----------
		adversary_type : str
			Type of adversary to assume
		"""
		self._actor_type = adversary_type

		if adversary_type == "zombie":
			self._damage = LocalZombie().get_damage()
		elif adversary_type == "ghost":
			self._damage = LocalGhost().get_damage()
		else:
			raise ValueError(f"{adversary_type} is an invalid adversary type.")

		msg = json.dumps({
			"type": "declare-adversary", 
			"adversary-type": adversary_type,
			"name": self._name})
		self._send(msg)
	
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
		Sends the message to the connection

		Parameters
		----------
		msg : str
			Message to send to client
		"""
		# Attempt to send message to client, disconnect if client shut down
		try:
			self._socket.send(msg.encode())
		except ConnectionResetError:
			self.disconnect()
		
		time.sleep(1)
	
	def _receive(self):
		"""
		Recieve a message from the socket

		Returns
		----------
		str
			Message recieved from client
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