import os
import sys
import time

from ELMDevice import ELMDevice
from DataSources.SerialPortDataSource import SerialPortDataSource

def main():
	port = SerialPortDataSource({'port' : '/dev/pts/1', 'baudrate' : '38400'})
	source = ELMDevice(port)
	
	result = source.open()
	if result is not True:
		sys.stderr.write("ERROR: %s%s" % (result, os.linesep))
		return
	
	print "Device: " + source.getDeviceInformation()
	
	source.test()
	#for i in range(20):
	#	print source.getVehicleSpeed()
	#	time.sleep(0.2)
	
	source.close()

if __name__ == '__main__':
	main()
