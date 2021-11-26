import json
import socket
import sys

from ..Adversary.local_zombie import LocalZombie
from ..Adversary.local_ghost import LocalGhost

class AdversaryClient:
	"""
	Client responsible for connecting to server, sending and recieving messages
	for remote adversary

	Parameters
	----------
	host : str
		IP address to connect to server at
	port : int
		Port to connect to server at
	"""
	def __init__(self, host, port):
		self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self._adversary = None
		self._host = host
		self._port = port
	
	def run(self):
		"""
		Runs the client application responsible for sending/recieving messages
		"""
		# Attempt to connect to server and identify as adversary
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
				self._send(json.dumps("adversary"))
			# Declare adversary type
			elif self.is_declare_adversary(req):
				if req['adversary-type'] == 'zombie':
					self._adversary = LocalZombie(req['name'])
				elif req['adversary-type'] == 'ghost':
					self._adversary = LocalGhost(req['name'])
			# Move request
			elif req == 'move':
				move_pos = self._adversary.request_move()
				self._send(json.dumps({ "type": "move", "to": move_pos}))
			# State update
			elif self.is_state_update(req):
				self._adversary.update_state(req)
			else:
				pass
	
	@staticmethod
	def is_declare_adversary(req):
		fields = (
			type(req) == dict and
			"type" in req and
			"adversary-type" in req and
			"name" in req and
			req['type'] == "declare-adversary"
		)
		return fields
	
	@staticmethod
	def is_state_update(req):
		fields = (
			type(req) == dict and
			"type" in req and
			"level" in req and
			"players" in req and
			"adversaries" in req and
			"exit-locked" in req and
			req['type'] == "state"
		)
		return fields

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
		print('Server disconnected')
		self._socket.close()
		sys.exit()
