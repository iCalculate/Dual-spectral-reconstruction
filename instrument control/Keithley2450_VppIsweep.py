# -*- coding: utf-8 -*-
"""
Keithley 2450 I-source V-Sweep (V-I curve)
Du X.C., March 2023, Univ. of Electronic Science and Technology of China
Program to sweep current & measure voltage on Keithley 2450 SMU
Installed PyVISA for GPIB communication, and pymeasure for Keithley macro-lib (supported by CasperSchippers)
"""

SaveFiles = True   # Save the plot & data?  Only display if False.
RealTime = False   # True for real-time V-I curve, False for text print

Keithley_GPIB_Addr = 18  # Keithley 2400 SourceMeter GPIB address is 16
Model335_GPIB_Addr = 12
SR400_GPIB_Addr = 23  # Keithley 2400 SourceMeter GPIB address is 16

DevName = '298-2-4' # will be inserted into filename of saved plot
Temperature = 2
Light = True

SweepMode = 'Voltage' # 'Voltage' for I-V curve, 'Current' for V-I curve
VoltageComp = 2.0e0	   # compliance (max) current, unit: Volt.
CurrentComp = +1.5e-3	# compliance (max) current, unit: Amp.
bottom = 0.0
top = 0.9e-3
start = 0	 # starting value of current sweep, unit: Amp.
stop = 0	# ending value, unit: Amp.
polar = True
numcycles = 1  # number of cycles
numpoints = 100  # number of points in sweepspace

R_ser = 1016.5;

#import pyvisa as visa		  # PyVISA module, for GPIB comms
# use->  rm = visa.ResourceManager() 
#	->  rm.list_resources()
# to lists connectable address information
from pymeasure.instruments.keithley import keithley2450
import numpy as np # enable NumPy numerical analysis
import scipy.io	   #to save .mat format data
import time       # to allow pause between measurements
import os         # Filesystem manipulation - mkdir, paths etc.
import warnings	  # Use to ignore some warnings
import matplotlib.pyplot as plt # for python-style plottting
import cv2
import pytesseract as pyta
from PIL import Image
import re

pyta.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1024)
print('VideoCapture Init Finished')

# Initialize the GPIB interface
keithley = keithley2450.Keithley2450('GPIB0::' + str(Keithley_GPIB_Addr) + '::INSTR')

keithley.apply_current()             # Sets up to source current

#keithley.source_current_range = 10e-3   # Sets the source current range to 10 mA
'''A floating point property that controls the source current range in Amps, 
which can take values between -1.05 and +1.05 A. Auto-range is disabled when 
this property is set.
'''
keithley.compliance_voltage = VoltageComp     # Sets the compliance voltage to 10 V
keithley.source_current = 0         # Sets the source current to 0 mA
keithley.measure_voltage()          # Sets up to measure voltage
keithley.enable_source()            # Enables the source output
#print("keithley Current source initialized ...")
T_init = time.time()	# Record the initialization timestamp

_sentinel = object()
def sweeplist(bottom, top, start = _sentinel, stop = _sentinel, polarity = True, Ncycle:int = 1, Npoint:int = 100, RemoveNLP = True):

	if polarity:
		start = bottom if start == _sentinel else start   # initialization variable start and stop
		stop = (Ncycle%2)*top+((Ncycle+1)%2)*bottom if stop == _sentinel else stop
		if (Ncycle == 1) & (stop <= start):   # Check whether there is an illegal termination value
			stop = top
			warnings.warn("Meaningless variable 'stop', correct to top!")
	else:   # Check for negative polarity
		start = top if start == _sentinel else start
		stop = (Ncycle%2)*bottom+((Ncycle+1)%2)*top if stop == _sentinel else stop
		if (Ncycle == 1) & (stop >= start):
			stop = bottom
			warnings.warn("Meaningless variable 'stop', correct to bottom!")

	linespace = np.linspace(bottom, top, num=Npoint)   # generate sweep linear space
	ss = np.array([start, stop])
	mask = np.isin(ss, linespace)     # Determine whether a linear space has a start and end value
	linespace = np.sort(np.append(linespace,ss[~mask]))  # Append an sort values that do not appear
	if not polarity:
		linespace = np.flipud(linespace)    # For negative sweep, flip the linespace
	loc = np.append(np.where(linespace == start), np.where(linespace == stop)) # Look for the start-stop position
	first_loop = linespace[loc[0]:loc[1]+1]     # the first_loop is from start to stop
	seconde_loop = np.append(linespace[loc[1]+1:], np.flipud(linespace[loc[1]:-1])) # the seconde_loop is from stop to stop at anti-polarity sweep
	third_loop = np.append(np.flipud(linespace[:loc[1]]), linespace[1:loc[1]+1]) # the third_loop is from stop to stop at polarity sweep
	add_loop = np.append(third_loop, seconde_loop)  # add_loop is for multi-cycle sweep
	if Ncycle == 1:
		slist = first_loop
	elif Ncycle >= 2:
		if (polarity & (stop <= start))|(not polarity & (stop >= start)):
			first_loop = linespace[loc[0]:]
			seconde_loop =  np.flipud(linespace[loc[1]:-1])
			start_loop = np.append(first_loop, seconde_loop)
		else:
			start_loop = np.append(first_loop, seconde_loop)
		slist = np.append(start_loop, np.tile(add_loop, int(np.floor((Ncycle-2)/2))))
		if Ncycle%2 == 1:
			slist = np.append(slist, third_loop)
	if RemoveNLP:
		if not mask[0]:
			loc_start = np.argwhere(slist==ss[0])
			slist = np.delete(slist, loc_start[1:])
		if not mask[1]:
			loc_stop = np.argwhere(slist==ss[1])
			slist = np.delete(slist, loc_stop[:-1])
	return slist

# Loop to sweep voltage
OsciList = []
VppList = []
VpList = []
Voltage, Current_set, Current, Resistance, Time = ([] for i in range(5))
if RealTime: 
	plt.ion()

for I in sweeplist(bottom, top, start, stop, polarity = polar, Ncycle = numcycles, Npoint = numpoints):
	if not RealTime:
		pass
		print("Current set to: " + str(I) + " A" )
	keithley.ramp_to_current(I, steps=2, pause=20e-3) 
	'''
	Ramps to a target current from the set current value over
	a certain number of linear steps, each separated by a pause duration.
	:param target_current: A current in Amps
	:param steps: An integer number of steps
	:param pause: A pause duration in seconds to wait between steps

	try-> keithley.source_current = I
	which use SPIC macro as ":SOUR:CURR?", ":SOUR:CURR:LEV %g"
	'''
	Current_set.append(I)	   # Populate the set current array
	keithley.measure_voltage(nplc=1.0, voltage=21.0, auto_range=True) #nplc: from 0.01 to 10;voltage: from -210 V to 210 V
	vread = keithley.voltage	# Reads the voltage in Volts
	Voltage.append(vread)	   # Populate the test voltage array
	# keithley.measure_current(nplc=1.0, current=1.05e-4, auto_range=True) #current: Upper limit of current in Amps, from -1.05 A to 1.05 A
	cread = keithley.source_current	# Reads the current in Amps 
	Current.append(cread)	   # Populate the test current array
	# keithley.measure_resistance(nplc=1, resistance=2.1e5, auto_range=True)#resistance: Upper limit of resistance in Ohms, from -210 MOhms to 210 MOhms
	if cread == 0.0: 
		rread = float("inf")
	else:   
		rread = vread/cread         # Reads the resistance in Ohms
	Resistance.append(rread)        # Populate the set current array
	tread = time.time() - T_init    # RThe time difference between the initialization timestamp
	Time.append(tread)   # Populate the timestamp array
	if not RealTime:
		print("--> Voltage = " + str(Voltage[-1]) + ' V')   # print last read value
	if RealTime:
		plt.clf()
		plt.scatter(np.array(Current[-1])*1e3, np.array(Voltage[-1])-R_ser*np.array(Current[-1]),\
					marker = '.', c = 'red', s = 200, zorder = 2) 
		plt.plot(np.array(Current)*1e3, np.array(Voltage)-R_ser*np.array(Current), '*-', zorder = 1)
		plt.xlabel("Current (mA)")
		plt.ylabel("Voltage (V)")
		plt.pause(0.01)
		plt.ioff()
	while(cap.isOpened()):
		ret, frame = cap.read()
		#print(f'\rWaiting for ret is {ret}', end= " ")
		if ret == True:
			fig = frame[930:990,260:370,:]
			break
			#cv2.imshow("frame", frame)
		pass
		if cv2.waitKey(1000)&0xff == ord("q"):
			break
		pass
	Str = pyta.image_to_string(fig)
	#osci = Str.split('\n')
	OsciList.append(Str)
	pattern = '\d+\.\d+'
	osci = re.findall(pattern, Str)
	if len(osci) >=1:
		VppList.append(float(osci[0]))
		if len(osci) >=2:
			VpList.append(float(osci[1]))
		else:
			VpList.append(float("inf"))
	else:
		VppList.append(float("inf"))
	time.sleep(2.0)

keithley.shutdown()    # Ramps the current to 0 mA and disables output
keithley.triad(440, 0.2)    # Sounds a musical triad using the system beep
cap.release()
   
plt.ion()
plt.subplot(221)       # Plot V-I curve
plt.plot(np.array(Current)*1e3, np.array(Voltage)-R_ser*np.array(Current), '*-')
plt.xlabel("Current (mA)")
plt.ylabel("Voltage (V)")

plt.subplot(222)       # Plot R-t curve
plt.plot(Time, Resistance, 'r*-')
plt.xlabel("Time (s)")
plt.ylabel("Resistance (Ohm)")
ax = plt.gca()
ax.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')

plt.subplot(223)       # Plot dT-I curve
dT = np.array(Time[1:])-np.array(Time[:-1])
plt.plot(np.array(Current[:-1])* 1e3, dT, 'g*-')
plt.xlabel("Current (mA)")
plt.ylabel("dT (s)")

plt.subplot(224)       # Current set accurrcy histrogram
with warnings.catch_warnings():
	warnings.simplefilter("ignore")
	rate = np.array(Current_set)/np.array(Current) - 1.0
plt.hist(rate[~np.isnan(rate)], 30)
ax = plt.gca()
ax.ticklabel_format(style='sci', scilimits=(-1,2), axis='x')
	

if SaveFiles:
	# create subfolder if needed:
	if not os.path.isdir(DevName): os.mkdir(DevName)
	curtime = time.strftime('%y-%m-%d_%H-%M-%S')
	SavePath = os.path.join(DevName, 'VppIsweep_' + DevName + f'_{Temperature}K_Light{Light}' +'_[' + curtime +']' )
	
	data = np.array((Current, Current_set, Voltage, Resistance, Time, VppList, VpList))
	# save test data as ACSII text file
	np.savetxt(SavePath + '.txt', data.T, fmt="%e", delimiter="\t",\
			   header="Current(A)\ Voltage_set(V)\tVoltage(A)\tResistance(Ohm)\tTime(s)\tVpp(mV)\tVp(mV)")
	# save test data as .mat format file for MATLAB post-processing
	scipy.io.savemat(SavePath +'.mat', \
					 mdict = {'volt':Voltage, 'curr':Current, 'volt_set':Current_set, \
							  'resis':Resistance, 't':Time, 'Vpp':VppList, 'Vp':VpList})
#end if(SaveFiles)

