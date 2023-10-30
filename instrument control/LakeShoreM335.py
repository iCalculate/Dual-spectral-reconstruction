




import pyvisa








class Model335 (object):
	def __init__(self, visa_name, timeout:int = 5000):
		rm = pyvisa.ResourceManager()
		self.pyvisa = rm.open_resource(visa_name)
		self.pyvisa.timeout = 5000 # Wait for instrument return value, default is infinite wait
	
	
	def read(self):
		return self.pyvisa.read()

	def write(self, string):
		self.pyvisa.write(string)

	def query(self, str):
		return self.pyvisa.query(str)
	
	def set_temperature (self, output, temp):
		'''
		:param output: Specifies which output’s control loop to configure: 1 or 2 	
		:param temp: The value for the setpoint (in the preferred units of the 
control loop sensor).
		'''
		if (output == 1)  or (output == 2) and (0 <= temp <= 800) :
			self.write("SETP "+ str(output) + "," + str(temp) )
		else:
			print("Input is error")
		
	def set_heater_range(self , output, ranges):
		'''
		:param output: Specifies which output to configure: 1 or 2.
		:type output: str
		:param ranges: For Outputs 1 and 2 in Current mode: 0 = Off, 1 = Low, 
2 = Medium, 3 = High
		:type ranges: TYPE 	
		'''
		self.write("RANGE " + str(output) + "," + str(ranges))
		

	def read_temperature(self , mode:str):
		'''state = self.query("RDGST" + mode )
		if state == 1 :
			print("invalid reading")
		elif state == 16 :
			print("temp underrange")
		elif state == 32 :
			print("temp overrange")
		elif state == 64 :
			print("sensor units zero")
		elif state == 128 :
			print("sensor units overrange")	
		else:'''
		nowtemp = self.query("KRDG?" + mode)
		return nowtemp
		
	
