# -*- coding: utf-8 -*-
"""
Stanford Research 400 Photon Counter comm. lib.
Du X.C., March 2023, Univ. of Electronic Science and Technology of China
Installed PyVISA for GPIB communication.
"""

import pyvisa
# import munpy as np
# from time import sleep
# from matlplotlib import pyplot as plt 

class sr400(object):
	def __init__(self, visa_name, timeout:int = 5000):
		rm = pyvisa.ResourceManager()
		self.pyvisa = rm.open_resource(visa_name)
		self.pyvisa.timeout = 5000 # Wait for instrument return value, default is infinite wait
	
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
	
	def sim_button(self, botton = 'STOP'):
		keydict = {'DOWN': 0, 'RIGHT': 1, 'LEVEL': 2, 'SETUP': 3,\
					'COM': 4, 'STOP': 5, 'LOCAL': 6, 'RESET': 7,\
					'LEFT': 8, 'UP': 9, 'MODE': 10, 'AGATE': 11,\
					'BGATE': 12, 'START': 13}
		self.write('CK ' + str(keydict[botton]))
		
	def cursor(self):
		cursordict = {'0\r\n': 'LEFT', '1\r\n': 'RIGHT', '2\r\n': 'INACTIVE'}
		return cursordict[self.query('SC')]
	
	def read_last_count(self, channel = 'ch1') -> int:
		if channel == 'ch1':
			count = int(self.query('QA'))
		elif channel == 'ch2':
			count = int(self.query('QB'))
		return count
	
	def read_count_now(self, channel = 'ch1') -> int:
		if channel == 'ch1':
			count = int(self.query('XA'))
		elif channel == 'ch2':
			count = int(self.query('XB'))
		return count
	
	def read_buffer_count(self, channel = 'ch1', bit = 1) -> int:
		if channel == 'ch1':
			count = int(self.query('QA ' + str(bit)))
		elif channel == 'ch2':
			count = int(self.query('QB ' + str(bit)))
		return count

	def check_ready(self):
		return bool(int(self.query('SS 1')))
	
	def check_para_change(self):
		'''
		Parameter Changed from front panel. When this 
		bit is set, it indicates that the front panel knob has 
		been rotated and a setting has been altered
		'''
		return bool(int(self.query('SS 0')))
	
	def check_count_finish(self):
		return bool(int(self.query('SS 1')))

	def check_scan_finish(self):
		return bool(int(self.query('SS 2')))
	
	def check_overrun(self):
		return bool(int(self.query('SS 3')))
	
	def check_gate_err(self):
		'''
		This bit is set whenever a gate is 
		missed. This can occur if a gate delay or width 
		exceeds the trigger period minus 1 µs
		'''
		return bool(int(self.query('SS 4')))

	def check_recall_err(self):
		'''
		 This bit is set if a recall from a stored 
		 setting detects an error in the recalled data. If an 
		 error is found, the instrument setup is not altered.
		'''
		return bool(int(self.query('SS 5')))

	def check_SRQ(self):
		return bool(int(self.query('SS 6')))
	
	def check_triggered(self):
		return bool(int(self.query('SI 0')))
	
	def check_inhibited(self):
		return bool(int(self.query('SI 1')))
	
	def check_counting(self):
		return bool(int(self.query('SI 2')))
	
	def check_command_err(self):
		'''
		This bit is set when an illegal command is received.
		'''
		return bool(int(self.query('SS 7')))

	def count_restart(self):
		self.write('CR') # CR command resets the counters
		self.write('CS') # CS command same as START key

	def count_reset(self):
		self.write('CR') # CR command resets the counters

	def count_stop(self):
		self.write('CH') # same effect as pressing the STOP key
		
	def count_start(self):
		self.write('CS') # same effect as pressing the START key
	
	
	def gate_delay(self, channel = 'A') -> float:
		delay = float(self.query('GZ ' + ('0' if channel == 'A' else '1')))
		return delay
	
	def gate_delay_set(self, channel = 'A', delay:float = 0.0):
		'''
		:param channel: select gate 'A' or 'B', defaults to 'A'
		:param delay: the selected gate delay is set to t seconds where 0 <= t <= 999.2E-3, defaults to 0.0
		:type delay: float, optional
		'''
		if 0 <= delay <= 999.2E-3:
			self.write('GD ' + ('0,' if channel == 'A' else '1,') + '%G' %delay)
		else:
			print('delay in range  0 <= t <= 999.2E-3.')
		
	def gate_mode(self, channel = 'A', mode = 'CW',query:bool = False):
		'''
		:param channel: DESCRIPTION, defaults to 'A'
		:param mode: If it is changed to SCAN, the delay begins scanning from the start position on the next count period. If it is changed to FIXED, the delay returns to the start position immediately, defaults to 'CW'
		:param query: True for asking, defaults to False for setting
		'''
		gate_mode_dict = {'CW':0, 'FIXED':1, 'SCAN': 2}
		if query:
			return self.query('GM '+ ('0' if channel == 'A' else '1'))
		else:
			try:
				self.write('GM '+ ('0,' if channel == 'A' else '1,') + str(gate_mode_dict[mode]))
			except:
				print('Illegal Keyword!')
		
	def gate_scan_step(self, channel = 'A', step:float = 0.0, query:bool = False):
		if query:
			return self.query('GY '+ ('0' if channel == 'A' else '1'))
		elif 0 <= step <= 999.2E-3:
			self.write('GY ' + ('0,' if channel == 'A' else '1,') + '%G' %step)
		else:
			print('step in range  0 <= t <= 99.92E-3.')
	
	def gate_window(self, channel = 'A', window:float = 0.0, query:bool = False):
		if query:
			return self.query('GW '+ ('0' if channel == 'A' else '1'))
		elif 0.005E-6 <= window <= 999.2E-3:
			self.write('GW ' + ('0,' if channel == 'A' else '1,') + '%G' %window)
		else:
			print('window in range 0.005E-6 <= t <= 999.2E-3.')
	
	def lcd_message(self, message, clear = False):
		if clear:
			self.write('MS')
		else:
			if len(message) <= 24: self.write('MS '+ message)
	
	def display_mode(self, conti:bool = True):
		self.write('SD ' + ('0' if conti else '1'))
	
	def scan_periods(self, num:int = 0):
		'''
		:param num: the number of periods is set to the value num.Changing the 
number of periods during a scan is allowed, defaults to 0
		:type num: int, optional
		'''
		if 1<= num <= 2000:
			self.write('NP ' + str(num))
		else:
			return int(self.query('NP'))
	def scan_position(self):
		return self.query('NN')
	
	def scan_end_mode(self, mode = 'STOP', query:bool = False):
		if query:
			status = bool(int(self.query('NE')))
			return ('STOP' if status else 'START')
		else:
			self.write('NE ' + ('0' if mode=='STOP' else '1'))
	
	def count_reset_all(self):
		'''
		NOTE: it is bad practice to use the CL command before all previous 
		commands have been processed and all responses have been received
		'''
		self.write('CL') 
		
	def count_mode(self, mode = 'query'):
		if mode == 'query':
			return self.query('CM')
		elif mode == 'independent':
			self.write('CM 0')
		elif mode == 'difference':
			self.write('CM 1')
		elif mode == 'sum':
			self.write('CM 2')
		elif mode == 'mutual':
			self.write('CM 3')
		else:
			print('setting count mode failed: Incorrect keywords')

	def dwell_time(self, dwell = -1.0):
		'''
		:param dwell: 0 for EXTERNAL dwell, internal dwell in range [2e-3,6e1]
		'''
		if dwell == 0:
			self.write('DT 0')
		if (dwell >= 6e1) or (dwell <= 2e-3):
			return self.query('DT')
		else:
			self.write('DT %g' %dwell)

	def set_disc_mode(self, channel = -1, fixed = True):
		'''
		:param channel: select A(0),B(1),T(2) channel, -1 for query
		:param fixed: True for FIXED, False for SCAN
		'''
		if channel is -1:
			return [self.query('DM 0'), self.query('DM 1'), self.query('DM 2')]
		else:
			self.write('DM '+ str(channel) + (',0' if fixed else ',1'))

	def set_disc_level(self, channel = 'ch1', level = 0.0, slope:bool = True):
		"""
		:param channel: target channel, allowed string 'ch1', 'ch2', 'trigger'
		:param level: gate trigger level, level in [-2.000, 2.000] Resolution is .001 V.
		:param slope: gate trigger slope. True for RISE or positive, False for FALL or negative
		"""
		if channel == 'trigger':
			self.write('TS ' + ('0' if slope else '1'))
			self.write('TL ' + str(level))
		else:
			self.write('DS ' + ('0' if channel=='ch1' else '1') \
						+ (',0' if slope else ',1'))
			self.write('DL ' + ('0' if channel=='ch1' else '1') \
						+ str(level))

	def set_count_preset(self, channel = 'T', time = 1.0, freqB = 1E3,query = False):
		'''
		:param channel: 'B' or 'T' for corresponding channel, defaults to 'T'
		:param time: preset time, defaults to 1.0
		:param freqB: B channel signal frequency, defaults to 1E3
		:param query: True for query rather setting, defaults to False
		:return: Returns the preset cycle number for channel B or T
		'''
		if channel == 'A':
			pass			
		elif channel == 'B':
			if query: 
				return self.query('CP 1')
			else:
				self.write('CP 1,%G' %(round(time*freqB)))	
		elif channel == 'T':
			if query: 
				return self.query('CP 2')
			else:
				self.write('CP 2,%G' %(round(time*1E7)))
	
	def set_count_input(self, counter = 'A', source = 'INPUT1', query:bool = False):
		counter_dict = {'A':0, 'B':1, 'T':2}
		source_dict = {'10MHz':0, 'INPUT1':1, 'INPUT2':2, 'TRIG':3}
		if query:
			return self.query('CI ' + str(counter_dict[counter]))
		else:
			if (counter == 'A') and (source_dict[source] <= 1):
				self.write('CI 0,' + str(source_dict[source]))
			elif (counter == 'B') and (1 <= source_dict[source] <= 2):
				self.write('CI 1,' + str(source_dict[source]))
			elif (counter == 'T') and (source_dict[source] != 1):
				self.write('CI 2,' + str(source_dict[source]))
			else:
				print('Illegal port mapping!')