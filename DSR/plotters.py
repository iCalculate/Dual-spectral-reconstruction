import h5py
import numpy as np
from matplotlib import pyplot as plt


def plot_vt(file):

    time_scale = 0.557e-11
    voltage_scale = 5.8
    offset = -5.8e-8

    experiment_nr = 1

    experiment_file = 'experimental-data/dark-count-pulse/C2k11-26-darkcountpulse-noavg-9uA{}.txt'.format(
        str(experiment_nr).zfill(5)
    )

    # Load the data with numpy
    experiment_data = np.genfromtxt(experiment_file, delimiter='\t', skip_header=6)[:, 3:5]

    with h5py.File(file, 'r') as data:
        voltage = np.array(data['voltage'][:]) * voltage_scale
        time = np.array(data['time'][:]) * time_scale + offset

    plt.plot(experiment_data[:, 0], experiment_data[:, 1])
    plt.plot(time, voltage)
    plt.xlabel('Time $t R / L_k$')
    plt.ylabel('Voltage $V / R I_c$')
    plt.show()


def plot_it(file):
    with h5py.File(file, 'r') as data:
        bias_current = np.array(data['bias_current'][:])
        time = np.array(data['time'][:])

    plt.plot(time, bias_current)
    plt.xlabel('Time $t R / L_k$')
    plt.ylabel('Bias current $I_b / I_c$')
    plt.show()


def plot_iv(file):
    with h5py.File(file, 'r') as data:
        voltage = np.array(data['voltage'][:])
        bias_current = np.array(data['bias_current'][:])

    plt.plot(bias_current, voltage)
    plt.xlabel('Bias current $I_b / I_c$')
    plt.ylabel('Voltage $V / R I_c$')
    plt.show()
