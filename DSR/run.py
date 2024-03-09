#!/usr/bin/env python3
import argparse
import json
import logging
import os
from pathlib import Path

import h5py
import numpy as np
from PyInquirer import prompt
from matplotlib import pyplot as plt

import plotters


class PlotterCli:

    def __init__(self):

        # Parse arguments
        parser = argparse.ArgumentParser(description='Plot data from simulations')
        parser.add_argument('-v', '--verbose', action='count', default=0, help='set verbose level '
                                                                               '(-v = INFO, -vv = DEBUG)')
        parser.add_argument('-l', '--logs', type=str, default='plot.log', help='set where logs should be stored')
        parser.add_argument('-i', '--input', type=str, default='data', help='directory to load data files from')
        parser.set_defaults(func=self.interactive)
        subparsers = parser.add_subparsers()

        # Compute averages and standard deviations
        average_parser = subparsers.add_parser('average', help='compare average voltage against some other parameter')
        average_parser.add_argument('-p', '--parameter', type=str, default='size', help='parameter to use in compare')
        average_parser.set_defaults(func=self.average)

        # Compare different pulses
        average_parser = subparsers.add_parser('pulse', help='compare voltage pulses against some other parameter')
        average_parser.add_argument('-p', '--parameter', type=str, default='size', help='parameter to use in compare')
        average_parser.set_defaults(func=self.pulses)

        self.args = parser.parse_args()

        # Enable logging
        self.logger = logging.getLogger('plotter-cli')
        self.logger.setLevel(logging.DEBUG if self.args.verbose >= 2 else (logging.INFO if self.args.verbose == 1
                                                                           else logging.WARN))
        file_stream = logging.FileHandler(self.args.logs)
        file_stream.setFormatter(logging.Formatter('%(asctime)-15s %(levelname)-8s %(message)s'))
        self.logger.addHandler(file_stream)

        self.args.func()

    def interactive(self):

        plot_mode = None

        # Select plot type and file
        while True:

            if plot_mode is None:
                plot_mode = self._select_plot_mode_()

            file = self._select_file_()

            if file == 'change_plot_type':
                plot_mode = None
                continue

            # Call plotter with name plot_${plot_mode}
            getattr(plotters, 'plot_{}'.format(plot_mode))(file)

    def average(self):
        files = self._get_files_()

        sorted_files = sorted(files, key=lambda x: self._parse_file_config_(x)['parameters'][self.args.parameter])

        # Get parameter values
        parameter = list(map(lambda x: self._parse_file_config_(x)['parameters'][self.args.parameter], sorted_files))

        # Get voltages
        voltages = list(map(lambda x: self._get_vector_data_(x, 'voltage'), sorted_files))

        # Get averages
        averages = np.mean(voltages, axis=1)

        # Get standard deviation
        std = np.std(voltages, axis=1)

        plt.plot(parameter, averages, '-o', label=r'$\langle V \rangle$')
        plt.plot(parameter, std, '-s', label=r'$\Delta V$')
        plt.legend()
        plt.xlabel(self.args.parameter)
        plt.ylabel('Voltage')
        plt.show()

    def pulses(self):
        files = self._get_files_()

        sorted_files = sorted(files, key=lambda x: self._parse_file_config_(x)['parameters'][self.args.parameter])

        # Get parameter values
        parameter = list(map(lambda x: self._parse_file_config_(x)['parameters'][self.args.parameter], sorted_files))

        # Get delta t
        dt = list(map(lambda x: self._parse_file_config_(x)['parameters']['dt'], sorted_files))

        # Get voltages
        voltages = list(map(lambda x: self._get_vector_data_(x, 'voltage'), sorted_files))

        rise = []

        for i in range(len(parameter)):
            time = dt[i] * np.array(range(len(voltages[i])))

            rise.append(np.argmax(voltages[i] > 5e-9) * dt[i])

            plt.plot(time, voltages[i], label='{}={}'.format(self.args.parameter, parameter[i]))

        plt.legend()
        plt.xlabel('Time')
        plt.ylabel('Voltage')
        plt.show()

    def _select_plot_mode_(self):
        question = {
            'type': 'list',
            'name': 'mode',
            'message': 'Select the plotting mode',
            'choices': [{
                'name': 'Voltage vs Time',
                'value': 'vt'
            }, {
                'name': 'Bias current vs Time',
                'value': 'it'
            }, {
                'name': 'Voltage vs Bias current',
                'value': 'iv'
            }]
        }

        result = prompt(question)

        try:
            return result['mode']
        except Exception as e:
            self.logger.error(e)
            exit(0)

    def _select_file_(self):

        files = [{
            'name': self._format_file_config_(self._parse_file_config_(file)),
            'value': file
        } for file in self._get_files_()]

        files.append({
            'name': 'Change plot type',
            'value': 'change_plot_type'
        })

        question = {
            'type': 'list',
            'name': 'file',
            'message': 'Select a file',
            'choices': files
        }

        result = prompt(question)

        try:
            return result['file']
        except Exception as e:
            self.logger.error(e)
            exit(0)

    def _get_files_(self):
        path = Path(self.args.input)

        files = sorted([os.path.join(str(path), o) for o in os.listdir(str(path))
                        if not os.path.isdir(os.path.join(str(path), o)) and o.endswith('.h5')])

        return files

    @staticmethod
    def _get_vector_data_(file, key):
        with h5py.File(file, 'r') as data:
            return data[key][:]

    @staticmethod
    def _parse_file_config_(file):
        with h5py.File(file, 'r') as data:
            json_config = data['json_config'][()]

        return json.loads(json_config)

    @staticmethod
    def _format_file_config_(config):
        initial = config['parameters']
        return 'sz={sz}, st={st}, av={av}, dt={dt}, q={q}, c0={c0}, vg={vg}, nl={nl}, ib={ib}'.format(
            sz=initial['size'],
            st=initial['maxSteps'],
            av=initial['average'],
            dt=initial['dt'],
            q=initial['q'],
            c0=initial['c0'],
            vg=initial['vg'],
            nl=initial['nl'],
            ib=initial['ib']
        )


if __name__ == '__main__':
    PlotterCli()
