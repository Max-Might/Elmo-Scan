from serial import Serial, SerialException

class SerialPortDataSource:
	def __init__(self, params):
		self.port = Serial()
		self.port.port = params['port']
		self.port.baudrate = params['baudrate']

	def open(self):
		try:
			self.port.open()
			return True
		except SerialException as e:
			return str(e)
	
	def close(self):
	    self.port.close()
	
	def execute(self, command):
		self.port.write(command + '\r\n')
		res = ""
		c = ''
		while (c != '>'):
			res += c
			c = self.port.read(1)
		
		return res
