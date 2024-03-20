# -*- coding: utf-8 -*-
"""
LakeShore Model335/336 comm. lib.
Du X.C., June 2023, Univ. of Electronic Science and Technology of China
Installed PyVISA for GPIB communication.
"""

import pyvisa
import time
import warnings
import datetime

import matplotlib.pyplot as plt # for python-style plottting

class Model335 (object):
	def __init__(self, visa_name, timeout:int = 5000):
		rm = pyvisa.ResourceManager()
		self.pyvisa = rm.open_resource(visa_name)
		self.pyvisa.timeout = 5000 # Wait for instrument return value, default is infinite wait
		print(visa_name+' ->')
		print(self.pyvisa.query("*IDN?"))
	
	
	def read(self):
		return self.pyvisa.read()

	def write(self, string):
		self.pyvisa.write(string)

	def query(self, str):
		return self.pyvisa.query(str)
    
	def close(self):
		return self.pyvisa.close()
	
	def set_temperature (self, channel, temp:float):
		'''
		:param output: Specifies which output’s control loop to configure: 1 or 2 	
		:param temp: The value for the setpoint (in the preferred units of the 
control loop sensor).
		'''
		if (channel == 1)  or (channel == 2) and (0 <= temp <= 800) :
			self.write("SETP "+ str(channel) + "," + str(temp) )
		else:
			print("Input is error")
		
	def set_heater_range(self, channel, ranges):
		'''
		:param output: Specifies which output to configure: 1 or 2.
		:type output: str
		:param ranges: For Outputs 1 and 2 in Current mode: 0 = Off, 1 = Low, 
2 = Medium, 3 = High
		:type ranges: TYPE 	
		'''
		self.write("RANGE " + str(channel) + "," + str(ranges))
		
	def set_ramp_state(self, channel, state:bool, rate:float = 10.0, query:bool = False):
		'''
		
		:param channel: Specifies which output’s control loop to configure: 1 or 2.
		:param state: Specifies whether ramping is 0 = Off or 1 = On.
		:param rate:  Specifies setpoint ramp rate in kelvin per minute from 0.1 to
		 100. The rate is always positive, but will respond to ramps up or down. A 
		 rate of 0 is interpreted as infinite, and will therefore respond as if 
		 setpoint ramping were off., defaults to 10.0
		:param query: True for query, defaults to False
		:type query: bool, optional
		:return: Ramp Parameter <off/on>,<rate value>[term] n,nnnn (refer to command for description

		'''
		if query:
			return self.query("RAMP?")
		else:
			self.write("RAMP "+str(channel)+","+str(int(state))+","+str(rate))
			# self.write(f'RAMP {channel},{int(state)},{rate}')
			
	def read_ramp_state(self, channel):
		'''
		
		:param channel: Specifies which output’s control loop to query: 1 or 2
		:return: <ramp status>[term] <ramp status> 0 = Not ramping, 1 = Setpoint is ramping.

		'''
		return bool(int(self.query("RAMPST?")))
		
		
	def read_heater_value(self, channel):
		value = self.query("HTR? "+str(channel))
		return float(value)/100
		
	def read_temperature(self , channel):
		'''
		:param channel: channel index
		:type channel: int from 1-4
		:return: KRDG? query the real-time temperature
		:rtype: ASCII
		'''
		state = int(self.query("RDGST? " + str(channel) ))
		nowtemp = -1
		if state & 0x01 :
			print("Temperature Query Error: invalid reading!")
			warnings.warn('Temperature Query Error: invalid reading!', DeprecationWarning)
		elif state & 0x10 :
			print("Temperature Query Error: temp underrange!")
		elif state & 0x20 :
			print("Temperature Query Error: temp overrange!")
		elif state & 0x40 :
			print("Temperature Query Error: sensor units zero!")
		elif state & 0x80 :
			print("Temperature Query Error: sensor units overrange!")	
		else:
			nowtemp = self.query("KRDG? " + str(channel))
		return float(nowtemp)
	
	def set_temp_stable(self, channel, aim:float, length = 200, threshold = 1e-4, tsample = 0.1, realtime = True):
		'''
		:param channel: select the operation channel from 1-4
		:param aim: float aim temperature unit K
		:param length: the temperature history FIFO queue length, defaults to 10
		:param threshold: the quadratic sum threshold of FIFO queue , defaults to 1e-3
		:param tsample: sample interval time, defaults to 1
		'''
		self.set_temperature(channel, aim)
		fifo = []
		heater = []
		loop = 0
		if realtime:
			plt.ion()
		for i in range(length):
			if realtime:
				plt.clf()
				plt.plot(fifo, '*-')
				plt.xlabel("FIFO index")
				plt.ylabel("delta Temp (K)")
				plt.pause(0.01)
			fifo.insert(0,float(self.read_temperature(channel))-aim)
			heater.insert(0,self.read_heater_value(channel))
			string = f'\rWaiting for temperature stable... T_now = {fifo[0]:.3f} K'
			print(string.replace('.', '·',i%4) ,end="")
			time.sleep(tsample)
			if realtime:
				plt.ioff()
		while sum(i*i/length for i in fifo) >= threshold:
			if realtime:
				plt.clf()
				plt.plot(fifo, '*-')
				plt.xlabel("FIFO index")
				plt.ylabel("delta Temp (K)")
				plt.pause(0.01)
			fifo.insert(0,float(self.read_temperature(channel))-aim)
			heater.insert(0,self.read_heater_value(channel))
			fifo.pop()
			string = f'\rWaiting for temperature stable... T_now = {fifo[0]:.3f} K'
			print(string.replace('.', '·',loop%4) ,end="")
			time.sleep(tsample)
			loop += 1
			if realtime:
				plt.ioff()
		nowtime = datetime.datetime.now().strftime('%H:%M:%S')
		print(' --> Finished!')
		print(f'[{nowtime}] --> Temperature stable at {aim} K')
		pass
	
	
	
	
	
	
	
	
	
	