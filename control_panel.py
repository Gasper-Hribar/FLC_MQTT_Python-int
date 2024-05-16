#!/usr/local/lib/python3.11

"""
Graphical user interface for FLC Interface communicator for Raspberry Pi using ethernet connection
and MQTT message transfering protocol. 
"""

import yaml
import time
import os
from os.path import dirname, abspath
from sys import platform
import numpy as np
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mbox
import customtkinter as ctk
import paho.mqtt.client as mqtt_client
import FLC_command


#
#  GLOBAL VARIABLES
#

""" General constants """

# get path to the directory
file_directory = dirname(abspath(__file__))
os.chdir(file_directory)

if platform == 'linux':    
    # import netifaces as ni
    if os.environ.get('DISPLAY','') == '':
        os.environ.__setitem__('DISPLAY', ':0.0')  # sets display environment variable to 0.0

PROCESS_PASSED = 0
PROCESS_FAILED = -1
    
""" FLC interface related constants """

ports={}
start_time = time.time()
alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P']
chipnames = {'mcp': 0, 'ADD1': 2, 'ADD3': 4, 'ADD4': 5}
ADDresolution = 4095
ADCresolution = 65535

read_values_keys = ['ADC0R', 'ADD1R', 'ADD3R', 'ADD4R', 'MCP0S', 'ADD1D', 'ADD3D', 'ADD4D']

zero_values = {'ADC0R':[0 ,0, 0, 0, 0, 0, 0, 0],
                'ADD1R':[0 ,0, 0, 0, 0, 0, 0, 0],
                'ADD3R':[0 ,0, 0, 0, 0, 0, 0, 0], 
                'ADD4R':[0 ,0, 0, 0, 0, 0, 0, 0], 
                'MCP0S':0, 
                'ADD1D':0, 
                'ADD3D':0, 
                'ADD4D':0}

""" MQTT related constants"""

# broker = '192.168.1.1'
# broker_port = 1883
# topic = "+"
# client_id = "IDpython"

# if platform == "linux":
#     client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION2, client_id)
# else:
#     client = mqtt_client.Client(client_id)

#
# APPLICATON 
#

# def connect_to_broker(client: mqtt_client):
   
#     if platform == 'linux':
#         ni.ifaddresses('eth0')
#         ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
#         print(ip)
#         if ip == broker:
#             try: 
#                 client.connect(broker, broker_port)
#                 print("Connected to broker.")
#                 return 0
#             except:
#                 os.system('mosquitto -c /etc/mosquitto/conf.d/mosquitto.conf')
#                 client.connect(broker, broker_port)
#                 return 0
    
#     else: 
#         try:
#             client.connect(broker, broker_port)
#             return PROCESS_PASSED
#         except:
#             return PROCESS_FAILED

#     return 0


# def subscribe(client: mqtt_client, topic='+'):
#     def on_message(client, userdata, msg):
#         # print("In on_message")
#         if msg.topic == "ID1pub":
#             # print("On message.")
#             result = FLC_command.on_message_to_pub(client=client, userdata=userdata, message=msg)
#             if not result == None:
#                 print(result)
#         elif msg.topic == "debug":
#             try:
#                 print(f'Debug message: {msg.payload.decode()}')
#             except:
#                 print(f"Error: Message payload cannot be decoded. [ {msg.payload} ]")
               

#     client.subscribe(topic)
#     client.on_message = on_message
#     return


def get_gain(ltc_range):
    gainV = 0
    if ltc_range == -5:
        gainV = 0
    elif ltc_range == -10:
        gainV = 1
    elif ltc_range == 5:
        gainV = 2
    elif ltc_range == 10:
        gainV = 3
    else:
        print("gainError")
    return gainV


def sort_read_values(data):
    """ Deprecated. Arduino based function. """
    data2 = data[0].decode('utf-8')
    data3 = data2[1:]
    data4 = [s for s in data3.split(',')]
    returnVal = [int(i) for i in data4 if i != '\r\n']
    return returnVal

def convert_read_val(readList):
    """ Deprecated. Arduino based function. """
    list3 = []
    readList2 = [bin(a) for a in readList]
    readVals = [0,0,0,0,0,0,0,0]
    for a in readList2:
        a0 = a[2:]
        while len(a0) <= 15:
            a0 = '0' + a0
        if len(a0) == 16:
            a0 = '0b' + a0
        list3.append(a0)
    for el in list3:
        if el != '0b0000000000000000':
            channelN = int(el[3:6], 2)
            readData = int(el[6:], 2)
            readVals[channelN] = readData
        else:
            pass
    return readVals


def read_fun(flc, adc_range, port_settings):
    gain = get_gain(adc_range['LTC'])
    readData, flag = flc.read_all(port_settings.portN, gain)
    # print(f"read fun - read data: {readData}")
    if flag != PROCESS_FAILED:
        return readData
    else:
        print("Process FAILED: read_fun().")
        # print(readData, "\n")
        return zero_values

class ColorButton(ctk.CTkButton):
    def __init__(self, parent, flc, port_settings, channelN, chipname, init_value, activeLow, text, column=0, row=0, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.flc = flc
        self.port_settings = port_settings
        self.init_value = init_value
        self.activeLow = activeLow
        self.chipname = chipname
        self.channelN = channelN
        self.cbutton = ctk.CTkButton(parent, text=text, text_color='black', bg_color='transparent', fg_color='white', hover_color=None, border_color='black', command=self.press)
        self.cbutton.grid(column=column, row=row, padx=5, pady=5)
        self.init_status()
        
    def init_status(self):
        if self.activeLow == 0:
            if self.init_value == 1:
                self.pressed = True
                self.cbutton.configure(fg_color='red')
            else:
                self.pressed = False
                self.cbutton.configure(fg_color='white')
            self.init_value = not self.init_value
            self.pressed = not self.pressed
        else:
            if self.init_value == 1:
                self.pressed = True
                self.cbutton.configure(fg_color='red')
            else:
                self.pressed = False
                self.cbutton.configure(fg_color='white')
            # self.init_value = not self.init_value
            # self.pressed = not self.pressed

    def press(self, *args):
        if self.activeLow == 0:
            if self.pressed and self.init_value == 1:
                self.cbutton.configure(fg_color='red')
                self.DIGwrite(onOff=True)
            else:
                self.cbutton.configure(fg_color='white')
                self.DIGwrite(onOff=False)
            self.init_value = not self.init_value
            self.pressed = not self.pressed

        else:
            if self.pressed and self.init_value == 0:
                self.cbutton.configure(fg_color='white')
                self.DIGwrite(onOff=True)
            elif self.pressed and self.init_value == 1:
                self.cbutton.configure(fg_color='white')
                self.DIGwrite(onOff=True)
            else:
                self.cbutton.configure(fg_color='red')
                self.DIGwrite(onOff=False)
            self.pressed = not self.pressed
        
    def DIGwrite(self, onOff):
        if onOff:
            self.flc.write_digital(self.port_settings.portN, chipnames[self.chipname], alphabet[self.channelN], val=1)
        else:
            self.flc.write_digital(self.port_settings.portN, chipnames[self.chipname], alphabet[self.channelN], val=0)


class SwitchButton(ctk.CTkRadioButton):

    def __init__(self, parent, flc, adc_range, port_settings, read_func, channelN, chipname, text, activeLow, column=0, row=0, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.flc = flc
        self.adc_range = adc_range
        self.port_settings = port_settings
        self.activeLow = activeLow
        self.channelN = channelN
        self.chipname = chipname
        self.text = text
        self.column = column
        self.row = row
        self.init_read = read_func
        self.onOff = ctk.BooleanVar(parent)
        self.button = ctk.CTkRadioButton(parent, text=self.text, hover=False, state='readonly', variable=self.onOff)
        self.button.grid(column=column, row=row, padx=5, pady=5)
        self.update_status()

    def digRead(self, *args):
        if args == ():
            readData = self.init_read
            if readData != PROCESS_FAILED:
                ADC_read, ADD1_read2, ADD3_read2, ADD4_read2, MCPdig, ADD1dig, ADD3dig, ADD4dig = [readData[key] for key in read_values_keys]
                # print(readData)
        else:
            MCPdig, ADD1dig, ADD3dig, ADD4dig = args
        if self.chipname == 'mcp':
            rData = sortDIGvals(MCPdig, 'mcp')
        elif self.chipname == 'ADD1':
            rData = sortDIGvals(ADD1dig, 'add')
        elif self.chipname == 'ADD3':
            rData = sortDIGvals(ADD3dig, 'add')
        elif self.chipname == 'ADD4':
            rData = sortDIGvals(ADD4dig, 'add')
        else:
            print('ERROR')
        return rData

    def update_status(self, *args):
        digVals = self.digRead(*args)
        # print(digVals)
        if digVals[self.channelN] == 1:
            self.button.configure(border_color='red')
            self.onOff.set(value=True)
        else:
            self.onOff.set(value=False)
            self.button.configure(fg_color='white')
            self.button.configure(hover_color='black')
        if self.channelN == 4 or self.channelN == 5:
            # print(digVals[self.channelN])
            pass


class LabelEntry:
    
    def __init__(self, parent, flc, adc_range, read_func, port_settings, channelN, chipname, label, k, c, isExp, t0, b, init_value, unit, column=0, row=0):
        self.flc = flc
        self.adc_range = adc_range
        self.port_settings = port_settings
        self.channelN = channelN
        self.chipname = chipname
        self.unit = unit
        self.k = k
        self.c = c
        self.isExp = isExp
        self.t0 = t0
        self.b = b
        self.init_read=read_func
        self.init_value = init_value
        self.frame = ctk.CTkFrame(parent)
        self.frame.grid(column=column, row=row, padx=5, pady=5)
        var = ctk.StringVar(self.frame, value=f'{self.convert_voltage()} {self.unit}')
        self.label = ctk.CTkLabel(self.frame, text=label).grid(column=0, row=0, padx=(0, 65))
        self.entry = ctk.CTkEntry(self.frame, fg_color='white', textvariable=var, text_color='black', width=80, state='readonly').grid(column=0, row=0, padx=(130, 0))
        self.var = var

    def update(self,*args):
        newVal = f'{self.convert_voltage(*args)} {self.unit}'
        self.var.set(newVal)

    def read(self, *args):
        if args == ():
            readData = self.init_read
            # print(f"read data: {readData}")
            if readData != PROCESS_FAILED:
                ADC_read, ADD1_read, ADD3_read, ADD4_read, MCPdig, ADD1dig, ADD3dig, ADD4dig = [readData[key] for key in read_values_keys]
        else:
            ADC_read, ADD1_read, ADD3_read, ADD4_read = args
        if self.chipname == 'adc':
            readData = ADC_read
        elif self.chipname == 'ADD1':
            readData = ADD1_read
        elif self.chipname == 'ADD3':
            readData = ADD3_read
        elif self.chipname == 'ADD4':
            readData = ADD4_read
        else:
            print("ERROR!")
        return readData[self.channelN]


    def convert_voltage(self, *args):
        var = tk.IntVar()
        to_convert = self.read(*args)
        if self.chipname == 'adc':
            if self.adc_range['LTC'] == 5 or self.adc_range['LTC'] == 10:
                # print("readVal", to_convert)
                voltage = (to_convert/ADCresolution)*self.adc_range['LTC'] # Equation for voltage range from 0 to 5V and 0 to 10V
            elif to_convert > ADCresolution/2:
                voltage = (to_convert-ADCresolution)/ADCresolution*abs(self.adc_range['LTC'])*2 # Equation for voltage range from -5 to 5V and -10 to 10V -> positive voltage
            else:
                voltage = to_convert/ADCresolution*abs(self.adc_range['LTC'])*2 # Equation for voltage range from -5 to 5V and -10 to 10V -> negative voltage
        else:
            if self.adc_range[self.chipname] == 5 or self.adc_range[self.chipname] == 10:
                voltage = (to_convert/ADDresolution)*self.adc_range[self.chipname]
            elif to_convert > ADDresolution/2:
                voltage = (to_convert-ADDresolution)/ADDresolution*abs(self.adc_range[self.chipname])*2
            else:
                voltage = to_convert/ADDresolution*abs(self.adc_range[self.chipname])*2

        if not self.isExp:
            readValue = voltage*self.k + self.c
        else:
            if voltage < 0.05: voltage = 0.05
            readValue = (1/self.t0 + 1/self.b * np.log(voltage/(5-voltage)))**(-1) - 273.15

        var = '{:.3f}'.format(readValue)
        return var

class Widget1:

    def __init__(self, parent, flc, initVals, dac_range, minValue, maxValue, port_settings, channelN, chipname, label, k, c, init_value, unit, column=0, row=0, values=[0.01, 0.1, 1]):
        self.flc = flc
        self.initVals = initVals
        self.dac_range = dac_range
        self.minValue = minValue
        self.maxValue = maxValue
        self.port_settings = port_settings
        self.frame = ctk.CTkFrame(parent)
        self.frame.grid(column=column, row=row, rowspan=2, padx=5, pady=5)
        self.chipname = chipname
        self.channelN = channelN
        self.unit = unit
        self.k = k
        self.c = c
        self.init_value = init_value
        row1 = row + 1
        self.var1 = 0.
        self.writeVal = ctk.StringVar(self.frame, value=f'0.000 {self.unit}')
        self.values = [str(a) for a in values]
        self.noStepSelected = True
        self.checkboxVal = ctk.BooleanVar(self.frame, value=True)
        self.increment = ctk.DoubleVar(self.frame, value=1)
        self.increment.set(1.0)
        # self.optionmenu_var = ctk.StringVar(value=f"{self.increment.get()}")

        self.label1 = ctk.CTkLabel(self.frame, text=label).grid(column=0, row=0, padx=(0,170)) # padx=(0,170) for full text display

        self.button1 = ctk.CTkButton(self.frame, width=40, border_width=2, fg_color=None, command=self.increase, text='>')
        self.button1.grid(column=0, row=0, padx=(200,0))

        self.button2 = ctk.CTkButton(self.frame, width=40, border_width=2, fg_color=None, command=self.decrease, text='<')
        self.button2.grid(column=0, row=0, padx=(0,30))

        self.entry = ctk.CTkEntry(self.frame, width=70, fg_color='white', state='readonly', text_color='black', textvariable=self.writeVal)
        self.entry.grid(column = 0, row = 0, padx=(100,14.495))

        self.checkbutton = ctk.CTkCheckBox(self.frame, variable=self.checkboxVal, command=self.checkbox, text="")
        self.checkbutton.grid(column=0, row=1, padx=(0,35))
        
        self.label2 = ctk.CTkLabel(self.frame, width=30, text='Step')
        self.label2.grid(column=0, row=1, padx=(60,0))

        self.button_step = ctk.CTkButton(self.frame, width=10, border_width=2, fg_color=None, command=self.open_selection_window, text=f"{self.increment.get():.3f}")
        self.button_step.grid(column=0, row=1, padx=(200,0))

        # self.combobox = ctk.CTkComboBox(self.frame, width=70, variable = self.increment, command=self.config_increment, values=self.values)
        # self.combobox['width'] = 6
        # self.combobox.grid(column=0, row=1, padx=(170,0))


        self.initialize()

    def open_selection_window(self):
    # Create a top-level window
        top = tk.Toplevel(self.frame)
        top.title("Select a Value")

        # Function to update increment and close the window
        def set_increment(value):
            self.increment.set(value)
            self.button_step.configure(text=f"{self.increment.get():.3f}")
            top.destroy()

        # Define buttons and their positions
        values = [(10, 0, 0), (1, 0, 1), (0.1, 0, 2), 
              (0.01, 1, 0), (0.001, 1, 1)]
        for value, row, col in values:
            ctk.CTkButton(top, text=str(value), command=lambda v=value: set_increment(v)).grid(row=row, column=col, padx=5, pady=5)

        # Empty space in the grid to balance the layout
        tk.Label(top, text="").grid(row=1, column=2)  # Empty label to fill the grid for symmetry


    def initialize(self):
        data_to_display = 0
        if self.chipname == 'ADD1':
            data_to_display = self.initVals.add1_init_values[self.channelN]
        elif self.chipname == 'ADD3':
            data_to_display = self.initVals.add3_init_values[self.channelN]
        elif self.chipname == 'ADD4':
            data_to_display = self.initVals.add4_init_values[self.channelN]
        else:
            print('WrongChipError')
        initwrite = '{:.3f}'.format(data_to_display)
        self.var1 = data_to_display
        data_to_display = f'{initwrite} {self.unit}'
        self.writeVal.set(data_to_display)
        
    def checkbox(self):
        if self.checkboxVal.get():
            self.combobox.configure(state=tk.NORMAL)
            self.entry.configure(state='readonly', fg_color='white')
            self.button1.configure(state=tk.NORMAL)
            self.button2.configure(state=tk.NORMAL)
            self.var1 = 0
        else:
            self.combobox.configure(state=tk.DISABLED)
            self.entry.configure(state=tk.DISABLED, fg_color='grey')
            self.button1.configure(state=tk.DISABLED)
            self.button2.configure(state=tk.DISABLED)
            self.writeVal.set(f'0.000 {self.unit}')
            self.flc.write_dac(0, chipnames[self.chipname], self.channelN, 0)

    def increase(self):
        if self.noStepSelected:
            self.var1 += self.increment.get()
        else:
            self.var1 += self.increment.get()


        if self.var1 > self.dac_range[self.chipname]:
            self.var1 = 5.000
        to_display = '{:.3f}'.format(self.var1)
        self.write_value(float(to_display))
        self.writeVal.set(f'{to_display} {self.unit}')
            # print(self.var1)

    def decrease(self):
        if self.noStepSelected:
            self.var1 -= self.increment.get()
            
            # print(self.var1)
        else:
            self.var1 -= self.increment.get()

        if self.var1 < 0:
            self.var1 = 0
        to_display = '{:.3f}'.format(self.var1)
        self.write_value(float(to_display))
        self.writeVal.set(f'{to_display} {self.unit}')
            # print(self.var1)

    def select_increment_callback(self, event):
        self.noStepSelected = False
        self.increment.set(float(self.combobox.get()))
        # self.combobox.set(f"{self.increment.get()}")
        print("Increment:", self.increment.get())


    def convert_voltage(self, voltage):
        self.init_value = self.k * voltage + self.c
        convertedVal = round((self.init_value/self.dac_range[self.chipname])*ADDresolution)
        if convertedVal > ADDresolution:
            convertedVal = ADDresolution
        return convertedVal

    def write_value(self, getVal):
        writeVal = self.convert_voltage(getVal)
        self.flc.write_dac(self.port_settings.portN, chipnames[self.chipname], alphabet[self.channelN], writeVal)
 

def sortDIGvals(val, chiptype):
    listDIG = []
    bin0 = bin(val)
    bin1 = bin0[2:]
    # print(f'bin1: {bin1}')
    for val in bin1[::-1]:
        listDIG.append(int(val))
    if chiptype == 'mcp':
        # print(bin0)
        while len(listDIG) < 16:
            listDIG.append(0)
    elif chiptype == 'add':
        while len(listDIG) < 8:
            listDIG.append(0)
    else:
        print('Wrong chiptype')
    # print(listDIG)
    return listDIG


class port():

    def __init__(self, parent, portnum, excel_address, xplus, *args, **kwargs):

        self.serial_settings = FLC_command.SerialSettings()
        
        self.portnum = portnum
        self.excel_address = excel_address
        self.parent = parent
        self.xplus = xplus
        self.readingBoxes = []
        self.digitalButtons = []
        self.xpluslist = []
        self.ypluslist = []
        self.dac_range, self.adc_range = FLC_command.collect_range_data(excel_address)
        self.port_settings = FLC_command.PortSetting(portN=portnum)
        self.port_settings.updateChipSettings(excel_address)
        self.initVals = FLC_command.PortInit()
        self.initVals.updateChipInitial(excel_address)
        self.flc = FLC_command.FLC_interface(serial_settings=self.serial_settings, settings=[self.port_settings], initVals=[self.initVals])
        self.flc.initialize_ADDrange(excel_address)
        self.flc.initialize_ports(excel_address)
        self.read_func = read_fun(self.flc, self.adc_range, self.port_settings)
        self.create_window()
        
        
    def create_window(self):
        mcp, add1, add3, add4, adc, pwr = FLC_command.readExcel(self.excel_address)
        add1_settings = FLC_command.collect_chip_data(add1)
        add3_settings = FLC_command.collect_chip_data(add3)
        add4_settings = FLC_command.collect_chip_data(add4)
        mcp_settings = FLC_command.collect_chip_data(mcp)
        adc_settings = FLC_command.collect_chip_data(adc)
        label = ctk.CTkLabel(self.parent, text=f'{ports[self.portnum]}')
        label.grid(column=1+self.xplus, row=0)
        self.control_panel(self.parent, add1_settings, 'ADD1', self.xplus)
        self.control_panel(self.parent, add3_settings, 'ADD3', self.xplus)
        self.control_panel(self.parent, add4_settings, 'ADD4', self.xplus)
        self.control_panel(self.parent, mcp_settings, 'mcp', self.xplus)
        self.control_panel(self.parent, adc_settings, 'adc', self.xplus)
        self.parent.after(500, self.update_fun)

    def control_panel(self, frame, chip, chipname, xplus):
        
        for channel in chip:
            channel.coordY += 1
            self.xpluslist.append(channel.coordX)
            self.ypluslist.append(channel.coordY)
            index = chip.index(channel)
            if not channel.hidden:
                if channel.function == 'DAC':
                    Widget1(frame, flc=self.flc, initVals=self.initVals, dac_range=self.dac_range, minValue=channel.minValues, maxValue=channel.maxValues, port_settings=self.port_settings, channelN=index, chipname=chipname, label=channel.name, k=channel.k, c=channel.constant, init_value=channel.initValues, unit=channel.unit, column=channel.coordX+xplus, row=channel.coordY)
                   
                elif channel.function == 'ADC':
                    readingBox = LabelEntry(frame, self.flc, self.adc_range, self.read_func, self.port_settings, channelN = index, chipname=chipname, label=channel.name, k=channel.k, c=channel.constant, isExp=channel.isExp, t0=channel.t0, b=channel.B, init_value=channel.initValues, unit=channel.unit, column=channel.coordX+xplus, row=channel.coordY)
                    
                    self.readingBoxes.append(readingBox)
                elif channel.function == 'DIG_IN':
                    digitalButton = SwitchButton(frame, self.flc, self.adc_range, self.port_settings, self.read_func, channelN=index, chipname=chipname, text=channel.name, activeLow = channel.activeLow, column=channel.coordX+xplus, row=channel.coordY)
                    
                    self.digitalButtons.append(digitalButton)
                elif channel.function == 'DIG_OUT':
                    ColorButton(frame, self.flc, self.port_settings, channelN=index, chipname=chipname, init_value=channel.initValues, activeLow=channel.activeLow, text=channel.name, column=channel.coordX+xplus, row=channel.coordY)
                   
                elif channel.function == 'PWR':
                    pass
                else:
                    print('Unknown function')
    
    def update_fun(self):
        readData = read_fun(self.flc, self.adc_range, self.port_settings)
        if readData != PROCESS_FAILED:
            ADC_read, ADD1_read, ADD3_read, ADD4_read, MCPdig, ADD1dig, ADD3dig, ADD4dig = [readData[key] for key in read_values_keys]
            print('ADD4read:', ADD4_read)
            print('ADD4dig:', ADD4dig)
        for box in self.readingBoxes:
            box.update(ADC_read, ADD1_read, ADD3_read, ADD4_read)
            
        for digitalButton in self.digitalButtons:
            digitalButton.update_status(MCPdig, ADD1dig, ADD3dig, ADD4dig)

        if True:
            self.parent.after(300, self.update_fun)
            
    def getXplus(self):
        return max(self.xpluslist)

    def getYplus(self):
        return max(self.ypluslist)

def scrollfunc(height, width):
    canvas.configure(scrollregion=canvas.bbox("all"),width=width,height=height)

if __name__ == '__main__':

    if FLC_command.connect_to_broker(FLC_command.client) == PROCESS_PASSED:
        FLC_command.client.publish('test', "Raspberry Pi is alive.", qos=0)
        FLC_command.client.publish('data',  'INIT', qos=0)
        FLC_command.subscribe(FLC_command.client)
        FLC_command.client.loop_start()
    
    root = ctk.CTk()
    root.grid_rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    topFrame = ctk.CTkFrame(root)
    topFrame.grid(column=0,row=0, sticky='nw')
    topFrame.grid_rowconfigure(0, weight=1)
    topFrame.grid_columnconfigure(0, weight=1)

    canvas = ctk.CTkCanvas(topFrame)
    
    canvas.grid(column=0,row=0, sticky='news')

    scrollbar=ctk.CTkScrollbar(topFrame, command=canvas.yview)
    scrollbar.grid(column=1, row=0, sticky='ns')
    canvas.configure(yscrollcommand=scrollbar.set)

    widget_frame = ctk.CTkFrame(canvas)
    canvas.create_window((0,0), window=widget_frame, anchor='nw')
        
    root.title('FLC controller')
    xstep = 0

    with open("port_settings.yaml", "r") as file:
        ymldata = yaml.load(file, Loader=yaml.FullLoader)
    for key, value in ymldata.items():
        if key.startswith('port'):
            ports[int(key[4])] = value
        else:
            darkmode = value
            if darkmode:
                ctk.set_appearance_mode("Dark")
    
    for portnum, excel_address in ports.items():
        win = port(widget_frame, portnum, excel_address, xstep)
        xplus = win.getXplus()
        xstep += xplus

    widget_frame.update_idletasks()
    width = widget_frame.winfo_width()
    height = widget_frame.winfo_height()
    canvas.configure(width=width, height=height)

    if platform == 'win32':
        root.geometry(f'{width+scrollbar.winfo_width()}x{height}')
    elif platform == 'linux':
        root.geometry(f'770x450') # for 7" raspberry touchscreen

    topFrame.bind("<Configure>", scrollfunc(height, width))
    widths = []

    for i in widget_frame.winfo_children():
        widths.append(i)
    root.mainloop()
