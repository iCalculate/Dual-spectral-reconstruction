# -*- coding: utf-8 -*-
"""
Keithley 2400 SourceMeter comm. lib.
Du X.C., March 2023, Univ. of Electronic Science and Technology of China
Installed PyVISA for GPIB communication.
"""

import pyvisa
import time
import datetime
# from pymeasure.instruments.keithley import keithley2450
import numpy as np
# from time import sleep
# from matlplotlib import pyplot as plt 

class K34461A(object):
	def __init__(self, visa_name, timeout:int = 5000):
		rm = pyvisa.ResourceManager()
		self.pyvisa = rm.open_resource(visa_name)
		self.pyvisa.timeout = 5000 # Wait for instrument return value, default is infinite wait
		
		print(visa_name+' ->')
		print(self.pyvisa.query('*IDN?'))

	def close(self):
		try:
			self.pyvisa.close()
		except Exception:
			pass
	def read(self):
		return self.pyvisa.read()

	def write(self, string):
		self.pyvisa.write(string)

	def query(self, str):
		return self.pyvisa.query(str)
	
	def read_volt(self, dc:bool = True, vrange = 0.1, nplc = 1.0):
		if dc:
			self.write(f'CONFigure:VOLTage:DC {vrange},DEF')
			self.write(f'SENSe:VOLTage:DC:NPLC {nplc}')
		else:
			self.write(f'CONFigure:VOLTage:AC {vrange},DEF')
			self.write(f'SENSe:VOLTage:AC:NPLC {nplc}')
		return float(self.query('READ?'))
	
class K32500B(object):
	def __init__(self, visa_name, timeout:int = 5000):
		rm = pyvisa.ResourceManager()
		self.pyvisa = rm.open_resource(visa_name)
		self.pyvisa.timeout = 5000 # Wait for instrument return value, default is infinite wait
		
		print(visa_name+' ->')
		print(self.pyvisa.query('*IDN?'))
		
	def close(self):
		try:
			self.pyvisa.close()
		except Exception:
			pass
	def read(self):
		return self.pyvisa.read()

	def write(self, string):
		self.pyvisa.write(string)

	def query(self, str):
		return self.pyvisa.query(str)
	
	def set_waveform_square(self, freq:float=1e3,high:float=1.0,low:float=-1.0,duty:float=0.5):
		'''
		Parameters
		----------
		freq : float, optional
			DESCRIPTION. The default is 1e3.
		high : float, optional
			DESCRIPTION. The default is 1.0.
		low : float, optional
			DESCRIPTION. The default is -1.0.
		duty : float
			DESCRIPTION.
		'''
		self.write('FUNC SQU')
		self.write(f'FUNC:SQU:DCYC {duty*100}')
		self.write(f'FREQ {freq}')
		self.write(f'VOLT:HIGH {high}')
		self.write(f'VOLT:LOW {low}')
		
	def set_waveform_pulse(self, freq:float=20e3,volt:float=0.1,offset:float=0.05,width:float=2e-6,lead:float = 8.4e-9,trail:float = 8.4e-9):
		
		self.write(f'FUNC PULS')
		self.write(f'FUNCtion:PULSe:HOLD WIDTh')
		self.write(f'FUNCtion:PULSe:PERiod {1/freq}')
# 		self.write(f'VOLTage {volt}')
# 		self.write(f'VOLTage:OFFSet {offset}')
		self.write(f'FUNCtion:PULSe:WIDTh {width}')
		self.write(f'FUNCtion:PULSe:TRANsition:LEADing {lead}')
		self.write(f'FUNCtion:PULSe:TRANsition:TRAiling {trail}')
		
		
	def set_waveform_ramp(self, freq:float=10e3,volt:float=0.1,offset:float=0.05,sym:float=0.5):
		'''
		Parameters
		----------
		freq : float, optional
			DESCRIPTION. The default is 10e3.
		volt : float, optional
			DESCRIPTION. The default is 0.1.
		offset : float, optional
			DESCRIPTION. The default is 0.05.
		sym : float, optional
			DESCRIPTION. The default is 0.5.
		'''
		self.write('FUNC RAMP')
		self.write(f'FUNCtion:RAMP:SYMMetry {sym*100}')
		self.write(f'FREQ {freq}')
		self.write(f'VOLTage {volt}')
		self.write(f'VOLTage:OFFSet {offset}')
		
	def set_FM_carrier(self,freq:float=10.0,dev:float=5.0,func:str='RAMP',source:bool=True):
		'''
		Parameters
		----------
		freq : float, optional
			DESCRIPTION. The default is 10.0.
		dev : float, optional
			DESCRIPTION. The default is 5.0.
		func : str, optional
			DESCRIPTION. The default is 'RAMP'.
		source : bool, optional
			DESCRIPTION. The default is True.
		'''
		if source:
			self.write('FM:SOURce INT')
			self.write(f'FM:INTernal:FUNCtion {func}')
			self.write(f'FM:DEViation {dev}')
			self.write(f'FM:INTernal:FREQuency {freq}')
			
		else:
			self.write('FM:SOURce EXT')
		self.write('FM:STATe 1')

		
	def output(self, output:bool):
		if output:
			self.write('OUTP 1')
		else:
			self.write('OUTP 0')
	
	def set_display(self,state:bool):
		if state:
			self.write('DISP ON')
		else:
			self.write('DISP OFF')
		