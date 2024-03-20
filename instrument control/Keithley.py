# -*- coding: utf-8 -*-
"""
Keithley 2400 SourceMeter comm. lib.
Du X.C., March 2023, Univ. of Electronic Science and Technology of China
Installed PyVISA for GPIB communication.
"""

import pyvisa
import time
import datetime
from pymeasure.instruments.keithley import keithley2450
import numpy as np
# from time import sleep
# from matlplotlib import pyplot as plt 

class Model2450(object):
	def __init__(self, visa_name):
		self.smu = keithley2450.Keithley2450(visa_name)
		
		print(visa_name+' ->')
		print(self.smu.ask("*IDN?"))
		
	def close(self):
		try:
			self.smu.shutdown()
		except Exception:
			pass
	
	def reset(self):
		self.smu.reset()
	
	def read(self):
		return self.smu.read()
	
	def write(self, string):
		self.smu.write(string)
		
	def query(self, string):
		return self.smu.ask(string)
	
	def on(self):
		self.smu.enable_source()
		
	def off(self):
		self.smu.disable_source()
				
	def beeper(self, freq = 5000, t = 0.3, loop = 1, lyric = False):
		if lyric == False:
			for i in range(loop):
				self.write(":SYSTem:BEEPer "+str(freq)+","+str(t))
				time.sleep(t*2)
		elif lyric == True:
			self.write(":SYSTem:BEEPer 1046, 0.1")
			time.sleep(0.1)
			self.write(":SYSTem:BEEPer 784, 0.1")
			time.sleep(0.1)
			self.write(":SYSTem:BEEPer 523, 0.1")
			time.sleep(0.1)
			self.write(":SYSTem:BEEPer 587, 0.2")
	
	def initSourceCurr(self, compVolt, currRange = None):
		self.smu.apply_current(current_range=currRange)
		self.smu.compliance_voltage = compVolt
		self.smu.source_current = 0.0
			
	def initSourceVolt(self, compCurr, voltRange = None):
		self.smu.apply_voltage(voltage_range=voltRange)
		self.smu.compliance_current = compCurr
		self.smu.source_voltage = 0.0
	
	def initSenseVolt(self, senseRange = 21, nplc = 1, autoRange = True):
		self.smu.measure_voltage(nplc=nplc, voltage=senseRange, auto_range=autoRange)
		
	def initSenseCurr(self, senseRange = 1.05e-4, nplc = 1, autoRange = True):
		self.smu.measure_current(nplc=nplc, current=senseRange, auto_range=autoRange)
		
	def getCurrData(self):
		self.write(":SENS:FUNC 'CURR'")
		return float(self.query(":READ?"))
	
	def getVoltData(self):
		self.write(":SENS:FUNC 'VOLT'")
		return float(self.query(":READ?"))
		
	def executeCustomCurrSweep(self, currList:list, rev = False):
		nowtime = datetime.datetime.now().strftime('%H:%M:%S')
		print(f'[{nowtime}] Execute Custom Current Sweep with {len(currList)} points...',end='')
		dataMat = []
		if rev == True:
			currList.extend(currList[::-1])
		start_time = time.time()
		self.beeper(freq=4000,t=0.2,loop=1)
		self.on()
		for I in currList:
			#self.smu.ramp_to_voltage(I,steps = 1,pause=0.0)
			self.smu.source_current = I
			curr = I
			volt = self.getVoltData()
			if curr == 0:
				resis = volt/self.getCurrData()
			else:
				resis = volt/curr
			t = time.time()-start_time
			Mat = [volt, curr, resis, t]
			dataMat.append(Mat)
		self.off()
		self.beeper(freq=4000,t=0.2,loop=2)
		nowtime = datetime.datetime.now().strftime('%H:%M:%S')
		print(f'[{nowtime}] --> Current Sweep Finished!')
		return dataMat

	def executeCurrSweep(self, top, num, rev = True, loop = False ,polar = True, sleeptime = 0):
		nowtime = datetime.datetime.now().strftime('%H:%M:%S')
		print(f'[{nowtime}] Execute Current Sweep from 0 to {top}A with {num} points...')
		dataMat = []
		currList = [i/num*top for i in list(range(0, num+1))]
		if rev ==True: currList.extend(currList[::-1])
		if loop == True:
			currList.extend([-i for i in currList])
		start_time = time.time()
		self.beeper(freq=4000,t=0.2,loop=1)
		cycle = 0
		self.smu.source_current = currList[0]
		self.on()
		time.sleep(sleeptime)
		for I in currList:
			print(f'\rrate of process: {(cycle-1)/num*50:.2f}%',end='')
			cycle += 1
			#self.smu.ramp_to_voltage(I,steps = 1,pause=0.0)
			self.smu.source_current = I
			curr = I
			volt = self.getVoltData()
			if curr == 0:
				resis = volt/self.getCurrData()
			else:
				resis = volt/curr
			t = time.time()-start_time
			Mat = [volt, curr, resis, t]
			dataMat.append(Mat)
		self.off()
		self.beeper(freq=4000,t=0.2,loop=2)
		nowtime = datetime.datetime.now().strftime('%H:%M:%S')
		print('\r',end='')
		print(f'[{nowtime}] --> Current Sweep Finished!')
		return dataMat
	
	def executeCurrLogSweep(self, start, stop, num, loop = False ,polar = True):
		nowtime = datetime.datetime.now().strftime('%H:%M:%S')
		print(f'[{nowtime}] Execute Current Log Sweep from {start} to {stop}A with {num} points...')
		dataMat = []
		start_log = np.log10(start)
		stop_log = np.log10(stop)
		currList = [start_log+i/num*(stop_log-start_log) for i in list(range(0, num+1))]
		currList = list(np.power(10,currList))
		currList.extend(currList[::-1])
		if loop == True:
			currList.extend([-i for i in currList])
		start_time = time.time()
		self.beeper(freq=4000,t=0.2,loop=1)
		self.on()
		for I in currList:
			#self.smu.ramp_to_voltage(I,steps = 1,pause=0.0)
			self.smu.source_current = I
			curr = I
			volt = self.getVoltData()
			if curr == 0:
				resis = volt/self.getCurrData()
			else:
				resis = volt/curr
			t = time.time()-start_time
			Mat = [volt, curr, resis, t]
			dataMat.append(Mat)
		self.off()
		self.beeper(freq=4000,t=0.2,loop=2)
		nowtime = datetime.datetime.now().strftime('%H:%M:%S')
		print(f'[{nowtime}] --> Current Log Sweep Finished!')
		return dataMat
	
	def executeCustomVoltSweep(self, voltList:list, rev = False):
		nowtime = datetime.datetime.now().strftime('%H:%M:%S')
		print(f'[{nowtime}] Execute Custom Voltage Sweep with {len(voltList)} points...')
		dataMat = []
		if rev == True:
			voltList.extend(voltList[::-1])
		start_time = time.time()
		self.beeper(freq=4000,t=0.2,loop=1)
		self.on()
		for V in voltList:
			#self.smu.ramp_to_voltage(V,steps = 1,pause=20e-3)
			self.smu.source_voltage = V
			volt = V
			curr = self.getCurrData()
			resis = volt/curr
			t = time.time()-start_time
			Mat = [volt, curr, resis, t]
			dataMat.append(Mat)
		self.off()
		self.beeper(freq=4000,t=0.2,loop=2)
		nowtime = datetime.datetime.now().strftime('%H:%M:%S')
		print(f'[{nowtime}] --> Voltage Sweep Finished!')
		return dataMat
	
	def executeVoltSweep(self, top, num, loop = False ,polar = True):
		nowtime = datetime.datetime.now().strftime('%H:%M:%S')
		print(f'[{nowtime}] Execute Voltage Sweep from 0 to {top}V with {num} points...')
		dataMat = []
		voltList = [i/num*top for i in list(range(0, num+1))]
		voltList.extend(voltList[::-1])
		if loop == True:
			voltList.extend([-i for i in voltList])
		start_time = time.time()
		self.beeper(freq=4000,t=0.2,loop=1)
		self.on()
		for V in voltList:
			#self.smu.ramp_to_voltage(V,steps = 1,pause=20e-3)
			self.smu.source_voltage = V
			volt = V
			curr = self.getCurrData()
			resis = volt/curr
			t = time.time()-start_time
			Mat = [volt, curr, resis, t]
			dataMat.append(Mat)
		self.off()
		self.beeper(freq=4000,t=0.2,loop=2)
		nowtime = datetime.datetime.now().strftime('%H:%M:%S')
		print(f'[{nowtime}] --> Voltage Sweep Finished!')
		return dataMat
	
	def executeVoltLogSweep(self, start, stop, num, loop = False ,polar = True):
		nowtime = datetime.datetime.now().strftime('%H:%M:%S')
		print(f'[{nowtime}] Execute Voltage Log Sweep from {start} to {stop}A with {num} points...')
		dataMat = []
		start_log = np.log10(start)
		stop_log = np.log10(stop)
		voltList = [start_log+i/num*(stop_log-start_log) for i in list(range(0, num+1))]
		voltList = list(np.power(10,voltList))
		voltList.extend(voltList[::-1])
		if loop == True:
			voltList.extend([-i for i in voltList])
		start_time = time.time()
		self.beeper(freq=4000,t=0.2,loop=1)
		self.on()
		for V in voltList:
			#self.smu.ramp_to_voltage(V,steps = 1,pause=20e-3)
			self.smu.source_voltage = V
			volt = V
			curr = self.getCurrData()
			resis = volt/curr
			t = time.time()-start_time
			Mat = [volt, curr, resis, t]
			dataMat.append(Mat)
		self.off()
		self.beeper(freq=4000,t=0.2,loop=2)
		nowtime = datetime.datetime.now().strftime('%H:%M:%S')
		print(f'[{nowtime}] --> Voltage Log Sweep Finished!')
		return dataMat
	
	
	def executeCurrBias(self, bias, num):
		nowtime = datetime.datetime.now().strftime('%H:%M:%S')
		print(f'[{nowtime}] Execute Current Bias at {bias}A with {num} points...')
		dataMat = []
		self.smu.source_current = bias
		start_time = time.time()
		self.on()	
		cycle = 0
		for i in range(num):
			cycle += 1
			print(f'\rrate of process: {cycle/num*100:.2f}%',end='')
			t = time.time()-start_time
			volt = self.getVoltData()
			resis = volt/bias
			dataMat.append([volt, bias, resis, t])
		self.off()
		self.beeper(freq=4000,t=0.2,loop=2)
		nowtime = datetime.datetime.now().strftime('%H:%M:%S')
		print(f'\r[{nowtime}] --> Current Bias Finished!')
		return dataMat
	
	def executeVoltBias(self, bias, num):
		nowtime = datetime.datetime.now().strftime('%H:%M:%S')
		print(f'[{nowtime}] Execute Voltage Bias at {bias}V with {num} points...')
		dataMat = []
		self.smu.source_voltage = bias
		self.beeper(freq=4000,t=0.2,loop=1)
		start_time = time.time()
		self.on()
		for i in range(num):
			t = time.time()-start_time
			curr = self.getCurrData()
			resis = bias/curr
			dataMat.append([bias, curr, resis, t])
		self.off()
		self.beeper(freq=4000,t=0.2,loop=2)
		nowtime = datetime.datetime.now().strftime('%H:%M:%S')
		print(f'[{nowtime}] --> Voltage Bias Finished!')
		return dataMat
	
	def executeCurrBiasStep(self, start, stop, stepnum, num):
		nowtime = datetime.datetime.now().strftime('%H:%M:%S')
		print(f'[{nowtime}] Execute Current Bias Step from {start}A to {stop}A with {num} points...')
		dataMat = []
		currList = [i/stepnum*(stop-start)+start for i in list(range(0, stepnum+1))]
		self.smu.source_current = currList[0]
		start_time = time.time()
		self.on()
		cycle = 0
		for Ibias in currList:
			cycle += 1
			print(f'\rrate of process: {cycle}/{stepnum+1} loops at {Ibias*1e3:.3f} mA%',end='')
			self.smu.source_current = Ibias
			for i in range(num):
				t = time.time()-start_time
				volt = self.getVoltData()
				if Ibias == 0:
					resis = volt/self.getCurrData()
				else:
					resis = volt/Ibias
				dataMat.append([volt, Ibias, resis, t])
		self.off()
		self.beeper(freq=4000,t=0.2,loop=2)
		nowtime = datetime.datetime.now().strftime('%H:%M:%S')
		print(f'\r[{nowtime}] --> Current Bias Step Finished!')
		return dataMat
	
	def executeVoltBiasStep(self, start, stop, stepnum, num):
		nowtime = datetime.datetime.now().strftime('%H:%M:%S')
		print(f'[{nowtime}] Execute Current Bias Step from {start}V to {stop}V with {num} points...')
		dataMat = []
		voltList = [i/stepnum*(stop-start)+start for i in list(range(0, stepnum+1))]
		self.smu.source_voltage = voltList[0]
		self.beeper(freq=4000,t=0.2,loop=1)
		start_time = time.time()
		self.on()
		for Vbias in voltList:
			self.smu.source_voltage = Vbias
			for i in range(num):
				t = time.time()-start_time
				curr = self.getCurrData()
				resis = Vbias/curr
				dataMat.append([Vbias, curr, resis, t])
		self.off()
		self.beeper(freq=4000,t=0.2,loop=2)
		nowtime = datetime.datetime.now().strftime('%H:%M:%S')
		print(f'[{nowtime}] --> Voltage Bias Step Finished!')
		return dataMat
		
		
			
class Model2400(object):
	def __init__(self, visa_name, timeout:int = 5000):
		rm = pyvisa.ResourceManager()
		self.pyvisa = rm.open_resource(visa_name)
		self.pyvisa.timeout = 500 # Wait for instrument return value, default is infinite wait
		print(visa_name+' ->')
		print(self.pyvisa.query("*IDN?"))
		
	def close(self):
		try:
			self.pyvisa.close()
		except Exception:
			pass
	
	def reset(self):
		self.write("*RST")
	
	def read(self):
		return self.pyvisa.read()
	
	def write(self, string):
		self.pyvisa.write(string)
		
	def query(self, str):
		return self.pyvisa.query(str)
	
	def on(self):
		self.write(":OUTP ON")
		
	def off(self):
		self.write(":OUTP OFF")
		
	def local(self):
		self.write("SYSTEM:KEY 23") # simulate keypress "LOCAL"
		
	def beeper(self, freq = 5000, t = 0.3, loop = 1, lyric = False):
		if lyric == False:
			for i in range(loop):
				self.write(":SYSTem:BEEPer "+str(freq)+","+str(t))
				time.sleep(t)
		elif lyric == True:
			self.write(":SYSTem:BEEPer 1046, 0.1")
			time.sleep(0.1)
			self.write(":SYSTem:BEEPer 784, 0.1")
			time.sleep(0.1)
			self.write(":SYSTem:BEEPer 523, 0.1")
			time.sleep(0.1)
			self.write(":SYSTem:BEEPer 587, 0.2")
	
	def initSourceCurr(self, autorange = True, fixed = True):
		self.write(":SOUR:FUNC:MODE CURR")
		if fixed:
			self.write(":SOURce:CURRent:MODE FIXed")
		if autorange:
			self.write(":SOURce:CURRent:RANGe:AUTO 1")
		self.write(":SOUR:CURR 0.0")
			
	def initSourceVolt(self, autorange = True, fixed = True):
		self.write(":SOUR:FUNC:MODE VOLT")
		if fixed:
			self.write(":SOURce:VOLTage:MODE FIXed")
		if autorange:
			self.write(":SOURce:VOLTage:RANGe:AUTO 1")
		self.write(":SOUR:VOLT 0.0")
	
	def initSenseVolt(self, voltComp, autorange = True):
		self.write(":SENS:FUNC \"VOLT\"")
		self.write(":SENS:VOLT:PROT:LEV " + str(voltComp))
		if autorange:
			self.write(":SENS:VOLT:RANGE:AUTO 1")
			
	def initSenseCurr(self, currComp, autorange = True):
		self.write(":SENS:FUNC \"CURR\"")
		self.write(":SENS:CURR:PROT:LEV " + str(currComp))
		if autorange:
			self.write(":SENS:CURR:RANGE:AUTO 1")
			
	def setSourceCurr(self, curr):
		self.write(":SOUR:CURR " + str(curr))
		
	def setSourceVolt(self, curr):
		self.write(":SOUR:VOLT " + str(curr))
		
	def getData(self):
		raw = self.query(":READ?")
		answer = [float(c) for c in raw.split(',')]
		answer[4] = int(answer[4])    # change STATUS to int format
		return answer    #[Volt, Curr, Resis, Time, Status]
	
	def systemTimeReset(self):
		self.write(":SYSTem:TIME:RESet")
		
	def executeCurrSweep(self, top, num, loop = False ,polar = True):
		nowtime = datetime.datetime.now().strftime('%H:%M:%S')
		print(f'[{nowtime}] Execute Current Sweep from 0 to {top}A with {num} points...')
		dataMat = []
		currList = [i/num*top for i in list(range(0, num+1))]
		currList.extend(currList[::-1])
		if loop == True:
			currList.extend([-i for i in currList])
		self.on()
		for I in currList:
			self.setSourceCurr(I)
			dataMat.append(self.getData())
		self.off()
		self.beeper(freq=4000,t=0.2,loop=2)
		nowtime = datetime.datetime.now().strftime('%H:%M:%S')
		print(f'[{nowtime}] --> Current Sweep Finished!')
		return dataMat
	
	def executeVoltSweep(self, top, num, loop = False ,polar = True):
		nowtime = datetime.datetime.now().strftime('%H:%M:%S')
		print(f'[{nowtime}] Execute Voltage Sweep from 0 to {top}V with {num} points...')
		dataMat = []
		voltList = [i/num*top for i in list(range(0, num+1))]
		voltList.extend(voltList[::-1])
		if loop == True:
			voltList.extend([-i for i in voltList])
		self.on()
		for V in voltList:
			self.setSourceVolt(V)
			dataMat.append(self.getData())
		self.off()
		self.beeper(freq=4000,t=0.2,loop=2)
		nowtime = datetime.datetime.now().strftime('%H:%M:%S')
		print(f'[{nowtime}] --> Voltage Sweep Finished!')
		return dataMat
	
	def executeCurrBias(self, bias, num):
		nowtime = datetime.datetime.now().strftime('%H:%M:%S')
		print(f'[{nowtime}] Execute Current Bias at {bias}A with {num} points...')
		dataMat = []
		self.setSourceCurr(bias)
		self.on()		
		for i in range(num):
			dataMat.append(self.getData())
		self.off()
		self.beeper(freq=4000,t=0.2,loop=2)
		nowtime = datetime.datetime.now().strftime('%H:%M:%S')
		print(f'[{nowtime}] --> Current Bias Finished!')
		return dataMat
	
	def executeVoltBias(self, bias, num):
		nowtime = datetime.datetime.now().strftime('%H:%M:%S')
		print(f'[{nowtime}] Execute Voltage Bias at {bias}V with {num} points...')
		dataMat = []
		self.setSourceVolt(bias)
		self.on()
		for i in range(num):
			dataMat.append(self.getData())
		self.off()
		self.beeper(freq=4000,t=0.2,loop=2)
		nowtime = datetime.datetime.now().strftime('%H:%M:%S')
		print(f'[{nowtime}] --> Voltage Bias Finished!')
		return dataMat
	
	def executeCurrBiasStep(self, start, stop, stepnum, num):
		nowtime = datetime.datetime.now().strftime('%H:%M:%S')
		print(f'[{nowtime}] Execute Current Bias Step from {start}A to {stop}A with {num} points...')
		dataMat = []
		currList = [i/stepnum*(stop-start)+start for i in list(range(0, stepnum+1))]
		self.setSourceCurr(currList[0])
		self.on()
		for Ibias in currList:
			self.setSourceCurr(Ibias)
			for i in range(num):
				dataMat.append(self.getData())
		self.off()
		self.beeper(freq=4000,t=0.2,loop=2)
		nowtime = datetime.datetime.now().strftime('%H:%M:%S')
		print(f'[{nowtime}] --> Current Bias Step Finished!')
		return dataMat
	
	def executeVoltBiasStep(self, start, stop, stepnum, num):
		nowtime = datetime.datetime.now().strftime('%H:%M:%S')
		print(f'[{nowtime}] Execute Current Bias Step from {start}V to {stop}V with {num} points...')
		dataMat = []
		voltList = [i/stepnum*(stop-start)+start for i in list(range(0, stepnum+1))]
		self.setSourceVolt(voltList[0])
		self.on()
		for Vbias in voltList:
			self.setSourceVolt(Vbias)
			for i in range(num):
				dataMat.append(self.getData())
		self.off()
		self.beeper(freq=4000,t=0.2,loop=2)
		nowtime = datetime.datetime.now().strftime('%H:%M:%S')
		print(f'[{nowtime}] --> Voltage Bias Step Finished!')
		return dataMat	

			












	