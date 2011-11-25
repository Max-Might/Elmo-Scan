from ELMCommands import ELMCommands
from OBDParameters import OBDParameters

class ELMDevice:
	def __init__(self, adapter):
		self.adapter = adapter
		self.pidflags = ''
	
	def __configure(self):
		self.__getRaw(ELMCommands.HardReset)
		self.__getRaw(ELMCommands.EnableAdaptiveTiming)
		self.__getRaw(ELMCommands.DisableLineFeed)
		self.__getRaw(ELMCommands.DisableEcho)
		self.__getRaw(ELMCommands.DisableHeaders)
		self.__getRaw(ELMCommands.DisableSpaces)
	
	def open(self):
		result = self.adapter.open()
		if (result is True):
			self.__configure()
			return True
		
		return result
	
	def close(self):
		self.adapter.close()
	
	# TODO: remove when not needed
	def test(self):
		print self.getTroubleCodes()
	
	def getTroubleCodes(self):
		result = []
		output = self.__getRaw(OBDParameters.GetDiagnosticTrouleCodes)
		output = output.strip()
		
		if (output == 'NO DATA'):
			return result
		
		frames = output.split('\r')
		
		for frame in frames:
			codes = self.__extractTroubleCodes(frame)
			for code in codes:
				result.append(code)
		return result
	
	def __extractTroubleCodes(self, frame):
		rawCodes = []
		result = []
		if (frame[0:2] != '43'):
			raise BaseException('Expected mode 03 frame, received ' + frame)
		
		for i in [2, 6, 10]:
			code = frame[i : i + 4]
			if (code == '0000'):
				continue
			
			rawCodes.append(code)
		
		for code in rawCodes:
			result.append(self.__processRawTroubleCode(code))
		
		return result
	
	def __processRawTroubleCode(self, code):
		binaryCode = ''
		
		for i in range(0, 4):
			binaryCode += bin(int(code[i], 16))[2:].zfill(4)
		
		byteA = binaryCode[:8]
		byteB = binaryCode[8:]
		
		charTemplate = {
			'00' : 'P',
			'01' : 'C',
			'10' : 'B',
			'11' : 'U'
		}
		
		result = charTemplate[byteA[:2]]
		result += str(int(byteA[2:4], 2))
		result += str(int(byteA[4:], 2))
		result += str(int(byteB[:4], 2))
		result += str(int(byteB[4:], 2))
		
		return result
	
	def __getRaw(self, command):
		return self.adapter.execute(command)
	
	def __getBytes(self, command):
		if (len(command) < 4):
			raise BaseException("Minimum command lenght: 4")
		
		inMode = command[1:1]
		inPID = command[2:2]
		
		result = self.adapter.execute(command)
		result = result.strip('\r')
		
		if (result == 'NO DATA'):
			raise BaseException("No data for parameter: " + command)
		
		if (result == '?'):
			raise BaseException("Unknown command: " + command)

		if ((len(result) - 4) / 2 != OBDParameters.Descriptions[command]['bytes']):
			raise BaseException("Incorrect result length: " + str(len(result)))
		
		outMode = command[1:1]
		outPID = command[2:2]
		
		if (inMode != outMode):
			raise BaseException("Incorrect mode returned: %s, expected %s, buffer: %s" % (inMode, outMode, result))
		
		if (inPID != outPID):
			raise BaseException("Incorrect PID returned: %s, expected %s, buffer: %s" % (inMode, outMode, result))

		return result[4:]
	
	def isSupported(self, pid):
		if (not self.pidflags):
			result = self.__getBytes(OBDParameters.SupportedPIDs)
			for c in result:
				self.pidflags += bin(int(c, 16))[2:].zfill(4)
		
		return int(self.pidflags[OBDParameters.Descriptions[pid]['index']]) == 1
	
	def getDeviceInformation(self):
		return self.__getRaw(ELMCommands.GetDeviceInformation)
	
	def clearTroubleCodes(self):
		result = self.__getRaw(OBDParameters.ClearTroubleCodes)
		if (result.upper() == 'OK'):
			return True
		
		return False
	
	def getEngineLoad(self):
		result = self.__getBytes(OBDParameters.EngineLoad)
		return int(result, 16) * 100 / 255
	
	def getRPM(self):
		result = self.__getBytes(OBDParameters.RPM)
		a = int(result[0:2], 16)
		b = int(result[2:4], 16)
		return ((a * 256) + b) / 4
	
	def getThrottlePosition(self):
		result = self.__getBytes(OBDParameters.ThrottlePosition)
		return int(result, 16) * 100 / 255
	
	def getEngineTemperature(self):
		result = self.__getBytes(OBDParameters.EngineTemperature)
		return int(result, 16) - 40
	
	def getMAFAirFlow(self):
		result = self.__getBytes(OBDParameters.MAFAirFlow)
		a = int(result[0:2], 16)
		b = int(result[2:4], 16)
		return ((a * 256) + b) / 100
	
	def getVehicleSpeed(self):
		result = self.__getBytes(OBDParameters.VehicleSpeed)
		return int(result, 16)

