import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import main  # Ensure this module contains the necessary signal processing functions
import os

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Signal Generator")

        # Initialize the figure for plotting
        self.fig = plt.Figure(figsize=(8, 12), dpi=100)
        self.canvas_plot = FigureCanvasTkAgg(self.fig, master=self.create_plot_area())
        self.create_widgets()

    def create_plot_area(self):
        frame = tk.Frame(self.root)
        frame.grid(row=9, column=0, columnspan=2)

        canvas = tk.Canvas(frame, width=800, height=600)
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.canvas_plot.get_tk_widget().pack()
        return scrollable_frame

    def create_widgets(self):
        # Signal Generation Section
        frame_generate = tk.LabelFrame(self.root, text="Generate Signal", padx=10, pady=10)
        frame_generate.grid(row=0, column=0, padx=10, pady=10)

        self.create_signal_generation_widgets(frame_generate)
        self.create_signal_comparison_widgets()
        self.create_signal_operations_widgets()

    def create_signal_generation_widgets(self, frame):
        tk.Label(frame, text="File Name:").grid(row=0, column=0)
        self.main.entry_file_name = tk.Entry(frame)
        self.main.entry_file_name.grid(row=0, column=1)
        tk.Button(frame, text="Save As", command=lambda: self.select_save_location(self.entry_file_name)).grid(row=0,
                                                                                                               column=2)

        tk.Label(frame, text="Signal Type (sin/cos):").grid(row=1, column=0)
        self.main.entry_type_signal = tk.Entry(frame)
        self.main.entry_type_signal.grid(row=1, column=1)

        tk.Label(frame, text="Analog Frequency:").grid(row=2, column=0)
        self.main.entry_analog_frequency = tk.Entry(frame)
        self.main.entry_analog_frequency.grid(row=2, column=1)

        tk.Label(frame, text="Sampling Frequency:").grid(row=3, column=0)
        self.main.entry_sampling_frequency = tk.Entry(frame)
        self.main.entry_sampling_frequency.grid(row=3, column=1)

        tk.Label(frame, text="Phase Shift:").grid(row=4, column=0)
        self.main.entry_phase_shift = tk.Entry(frame)
        self.main.entry_phase_shift.grid(row=4, column=1)

        tk.Label(frame, text="Amplitude:").grid(row=5, column=0)
        self.main.entry_amplitude = tk.Entry(frame)
        self.main.entry_amplitude.grid(row=5, column=1)

        tk.Button(frame, text="Generate Signal", command=self.generate_signal).grid(row=6, columnspan=3)

    def create_signal_comparison_widgets(self):
        frame_compare = tk.LabelFrame(self.root, text="Compare Signals", padx=10, pady=10)
        frame_compare.grid(row=1, column=0, padx=10, pady=10)

        tk.Label(frame_compare, text="Generated Signal File:").grid(row=0, column=0)
        self.main.entry_compare_file = tk.Entry(frame_compare)
        self.main.entry_compare_file.grid(row=0, column=1)
        tk.Button(frame_compare, text="Select File", command=lambda: self.select_file(self.main.entry_compare_file)).grid(
            row=0, column=2)

        tk.Button(frame_compare, text="Compare Signals", command=self.main.compare_signals).grid(row=1, columnspan=3)

    def create_signal_operations_widgets(self):
        frame_operations = tk.LabelFrame(self.root, text="Signal Operations", padx=10, pady=10)
        frame_operations.grid(row=2, column=0, padx=10, pady=10)

        tk.Label(frame_operations, text="Signal 1:").grid(row=0, column=0)
        self.main.entry_signal1 = tk.Entry(frame_operations)
        self.entry_signal1.grid(row=0, column=1)
        tk.Button(frame_operations, text="Select File", command=lambda: self.select_file(self.main.entry_signal1)).grid(
            row=0, column=2)

        tk.Label(frame_operations, text="Signal 2 (Optional):").grid(row=1, column=0)
        self.main.entry_signal2 = tk.Entry(frame_operations)
        self.main.entry_signal2.grid(row=1, column=1)
        tk.Button(frame_operations, text="Select File", command=lambda: self.select_file(self.main.entry_signal2)).grid(
            row=1, column=2)

        tk.Label(frame_operations, text="Operation:").grid(row=2, column=0)
        self.main.entry_operation = ttk.Combobox(frame_operations,
                                            values=['add', 'subtract', 'multiply', 'square', 'normalize', 'accumulate'])
        self.entry_operation.grid(row=2, column=1)
        self.entry_operation.bind("<<ComboboxSelected>>", self.update_operation_fields)

        self.label_constant = tk.Label(frame_operations, text="Constant (for multiply):")
        self.entry_constant = tk.Entry(frame_operations)

        self.label_normalize_range = tk.Label(frame_operations, text="Normalize Range (-1 to 1 or 0 to 1):")
        self.entry_normalize_range = tk.Entry(frame_operations)

        tk.Button(frame_operations, text="Perform Operations", command=self.perform_operations).grid(row=5,
                                                                                                     columnspan=3)

    def select_file(self, entry_widget):
        file_path = filedialog.askopenfilename()
        if file_path:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, file_path)

    def select_save_location(self, entry_widget):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, file_path)

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
                main.add_two_signals(file1, file2, file_name)
            elif operation == 'subtract':
                main.subtract_two_signals(file1, file2, file_name)
            elif operation == 'multiply':
                constant = float(self.entry_constant.get())
                main.multiply_signal(file1, constant, file_name)
            elif operation == 'square':
                main.square_signal(file1, file_name)
            elif operation == 'normalize':
                normalize_range = self.entry_normalize_range.get().strip()
                main.normalize_signal(file1, file_name, normalize_range)
            elif operation == 'accumulate':
                main.accumulate_signal(file1, file_name)

            data = main.read_file(file_name + ".txt")
            self.plot_two_signals(data)

        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def generate_signal(self):
        try:
            file_name = self.main.entry_file_name.get().strip()
            type_signal = self.main.entry_type_signal.get().strip().lower()
            analog_frequency = int(self.main.entry_analog_frequency.get())
            sampling_freq = int(self.main.entry_sampling_frequency.get())
            phase_shift = float(self.main.entry_phase_shift.get())
            A = float(self.main.entry_amplitude.get())

            if not file_name:
                messagebox.showerror("Input Error", "File name cannot be empty.")
                return
            if type_signal not in ['sin', 'cos']:
                messagebox.showerror("Input Error", "Signal type must be 'sin' or 'cos'.")
                return

            if os.path.exists(file_name + ".txt"):
                data = main.read_file(file_name + ".txt")
                self.plot_two_signals(data)
                return

            main.create_file(file_name, sampling_freq, phase_shift, A, type_signal, analog_frequency)

            data = main.read_file(file_name + ".txt")
            self.plot_file_discrete(data)
            self.plot_continuous_data(analog_frequency, A, sampling_freq, phase_shift, type_signal)

        except ValueError as ve:
            messagebox.showerror("Input Error", f"Invalid input: {ve}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def plot_two_signals(self, data):
        self.plot_file_exists_discrete(data)
        self.plot_file_exists_connected(data)

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
        if type_signal == 'sin':
            y = A * np.sin(2 * np.pi * Analog_freq * time + phase_shift)
        else:
            y = A * np.cos(2 * np.pi * Analog_freq * time + phase_shift)

        ax2 = self.fig.add_subplot(212)
        ax2.plot(time, y,
                 label=r'$y = A \cdot \sin(2\pi f x + \theta)$' if type_signal == 'sin' else r'$y = A \cdot \cos(2\pi f x + \theta)$',
                 color='b', linewidth=2)
        ax2.set_title('Continuous Waveform', fontsize=16)
        ax2.set_xlabel('Time (seconds)', fontsize=14)
        ax2.set_ylabel('Amplitude', fontsize=14)
        ax2.grid(True)
        ax2.legend()
        self.canvas_plot.draw()

    def plot_file_exists_discrete(self, data):
        ax1 = self.fig.add_subplot(211)
        ax1.cla()
        ax1.stem(data['index'], data['data'], linefmt='--', markerfmt='o', basefmt=' ', label='Discrete Steps')
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
        ax3.set_title('Discrete Signal connected Plot', fontsize=16)
        ax3.set_xlabel('Index', fontsize=14)
        ax3.set_ylabel('Amplitude', fontsize=14)
        ax3.grid(True)
        ax3.legend()
        self.canvas_plot.draw()

    def update_operation_fields(self, event):
        selected_operation = self.main.entry_operation.get()
        if selected_operation == 'multiply':
            self.label_constant.grid(row=3, column=0)
            self.entry_constant.grid(row=3, column=1)
            self.label_normalize_range.grid_forget()
            self.entry_normalize_range.grid_forget()
        elif selected_operation == 'normalize':
            self.label_normalize_range.grid(row=4, column=0)
            self.entry_normalize_range.grid(row=4, column=1)
            self.label_constant.grid_forget()
            self.entry_constant.grid_forget()
        else:
            self.label_constant.grid_forget()
            self.entry_constant.grid_forget()
            self.label_normalize_range.grid_forget()
            self.entry_normalize_range.grid_forget()


if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()
