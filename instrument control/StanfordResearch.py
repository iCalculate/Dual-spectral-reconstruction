# -*- coding: utf-8 -*-
"""
LakeShore Model335/336 comm. lib.
Du X.C., June 2023, Univ. of Electronic Science and Technology of China
Installed PyVISA for GPIB communication.
"""

import serial
import pyvisa
import datetime
import time

class SR900 (object):
	def __init__(self, com_name, timeout:float = 0.5):
		
		self.ser = serial.Serial(port = com_name,
							baudrate = 115200,
							bytesize = serial.EIGHTBITS,
							parity = serial.PARITY_NONE,
							stopbits = serial.STOPBITS_ONE,
							timeout = 5.0) 
		print(com_name+' ->')
		self.ser.write("*IDN?\r\n".encode('utf-8'))
		idn = self.ser.readline()
		print(idn.decode())
		
	def write(self, string:str):
		string_term = string + "\r\n"
		self.ser.write(string_term.encode('utf-8'))
		
	def read(self):
		msg = self.ser.readline()
		return msg.decode('utf-8')

	def query(self, string:str):
		self.write(string)
		return self.ser.read_all()
	
	def close(self):
		self.ser.close()
		
	def set_on(self, port:int):
		self.write(f"SNDT {port},'OPON'")
	
	def set_off(self, port:int):
		self.write(f"SNDT {port},'OPOF'")
		
	def set_voltage(self, port:int, volt:float):
		self.write(f"SNDT {port},\"VOLT {volt:.3e}\"")
		
	def read_source_voltage(self, port):
		self.ser.flushInput()
		self.ser.reset_input_buffer()
		self.write(f"SNDT {port}, 'VOLT?'")
		self.write(f"GETN? {port},30")
		# time.sleep(1)
		readReg = self.ser.read_until(b'\r\n')
		print(readReg)
		volt = float(readReg[5:])
		self.ser.flushInput()
		return volt
	
	def read_meter_voltage(self, port:int, channel:int):
		self.ser.flushInput()
		self.write(f"SNDT {port}, 'VOLT? {channel}'")
# 		self.write(f"GETN? {port},20")
		self.write(f"RAWN? {port},80")
		readReg = self.ser.read_line()
		volt = float(readReg[5:])
		self.ser.flushInput()
		return volt
# 		self.write(f"SNDT {port}, 'VOLT?'")
# 		self.write(f"GETN? {port},30")
# 		readReg = self.ser.read_all()
# 		length = int(readReg[2:5])
# 		print(f"length is {length}")
# 		print(self.ser.read_all())
# 		self.write(f"RAWN? {port},{7}")
# 		time.sleep(3)
# 		string = readReg[5:-1]
# 		string = self.ser.read_all()
# 		print(string)
# 		return float(string)
# 		return self.query(f"SNDT {port}, 'VOLT?'\nRAWN? {port},10")
	
	
class SR542 (object):
	def __init__(self, com_name, timeout:float = 0.5):
		
		self.ser = serial.Serial(port = com_name,
							baudrate = 115200,
							bytesize = serial.EIGHTBITS,
							parity = serial.PARITY_NONE,
							stopbits = serial.STOPBITS_ONE,
							timeout = 0.5) 
		print(com_name+' ->')
		self.ser.write("*IDN?\r\n".encode('utf-8'))
		idn = self.ser.readline()
		print(idn.decode())
		
	def write(self, string:str):
		string_term = string + "\r\n"
		self.ser.write(string_term.encode('utf-8'))
		
	def read(self):
		msg = self.ser.readline()
		return msg.decode('utf-8')

	def query(self, string:str):
		self.write(string)
		return self.read()
	
	def close(self):
		self.ser.close()
	
	def on(self):
		self.write("MOTR ON")
		nowtime = datetime.datetime.now().strftime('%H:%M:%S')
		print(f'[{nowtime}] --> Chopper ON.')
		
	def off(self):
		self.write("MOTR OFF")
		nowtime = datetime.datetime.now().strftime('%H:%M:%S')
		print(f'[{nowtime}] --> Chopper OFF.')
	
	def mult(self, mult:int, query = False):
		if query:
			return self.query("MULT?")
		elif 1<=mult<=200:
			self.write("MULT "+str(mult))
		else:
			print("The chopper mult number must in [1, 200]")
	
	def divr(self, divr:int, query = False):
		if query:
			return self.query("DIVR?")
		elif 1<=divr<=200:
			self.write("DIVR "+str(divr))
		else:
			print("The chopper mult number must in [1, 200]")
			
	def disp(self, mode:int, query = False):
		if query:
			return self.query("DISP?")
		elif 0 <= mode <= 8:
			self.write("DISP "+str(mode))
		else:
			print("Incorrect display mode index")
	
	def read_freq(self, mode:int):
		if 0 <= mode <= 6:
			return self.query("MFRQ? "+str(mode))
		else:
			print("Incorrect freq_monitor mode index")
			
	def inter_freq(self, freq:float = 100, query = False):
		if query:
			return self.query("IFRQ?")
		elif 1.0<=freq<=1000.0:
			self.write(f"IFRQ {freq:.3f}")
		else:
			print("Illegal internal frequency value")
	

class SR400(object):
	def __init__(self, visa_name, timeout:int = 5000):
		rm = pyvisa.ResourceManager()
		
		self.pyvisa = rm.open_resource(visa_name)
		self.pyvisa.timeout = 5000 # Wait for instrument return value, default is infinite wait
		print(visa_name+' ->')
		print('Stanford Research,SR400,Photon Counter')
	
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
		if channel == -1:
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
			self.write('DL ' + ('0,' if channel=='ch1' else '1,') \
						+ str(level))

	def set_count_preset(self, channel = 'T', t = 1.0, freqB = 1E3,query = False):
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
				self.write('CP 1,%G' %(round(t*freqB)))	
		elif channel == 'T':
			if query: 
				return self.query('CP 2')
			else:
				self.write('CP 2,%G' %(round(t*1E7)))
	
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
					

class SR830(object):
	def __init__(self, visa_name, timeout:int = 5000):
		rm = pyvisa.ResourceManager()
		self.pyvisa = rm.open_resource(visa_name)
		self.pyvisa.timeout = 500 # Wait for instrument return value, default is infinite wait
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
	
	#### REFERENCE and PHASE COMMANDS ####
	
	def set_ref_phase(self, phase:float=0.0, query:bool = False):
		'''
		:param phase: The PHAS command sets or queries the reference phase shift. The parameter x is the phase (real number of degrees). The PHAS x command will set the phase shift to x. The value of x will be rounded to 0.01°. The phase may be programmed from -360.00 £ x £ 729.99 and will be wrapped around at ±180°. For example, the PHAS 541.0 command will set the phase to -179.00° (541-360=181=-179). The PHAS? queries the
phase shift.
		'''
		if query:
			return float(self.query('PHAS?'))
		else:
			self.write(f'PHAS {phase:.4f}')
	
	def set_ref_mode(self, inter:bool=True, query:bool = False):
		'''
		:param inter: The FMOD command sets or queries the reference source. The parameter i selects internal (i=1) or external (i=0).
		'''
		if query:
			return bool(self.query('FMOD?'))
		else:
			self.write(f'FMOD {int(inter)}')
	
	def set_ref_freq(self, freq:float=1000.0, query:bool = False):
		'''
		:param freq: The FREQ f command sets the frequency of the internal oscillator. This command is allowed only if the reference source is internal. The parameter f is a frequency (real number of Hz). The value of f will be rounded to 5 digits or 0.0001 Hz, whichever is greater. The value of f is limited to 0.001 £ f £ 102000. If the harmonic number is greater than 1, then the frequency is limited to nxf £ 102 kHz where n is the harmonic number.
		'''
		if query:
			return float(self.query('FREQ?'))
		else:
			self.write(f'FREQ {freq:.4f}')
			
	def set_ref_triggermode(self, mode:int=0, query:bool = False):
		'''
		:param mode: zero crossing (i=0), TTL rising edge (i=1), , or TTL falling edge (i=2), defaults to zero crossing
		'''
		if query:
			return int(self.query('SRLP?'))
		else:
			self.write(f'SRLP {mode}')
			
	def set_ref_harmonic(self, harmonic:int=1, query:bool = False):
		'''
		:param harmonic: The HARM command sets or queries the detection harmonic. This parameter is an integer from 1 to 19999. The HARM i command will set the lock-in to detect at the ith harmonic of the reference frequency, defaults to 1
		'''
		if query:
			return int(self.query('HARM?'))
		else:
			self.write(f'HARM {harmonic}')
			
	def set_ref_outputlevel(self, level:float=1.0, query:bool = False):
		'''
		:param level: The SLVL command sets or queries the amplitude of the sine output. The parameter x is a voltage (real number of Volts)., defaults to 1.0
		'''
		if query:
			return float(self.query('SLVL?'))
		else:
			self.write(f'SLVL {level:.4f}')
			
	#### INPUT and FILTER COMMANDS ####
	
	def set_input_config(self, config:int=0, query:bool=False):
		'''
		:param config: The ISRC command sets or queries the input configuration. The parameter i selects A (i=0), A-B (i=1), I (1 MW) (i=2) or I (100 MW) (i=3).
		'''
		if query:
			return int(self.query('ISRC?'))
		else:
			self.write(f'ISRC {config}')
			
	def set_input_grounding(self, grounding:bool=False, query:bool=False):
		'''
		:param grounding: The IGND command sets or queries the input shield grounding. The parameter i selects Float (i=0) or Ground (i=1).
		'''
		if query:
			return int(self.query('IGND?'))
		else:
			self.write(f'IGND {int(grounding)}')
			
	def set_input_coupling(self, DC:bool=True, query:bool=False):
		'''
		:param DC: The ICPL command sets or queries the input coupling. The parameter i selects AC (i=0) or DC (i=1).
		'''
		if query:
			return int(self.query('ICPL?'))
		else:
			self.write(f'ICPL {int(DC)}')
	
	def set_input_notchfilter(self, state:int=0, query:bool=False):
		'''
		:param state: The ILIN command sets or queries the input line notch filter status. The parameter i selects Out or no filters (i=0), Line notch in (i=1), 2xLine notch in (i=2) or Both notch filters in (i=3).
		'''
		if query:
			return int(self.query('ILIN?'))
		else:
			self.write(f'ILIN {state}')
	
	#### GAIN and TIME CONSTANT COMMANDS ####
	
	def set_sens_sensitivity(self, sensitivity:int=26, query:bool=False):
		'''
		
		:param sensitivity:
			0 2 nV/fA         13 50 μV/pA
			1 5 nV/fA         14 100 μV/pA
			2 10 nV/fA        15 200 μV/pA
			3 20 nV/fA        16 500 μV/pA
			4 50 nV/fA        17 1 mV/nA
			5 100 nV/fA       18 2 mV/nA
			6 200 nV/fA       19 5 mV/nA
			7 500 nV/fA       20 10 mV/nA
			8 1 μV/pA         21 20 mV/nA
			9 2 μV/pA         22 50 mV/nA
			10 5 μV/pA        23 100 mV/nA
			11 10 μV/pA       24 200 mV/nA
			12 20 μV/pA       25 500 mV/nA
			                  26 1 V/μA
		'''
		if query:
			return int(self.query('SENS?'))
		else:
			self.write(f'SENS {sensitivity}')
		
	def set_sens_reserve(self, mode:int=1, query:bool=False):
		'''
		:param sensitivity: The RMOD command sets or queries the reserve mode. The parameter i selects High Reserve (i=0), Normal (i=1) or Low Noise (minimum) (i=2). See the description of the [Reserve] key for the actual reserves for each sensitivity.
		'''
		if query:
			return int(self.query('RMOD?'))
		else:
			self.write(f'RMOD {mode}')

	def set_sens_timeconstant(self, time_const:int=6, query:bool=False):
		'''
		:param time_const: 
			0 10 μs           10 1 s
			1 30 μs           11 3 s
			2 100 μs          12 10 s
			3 300 μs          13 30 s
			4 1 ms            14 100 s
			5 3 ms            15 300 s
			6 10 ms           16 1 ks
			7 30 ms           17 3 ks
			8 100 ms          18 10 ks
			9 300 ms          19 30 ks
		'''
		if query:
			return int(self.query('OFLT?'))
		else:
			self.write(f'OFLT {time_const}')
		
	def set_sens_lpfslope(self, slope:int=0, query:bool=False):
		'''
		:param slope: The OFSL command sets or queries the low pass filter slope. The parameter i selects 6 dB/oct (i=0), 12 dB/oct (i=1), 18 dB/oct (i=2) or 24 dB/oct (i=3).
		'''
		if query:
			return int(self.query('OFSL?'))
		else:
			self.write(f'OFSL {slope}')
			
	def set_sens_synchronous(self, status:bool=True, query:bool=False):
		'''
		:param status: The SYNC command sets or queries the synchronous filter status. The parameter i selects Off (i=0) or synchronous filtering below 200 Hz (i=1). Synchronous filtering is turned on only if the detection frequency (reference x harmonic number) is less than 200 Hz.
		'''
		if query:
			return bool(self.query('SYNC?'))
		else:
			self.write(f'SYNC {int(status)}')
			
	#### DISPLAY and OUTPUT COMMANDS ####
	
	def set_disp_display(self, channel:int=1, display:int=0, ratio:int=0):
		'''
		
		:param channel: 
			CH1 (i=1)       CH2 (i=2)
			j display       j display
			0 X             0 Y
			1 R             1 q
			2 X Noise       2 Y Noise
			3 Aux In 1      3 Aux In 3
			4 Aux In 2      4 Aux In 4
			k ratio         k ratio
			0 none          0 none
			1 Aux In 1      1 Aux In 3
			2 Aux In 2      2 Aux In 4

		'''
		self.write(f'DDEF {channel},{display},{ratio}')
	
	#### DATA STORAGE COMMANDS ####
	 
	def set_buffer_rate(self, rate:int=4, query:bool=False):
		'''
		:param rate:   
			0 62.5 mHz   7 8 Hz
			1 125 mHz    8 16 Hz
			2 250 mHz    9 32 Hz
			3 500 mHz   10 64 Hz
			4 1 Hz      11 128 Hz
			5 2 Hz      12 256 Hz
			6 4 Hz      13 512 Hz
						14 Trigger
		'''
		if query:
			return int(self.query('SRAT ?'))
		else:
			self.write(f'SRAT {rate}')
		
	def set_buffer_endmode(self, loopmode:bool=False, query:bool=False):
		'''
		:param loopmode: The SEND command sets or queries the end of buffer mode. The parameter i selects 1 Shot (i=0) or Loop (i=1). If Loop mode is used, make sure to pause data storage before reading the data to avoid confusion about which point is the most recent.
		'''
		if query:
			return bool(self.query('SEND ?'))
		else:
			self.write(f'SEND {int(loopmode)}')
	
	def set_buffer_trigger(self):
		self.write('TRIG')
		
	def set_buffer_startmode(self, scanmode:bool=False, query:bool=False):
		'''
		:param scanmode: The TSTR command sets or queries the trigger start mode. The parameter i=1 selects trigger starts the scan and i=0 turns the trigger start feature off.
		'''
		if query:
			return bool(self.query('TSTR ?'))
		else:
			self.write(f'TSTR {int(scanmode)}')
			
	def set_buffer_start(self):
		'''
		:return: The STRT command starts or resumes data storage. STRT is ignored if storage is already in progress.
		'''
		self.write('STRT')
		
	def set_buffer_pause(self):
		'''
		:return: The PAUS command pauses data storage. If storage is already paused or reset then this command is ignored.
		'''
		self.write('PAUS')
		
	def set_buffer_reset(self):
		'''
		:return: The REST command resets the data buffers. The REST command can be sent at any time - any storage in progress, paused or not, will be reset. This command will erase the data buffer.
		'''
		self.write('REST')
	
	#### DATA TRANSFER COMMANDS ####
	
	def read_X(self):
		return float(self.query('OUTP ? 1'))
	
	def read_Y(self):
		return float(self.query('OUTP ? 2'))
	
	def read_R(self):
		return float(self.query('OUTP ? 3'))
	
	def read_T(self):
		return float(self.query('OUTP ? 4'))
	
	def read_all(self):
		data = []
		data.append(self.read_X())
		data.append(self.read_Y())
		data.append(self.read_R())
		data.append(self.read_T())
		return data
	
	def read_aux(self):
		return [float(i) for i in self.query('SNAP ? 5,6,7,8').split(',')]
	
	def read_freqref(self):
		return float(self.query('SNAP ? 9,10,11'))
	
	def read_buffer_depth(self):
		'''
		:return: The SPTS? command queries the number of points stored in the buffer. Both displays have the same number of points. If the buffer is reset, then 0 is returned. Remember, SPTS? returns N where N is the number of points - the points are numbered from 0 (oldest) to N-1 (most recent). The SPTS? command can be sent at any time, even while storage is in progress. This command is a query only command.
		'''
		return int(self.query('SPTS ?'))
	
	def read_buffer_data(self, buffer:int=1, start:int=0, num:int=10):
		'''
		:param buffer: The TRCA? command queries the points stored in the Channel i buffer. The values are returned as ASCII floating point numbers with the units of the trace. Multiple points are separated by commas and the final point is followed by a terminator.
		The parameter i selects the display buffer (i=1, 2) and is required. Points are read from the buffer starting at bin j (j³0). A total of k bins are read (k³1). To read a single point, set k=1. Both j and k are required. If j+k exceeds the number of stored points (as returned by the SPTS? query), then an error occurs. Remember, SPTS? returns N where N is the total number of bins - the TRCA? command numbers the bins from 0 (oldest) to N-1 (most recent). If data storage is set to Loop mode, make sure that storage is paused before reading any data. This is because the points are indexed relative to the most recent point which is continually
changing.
		'''
		buffer_str = self.query(f'TRCA ? {buffer},{start},{num}')
		buffer_data = [float(i) for i in buffer_str.split(',')[0:-1]]
		return buffer_data
	
	#### STATUS REPORTING COMMANDS ####
	
	def read_reg_errorstatus(self):
		'''
		:return: 
			0 Unused
			1 Backup Error Set at power up when the battery backup has failed.
			2 RAM Error Set when the RAM Memory test finds an error.
			3 Unused
			4 ROM Error Set when the ROM Memory test finds an error.
			5 GPIB Error Set when GPIB fast data transfer mode aborted.
			6 DSP Error Set when the DSP test finds an error.
			7 Math Error Set when an internal math error occurs.
		'''
		error_status = self.query('ERRS?')
		return list(f'{error_status:08b}')[::-1]
		
	def read_reg_lia(self):
		'''
		:return: 
			0 INPUT/RESRV Set when an Input or Amplifier overload is detected.
			1 FILTR Set when a Time Constant filter overload is detected.
			2 OUTPT Set when an Output overload is detected.
			3 UNLK Set when a reference unlock is detected.
			4 RANGE Set when the detection frequency switches ranges (harmonic x ref. frequency decreases below 199.21 Hz or increases above 203.12 Hz). Time constants above 30 s and Synchronous filtering are turned off in the upper frequency range.
			5 TC Set when the time constant is changed indirectly, either by changing frequency range, dynamic reserve, filter slope or expand.
			6 TRIG Set when data storage is triggered. Only if samples or scans are in externally triggered mode.
			7 unused
		'''
		lia_status = self.query('LIAS?')
		return list(f'{lia_status:08b}')[::-1]
		
		
			
	