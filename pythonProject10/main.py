import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import dsp_task3  # Import Task3 module


class SignalProcessor:
    def __init__(self, root):
        self.root = root
        self.root.title("Signal Generator")

        # Initialize the plotting figure
        self.fig = plt.Figure(figsize=(8, 12), dpi=100)
        self.canvas_plot = None  # Will be initialized in the plotting section

        # Initialize GUI elements
        self.init_gui()

    def init_gui(self):
        # GUI setup for signal generation, operations, and plotting
        # Add GUI components here using Tkinter widgets.
        pass  # Replace with full GUI setup, as previously shown

    def read_file(self, path):
        data1, index = [], []
        with open(path, 'r') as file:
            content = file.readlines()
            for line in content[3:]:
                idx, value = line.split()
                index.append(float(idx))
                data1.append(float(value))
        return {'index': index, 'data': data1}

    def plot_file_discrete(self, data):
        ax = self.fig.add_subplot(211)
        ax.stem(data['index'], data['data'], linefmt='--', markerfmt='o', basefmt='r-', label='Discrete Steps')
        ax.set_title('Discrete Signal Plot', fontsize=16)
        ax.set_xlabel('Index', fontsize=14)
        ax.set_ylabel('Amplitude', fontsize=14)
        ax.grid(True)
        ax.set_xlim(0, 30)
        ax.legend()
        self.canvas_plot.draw()

    def plot_continuous_data(self, Analog_freq, A, sample_freq, phase_shift, type_signal):
        time = np.linspace(0, 1, sample_freq)
        y = A * (np.sin if type_signal == 'sin' else np.cos)(2 * np.pi * Analog_freq * time + phase_shift)

        ax2 = self.fig.add_subplot(212)
        ax2.plot(time, y, label=f'$y = A \cdot {type_signal}(2\pi f x + \\theta)$', color='b', linewidth=2)
        ax2.set_title('Continuous Waveform', fontsize=16)
        ax2.set_xlabel('Time (seconds)', fontsize=14)
        ax2.set_ylabel('Amplitude', fontsize=14)
        ax2.grid(True)
        ax2.legend()
        self.canvas_plot.draw()

    def create_file(self, name, sampling_frequency, phase_shift, A, type_signal, analog_freq):
        name = name + ".txt"
        if os.path.exists(name):
            print(f"File '{name}' already exists. Aborting operation.")
            return
        if sampling_frequency < 2 * analog_freq:
            messagebox.showerror("Error", "Sample frequency is smaller than 2 * analog frequency")
            return

        with open(name, 'w') as file:
            file.write("0 \n0 \n" + str(sampling_frequency) + '\n')
            for i in range(sampling_frequency):
                value = A * (math.sin if type_signal == 'sin' else math.cos)(
                    2 * math.pi * (analog_freq / sampling_frequency) * i + phase_shift)
                file.write(f"{i} {round(value, 6)}\n")

    def read_existing_file(self, data):
        data = self.read_file(data)
        self.plot_file_exists(data)

    def plot_file_exists(self, data):
        self.fig.clf()
        ax = self.fig.add_subplot(211)
        ax.plot(data['index'], data['data'], linestyle='-', marker='o', color='b', label='Connected Points')
        ax.stem(data['index'], data['data'], linefmt='--', markerfmt='o', basefmt='r-', label='Discrete Steps')
        ax.set_title('Discrete Signal Plot', fontsize=16)
        ax.set_xlabel('Index', fontsize=14)
        ax.set_ylabel('Amplitude', fontsize=14)
        ax.grid(True)
        ax.set_xlim(0, 30)
        ax.legend()
        self.canvas_plot.draw()

    def plot_file_exists_discrete(self, data):
        ax1 = self.fig.add_subplot(211)
        ax1.cla()
        ax1.stem(data['index'], data['data'], linefmt='--', markerfmt='o', basefmt=' ')
        ax1.set_title('Discrete Signal Plot', fontsize=16)
        ax1.set_xlabel('Index', fontsize=14)
        ax1.set_ylabel('Amplitude', fontsize=14)
        ax1.set_xlim(min(data['index']), max(data['index']))
        ax1.set_ylim(min(data['data']), max(data['data']))
        ax1.grid(True)
        ax1.legend()
        self.canvas_plot.draw()

    def plot_file_exists_connected(self, data):
        ax3 = self.fig.add_subplot(212)
        ax3.plot(data['index'], data['data'], linestyle='-', marker='x', color='r', label='Connected Points')
        ax3.set_title('Discrete Signal Connected Plot', fontsize=16)
        ax3.set_xlabel('Index', fontsize=14)
        ax3.set_ylabel('Amplitude', fontsize=14)
        ax3.grid(True)
        ax3.legend()
        self.canvas_plot.draw()

    def SignalSamplesAreEqual(self, file_name, indices, samples):
        # Your comparison function implementation here
        pass

    def compare_signals(self):
        # Include the code for comparing signals here
        pass

    def perform_operations(self):
        try:
            file1 = self.entry_signal1.get().strip()
            file2 = self.entry_signal2.get().strip()
            operation = self.entry_operation.get().strip().lower()
            file_name = self.entry_file_name.get().strip()

            if not file_name:
                messagebox.showerror("Input Error", "File name cannot be empty.")
                return

            if operation == 'add':
                self.add_two_signals(file1, file2, file_name)
            elif operation == 'subtract':
                self.subtract_two_signals(file1, file2, file_name)
            elif operation == 'multiply':
                constant = float(self.entry_constant.get())
                self.multiply_signal(file1, constant, file_name)
            elif operation == 'square':
                self.square_signal(file1, file_name)
            elif operation == 'normalize':
                normalize_range = self.entry_normalize_range.get().strip()
                self.normalize_signal(file1, file_name, normalize_range)
            elif operation == 'accumulate':
                self.accumulate_signal(file1, file_name)

            # Read and plot the new file
            data = self.read_file(file_name + ".txt")
            #        print(data)  # Debugging: print the contents of the new data
            self.plot_two_signals(data)

        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def generate_signal(self):
        try:
            file_name = self.entry_file_name.get().strip()
            type_signal = self.entry_type_signal.get().strip().lower()
            analog_frequency = int(self.entry_analog_frequency.get())
            sampling_freq = int(self.entry_sampling_frequency.get())
            phase_shift = float(self.entry_phase_shift.get())
            A = float(self.entry_amplitude.get())

            if not file_name:
                messagebox.showerror("Input Error", "File name cannot be empty.")
                return
            if type_signal not in ['sin', 'cos']:
                messagebox.showerror("Input Error", "Signal type must be 'sin' or 'cos'.")
                return

            if os.path.exists(file_name + ".txt"):
                data = self.read_file(file_name + ".txt")
                self.plot_two_signals(data)
                return

            self.create_file(file_name, sampling_freq, phase_shift, A, type_signal, analog_frequency)

            data = self.read_file(file_name + ".txt")
            self.plot_file_discrete(data)
            self.plot_continuous_data(analog_frequency, A, sampling_freq, phase_shift, type_signal)

        except ValueError as ve:
            messagebox.showerror("Input Error", f"Invalid input: {ve}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
            pass

    def add_two_signals(self, file1, file2, name):
        data_file1, data_file2 = self.read_file(file1), self.read_file(file2)
        all_indices = sorted(set(data_file1['index'] + data_file2['index']))
        new_data = {'index': all_indices, 'data': []}

        value_map1 = dict(zip(data_file1['index'], data_file1['data']))
        value_map2 = dict(zip(data_file2['index'], data_file2['data']))

        for idx in all_indices:
            new_data['data'].append(value_map1.get(idx, 0) + value_map2.get(idx, 0))

        self.create_file_array_input(name, new_data['data'], new_data['index'])

    def subtract_two_signals(self, file1, file2, name):
        data_file1, data_file2 = self.read_file(file1), self.read_file(file2)
        all_indices = sorted(set(data_file1['index'] + data_file2['index']))
        new_data = {'index': all_indices, 'data': []}

        value_map1 = dict(zip(data_file1['index'], data_file1['data']))
        value_map2 = dict(zip(data_file2['index'], data_file2['data']))

        for idx in all_indices:
            new_data['data'].append(value_map2.get(idx, 0) - value_map1.get(idx, 0))

        self.create_file_array_input(name, new_data['data'], new_data['index'])

    def multiply_signal(self, file_name, constant, new_file_name):
        data = self.read_file(file_name)
        new_data = {'index': data['index'], 'data': [value * constant for value in data['data']]}
        self.create_file_array_input(new_file_name, new_data['data'], new_data['index'])

    def create_file_array_input(self, name, data, index):
        with open(f"{name}.txt", 'w') as file:
            file.writelines('0 \n0 \n' + str(9) + '\n')
            for i, idx in enumerate(index):
                file.write(f"{idx} {data[i]}\n")

    def normalize_signal(self, file_name, new_file_name, normalize_range):
        data = self.read_file(file_name)
        min_value, max_value = min(data['data']), max(data['data'])

        if normalize_range == '0 to 1':
            new_data = {'index': data['index'],
                        'data': [(value - min_value) / (max_value - min_value) for value in data['data']]}
        elif normalize_range == '-1 to 1':
            new_data = {'index': data['index'],
                        'data': [2 * ((value - min_value) / (max_value - min_value)) - 1 for value in data['data']]}

        self.create_file_array_input(new_file_name, new_data['data'], new_data['index'])

    def accumulate_signal(self, file_name, new_file_name):
        data = self.read_file(file_name)
        accumulated_data = []  # Initialize an empty list to store cumulative sums
        running_sum = 0  # Initialize running sum
        for value in data['data']:
            running_sum += value  # Add current value to the running sum
            accumulated_data.append(running_sum)  # Append the updated sum to the list
        self.create_file_array_input(new_file_name, accumulated_data, data['index'])

    def run_task3(self, number_of_bits=3):
        task3_instance = dsp_task3.Task3(number_of_bits, self)
        task3_instance.run()

    # Main code to run the GUI and SignalProcessor instance
root = tk.Tk()
app = SignalProcessor(root)
x=3
app.run_task3(x)  # Run Task3 within SignalProcessor, with the default 3 bits
root.mainloop()
