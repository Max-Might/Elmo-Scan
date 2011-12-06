from time import sleep
from bluetooth import *

class BluetoothDataSource:
	def __init__(self, params):
		self.params = params
		self.socket = BluetoothSocket(RFCOMM)
	
	def search(self):
		return discover_devices(lookup_names = True)

	def open(self):
		try:
			self.socket.connect((self.params['device'], self.params['port']))
			sleep(0.4)
			return True
		except BluetoothError as e:
			return str(e)
	
	def close(self):
		self.socket.close()
	
	def execute(self, command):
		self.socket.send(command + '\r\n')
		res = ''
		c = ''
		
		while (c != '>'):
			res += c
			c = self.socket.recv(1)
		
		return res
