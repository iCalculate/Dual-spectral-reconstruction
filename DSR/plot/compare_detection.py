#!/usr/bin/env python
import numpy as np
from matplotlib import pyplot as plt
import h5py

experiment_nr = 1

simulation_file = '../data/detection/2020-11-05_162057.h5'
time_scale = 2.057e-11
voltage_scale = 5.8
steps = 2e6
offset = -2.5e-8


# Get the experimental data file
experiment_file = '../experimental-data/dark-count-pulse/C2k11-26-darkcountpulse-noavg-9uA{}.txt'.format(
    str(experiment_nr).zfill(5)
)

# Load the data with numpy
experiment_data = np.genfromtxt(experiment_file, delimiter='\t', skip_header=6)[:, 3:5]

plt.plot(experiment_data[:, 0], experiment_data[:, 1])

# Plot the simulation data
with h5py.File(simulation_file, 'r') as data:
    voltage = np.array(data['voltage'][:])[0:int(steps)] * voltage_scale
    time = np.array(data['time'][:])[0:int(steps)] * time_scale + offset

plt.plot(time, voltage)
plt.xlabel('Time [s]')
plt.ylabel('Voltage $V / R I_c$')
plt.show()
