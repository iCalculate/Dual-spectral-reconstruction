# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 11:43:30 2023

@author: ywang
"""
DevName = 'xxx-x-x' # will be inserted into filename of saved plot
Keithley_GPIB_Addr = 18  # Keithley 2400 SourceMeter GPIB address is 16
Model335_GPIB_Addr = 12  # LakeShore Model335 Cryogenic Temperature Controller
SR400_GPIB_Addr = 23  # Keithley 2400 SourceMeter GPIB address is 16


import SRS400
import time
import seaborn as sns

###   GPIB INITIALZATION   ###
SR400 = SRS400.sr400('GPIB0::' + str(SR400_GPIB_Addr) + '::INSTR')

###   MODE SETTING   ###
SR400.count_mode(mode = 'independent')  # set independent(A,B for T preset) count mode
SR400.set_count_input(counter = 'A', source = '10MHz')  # mapping internal 10MHz to counter A
SR400.dwell_time(dwell = 0.1)  # set dwell time(the interval time between counts)
SR400.set_count_preset(channel = 'T', time = 0.9)  # set preset window to control counting duration

###   SCAN PERIOD SETTING   ###
SR400.scan_periods(num = 1000)  # set N PERIOD
SR400.scan_end_mode(mode = 'STOP')  # set scan stop at N-period

###   GATE SETTING   ###
SR400.gate_window(channel = 'A', window = 200e-9)  # set gate window width
SR400.gate_mode(channel = 'A', mode = 'SCAN')  # set gate mode as SCAN(scan the delay)
SR400.gate_scan_step(channel = 'A', step = 100e-9)  # set delay step value
SR400.gate_delay_set(channel = 'A', delay = 0e-9)  # set initial delay value

###   TRIGGER SETTING   ###
SR400.set_disc_level(channel = 'trigger', level = 0.0, slope = False)  # set trigger disc. level and edge

###   DISPLAY SETTING   ###
SR400.display_mode(conti = False)  # set as hold display mode

buffer_len = SR400.scan_periods()

start_time_stamp = time.time()
SR400.count_restart()  # same as double click STOP and then single click START
SR400.lcd_message('Pulse Delay Scanning...')  # reset(double click STOP) will erase the custom message

while(not SR400.check_scan_finish()):
	pass
	time.sleep(0.1)
	time_stamp = time.time()-start_time_stamp
	loop = int(SR400.scan_position())
	if loop>=2:
		count = SR400.read_buffer_count(channel = 'ch1', bit = loop-1)
	else:
		count = -1
	print(f'\r[@{time_stamp:.2f} s] Recent period: {loop}/{buffer_len}   Last count = {count}', end = " ")

SR400.count_stop()
print('\n Scan Finished!')

count = []
for i in range(buffer_len-1):
	count.append(SR400.read_buffer_count(channel = 'ch1', bit = i+1))

SR400.close()  # Suspends port before program ends

x = range(0,100*(buffer_len-1),100) 
fig1 = sns.jointplot(x = "Delay (ns)", count = "Count")
fig1.show()

fig2 = sns.distplot(count, bins = 10)
fig2.set_xlabel("Count")
fig2.set_ylabel("Probability")
fig2.show()
