from argparse import ArgumentParser
from functools import partial
import time
from tracemalloc import start
import FLC_command
import tkinter as tk
from tkinter.ttk import Combobox

start_time = time.time()
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
    data2 = data[0].decode('utf-8')
    data3 = data2[1:]
    data4 = [s for s in data3.split(',')]
    returnVal = [int(i) for i in data4 if i != '\r\n']
    return returnVal

def convert_read_val(readList):
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


def read_fun():
    gain = get_gain(adc_range['LTC'])
    readData = flc1.read_all(port_settings.portN, gain)
    sorted = sort_read_values(readData)
    ADC_read = []
    ADD1_read = []
    ADD3_read = []
    ADD4_read = []
    for el in range(0, 8):
        ADC_read.append(sorted[el])
    for el in range(8, 16):
        ADD1_read.append(sorted[el])
    for el in range(16, 24):
        ADD3_read.append(sorted[el])
    for el in range(24, 32):
        ADD4_read.append(sorted[el])
    MCPdig = sorted[32]
    ADD1dig = sorted[33]
    ADD3dig = sorted[34]
    ADD4dig = sorted[35]
    ADD1_read2 = convert_read_val(ADD1_read)
    ADD3_read2 = convert_read_val(ADD3_read)
    ADD4_read2 = convert_read_val(ADD4_read)
    return ADC_read, ADD1_read2, ADD3_read2, ADD4_read2, MCPdig, ADD1dig, ADD3dig, ADD4dig

ADC_read, ADD1_read, ADD3_read, ADD4_read, MCPdig, ADD1dig, ADD3dig, ADD4dig = read_fun()

class ColorButton(tk.Button):
    def __init__(self, parent, channelN, chipname, init_value, activeLow, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.init_value = init_value
        self.activeLow = activeLow
        self.chipname = chipname
        self.channelN = channelN
        self.init_status()
        self.bind("<Button-1>", self.press)

    def init_status(self):
        if self.activeLow == 0:
            if self.init_value == 1:
                self.pressed = True
                self['bg'] = 'skyblue'
                self['fg'] = 'red'
            else:
                self.pressed = False
                self['bg'] = 'white'
                self['fg'] = 'black'
            self.init_value = not self.init_value
            self.pressed = not self.pressed
        else:
            if self.init_value == 1:
                self.pressed = True
                self['bg'] = 'skyblue'
                self['fg'] = 'red'
            else:
                self.pressed = False
                self['bg'] = 'white'
                self['fg'] = 'black'

    def press(self, *args):
        if self.activeLow == 0:
            if self.pressed and self.init_value == 1:
                self['bg'] = 'skyblue'
                self['fg'] = 'red'
                self.DIGwrite(onOff=True)
            else:
                self['bg'] = 'white'
                self['fg'] = 'black'
                self.DIGwrite(onOff=False)
            self.init_value = not self.init_value
            self.pressed = not self.pressed

        else:
            if self.pressed and self.init_value == 0:
                self['bg'] = 'white'
                self['fg'] = 'black'
                self.DIGwrite(onOff=True)
            else:
                self['bg'] = 'skyblue'
                self['fg'] = 'red'
                self.DIGwrite(onOff=False)
            self.pressed = not self.pressed
        
    def DIGwrite(self, onOff):
        if onOff:
            flc1.write_digital(port_settings.portN, chipnames[self.chipname], alphabet[self.channelN], val=1)
        else:
            flc1.write_digital(port_settings.portN, chipnames[self.chipname], alphabet[self.channelN], val=0)


class SwitchButton(tk.Radiobutton):

    def __init__(self, parent, channelN, chipname, text, activeLow, column=0, row=0, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.activeLow = activeLow
        self.channelN = channelN
        self.chipname = chipname
        self.text = text
        self.column = column
        self.row = row
        self.button = tk.Radiobutton(parent, text=self.text)
        self.button.grid(column=column, row=row)
        self.update_status()

    def digRead(self, *args):
        global MCPdig
        global ADD1dig
        global ADD3dig
        global ADD4dig
        if args == ():
            pass
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
        if digVals[self.channelN] == 1:
            self.button['fg'] = 'black'
            self.button['selectcolor'] = 'red'
        else:
            self.button['fg'] = 'black'
            self.button['selectcolor'] = 'white'



class LabelEntry:
    
    def __init__(self, parent, channelN, chipname, label, k, c, init_value, unit, column=0, row=0):
        self.channelN = channelN
        self.chipname = chipname
        self.unit = unit
        self.k = k
        self.c = c
        self.init_value = init_value
        var = tk.StringVar(parent, value=f'{self.convert_voltage()} {self.unit}')
        self.label = tk.Label(parent, text=label).grid(column=column, row=row)
        self.entry = tk.Entry(parent, textvariable=var, width=10, state='readonly').grid(column=column, row=row, padx=(120, 0))
        self.var = var

    def update(self,*args):
        newVal = f'{self.convert_voltage(*args)} {self.unit}'
        self.var.set(newVal)

    def read(self, *args):
        global ADC_read
        global ADD1_read
        global ADD3_read
        global ADD4_read
        if args == ():
            pass
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
            if adc_range['LTC'] == 5 or adc_range['LTC'] == 10:
                # print("readVal", to_convert)
                voltage = (to_convert/ADCresolution)*adc_range['LTC'] # Equation for voltage range from 0 to 5V and 0 to 10V
            elif to_convert > ADCresolution/2:
                voltage = (to_convert-ADCresolution)/ADCresolution*abs(adc_range['LTC'])*2 # Equation for voltage range from -5 to 5V and -10 to 10V -> positive voltage
            else:
                voltage = to_convert/ADCresolution*abs(adc_range['LTC'])*2 # Equation for voltage range from -5 to 5V and -10 to 10V -> negative voltage
        else:
            if adc_range[self.chipname] == 5 or adc_range[self.chipname] == 10:
                voltage = (to_convert/ADDresolution)*adc_range[self.chipname]
            elif to_convert > ADDresolution/2:
                voltage = (to_convert-ADDresolution)/ADDresolution*abs(adc_range[self.chipname])*2
            else:
                voltage = to_convert/ADDresolution*abs(adc_range[self.chipname])*2
        readValue = voltage*self.k + self.c
        var = '{:.3f}'.format(readValue)
        return var

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


def sortDIGvals(val, chiptype):
    listDIG = []
    bin0 = bin(val)
    bin1 = bin0[2:]
    for val in bin1[::-1]:
        listDIG.append(int(val))
    if chiptype == 'mcp':
        while len(listDIG) < 16:
            listDIG.append(0)
    elif chiptype == 'add':
        while len(listDIG) < 8:
            listDIG.append(0)
    else:
        print('Wrong chiptype')
    return listDIG


mcp, add1, add3, add4, adc, pwr = FLC_command.readExcel()
add1_settings = FLC_command.collect_chip_data(add1)
add3_settings = FLC_command.collect_chip_data(add3)
add4_settings = FLC_command.collect_chip_data(add4)
mcp_settings = FLC_command.collect_chip_data(mcp)
adc_settings = FLC_command.collect_chip_data(adc)

readingBoxes = []
digitalButtons = []

def control_panel(chip, chipname):
    for channel in chip:
        index = chip.index(channel)
        if not channel.hidden:
            if channel.function == 'DAC':
                Widget1(frame, channelN=index, chipname=chipname, label=channel.name, k=channel.k, c=channel.constant, init_value=channel.initValues, unit=channel.unit, column=channel.coordX, row=channel.coordY)
            elif channel.function == 'ADC':
                readingBox = LabelEntry(frame, channelN = index, chipname=chipname, label=channel.name, k=channel.k, c=channel.constant, init_value=channel.initValues, unit=channel.unit, column=channel.coordX, row=channel.coordY)
                readingBoxes.append(readingBox)
            elif channel.function == 'DIG_IN':
                digitalButton = SwitchButton(frame, channelN=index, chipname=chipname, text=channel.name, activeLow = channel.activeLow, column=channel.coordX, row=channel.coordY)
                digitalButtons.append(digitalButton)
            elif channel.function == 'DIG_OUT':
                ColorButton(frame, channelN=index, chipname=chipname, init_value=channel.initValues, activeLow=channel.activeLow, text=channel.name).grid(column=channel.coordX, row=channel.coordY)
            elif channel.function == 'PWR':
                pass
            else:
                print('Unknown function')

control_panel(add1_settings, 'ADD1')
control_panel(add3_settings, 'ADD3')
control_panel(add4_settings, 'ADD4')
control_panel(mcp_settings, 'mcp')
control_panel(adc_settings, 'adc')

def update_fun():
    ADC_read, ADD1_read, ADD3_read, ADD4_read, MCPdig, ADD1dig, ADD3dig, ADD4dig = read_fun()
    for box in readingBoxes:
        box.update(ADC_read, ADD1_read, ADD3_read, ADD4_read)
    for digitalButton in digitalButtons:
        digitalButton.update_status(MCPdig, ADD1dig, ADD3dig, ADD4dig)
    if True:
        frame.after(500, update_fun)

frame.after(500, update_fun)
print("--- %s seconds ---" % (time.time() - start_time))
frame.mainloop()

