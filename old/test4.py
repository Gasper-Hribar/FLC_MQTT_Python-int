from functools import partial
import time
import FLC_command
import tkinter as tk
from tkinter.ttk import Combobox
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
print("readAll", flc1.read_all(0))
print("readMCP", flc1.read_chips(0, 0))
print("readLTC", flc1.read_chips(0, 1))
print("readADD2", flc1.read_chips(0, 2))
print("readADD4", flc1.read_chips(0, 4))
print("readADD5", flc1.read_chips(0, 5))