from functools import partial
import tkinter as tk
import customtkinter as ctk
from tkinter.ttk import Combobox
import FLC_command

root = tk.Tk()
frame = tk.Frame(root)
frame.grid()
root.title('ADD_adapter_test-port0')

alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P']
chipnames = {'mcp': 0, 'ADD1': 2, 'ADD3': 4, 'ADD4': 5}
ADDresolution = 4095
ADCresolution = 65535

dac_range, adc_range = FLC_command.collect_range_data()
serial_settings = FLC_command.SerialSettings(port="COM15")
port_settings = FLC_command.PortSetting(portN=0)
port_settings.updateChipSettings()
initVals = FLC_command.PortInit()
initVals.updateChipInitial()
flc1 = FLC_command.FLC_interface(serial_settings=serial_settings, settings=[port_settings], initVals=[initVals])


class Widget1:

    def __init__(self, parent, channelN, chipname, label, k, c, init_value, unit, column=0, row=0, start=0, stop=100, values=[0.01, 0.1, 1, 10]):
        self.chipname = chipname
        self.channelN = channelN
        self.k = k
        self.c = c
        self.init_value = init_value
        row1 = row + 1
        var1 = tk.IntVar(value=1)
        self.label1 = tk.Label(parent, text=label).grid(column=column, row=row, padx=(0,20))
        self.label2 = tk.Label(parent, text=unit).grid(column=column, row=row, padx=(170,20))
        self.label3 = tk.Label(parent, text='Step').grid(column=column, row=row1)

        self.spinbox = tk.Spinbox(parent)
        self.spinbox.grid(column=column, row=row, padx=(100,10))
        self.spinbox['from_'] = start
        self.spinbox['to'] = stop
        self.spinbox['width'] = 6
        self.spinbox['command'] = self.write_value
        self.spinbox['state'] = 'readonly'

        self.checkbutton = tk.Checkbutton(parent)
        self.checkbutton.grid(column=column, row=row1, padx=(0,50))
        self.checkbutton['variable'] = var1
        self.checkbutton['command'] = partial(self.update, var1)
        
        self.combobox = Combobox(parent)
        self.combobox['width'] = 6
        self.combobox['values'] = values
        self.combobox.current(2) # default value of the combobox based on the values given
        self.combobox.grid(column=column, row=row1, padx=(100,0))
        self.combobox.bind('<<ComboboxSelected>>', self.config_increment)

    def update(self, var):
        state = var.get()
        if state == 1:
            self.combobox.configure(state='readonly')
            self.spinbox.configure(state = 'readonly')
            self.spinbox.configure(increment = self.combobox.get())
        else:
            self.combobox.configure(state='disabled')
            # self.spinbox.configure(increment = 0)
            self.spinbox.configure(state = 'disabled')
            flc1.write_dac(0, chipnames[self.chipname], self.channelN, 0)

    def config_increment(self, event):
        self.spinbox.configure(increment = self.combobox.get())

    def convert_voltage(self, voltage):
        self.init_value = self.k * voltage + self.c
        convertedVal = round((self.init_value/dac_range[self.chipname])*ADDresolution)
        return convertedVal
    def write_value(self):
        getVal = float(self.spinbox.get())
        writeVal = self.convert_voltage(getVal)
        flc1.write_dac(port_settings.portN, chipnames[self.chipname], alphabet[self.channelN], writeVal)

