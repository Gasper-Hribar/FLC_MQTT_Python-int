from email.policy import default
from mimetypes import init
from turtle import update
from wsgiref.util import setup_testing_defaults
import serial
from dataclasses import dataclass, field
import time
import pandas as pd
import numpy as np


start_time = time.time()

alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P']

@dataclass
class ChSetting:
    function: str
    name: str
    unit: str
    k: float
    constant: float
    hidden: bool
    coordX: int
    coordY: int
    dacRange: int
    adcRange: int
    minValues: float
    maxValues: float
    initValues: int
    isImportant: bool
    Ximportant: int
    Yimportant: int
    activeLow: bool
    isExp: bool
    B: float
    r0: float
    t0: float
    enableInitVal: bool
    disablePowerDrop: bool

@dataclass
class Alarms:
    enableAlarm: bool
    aboveBelow: bool
    warningVal: float
    interlockVal: float

@dataclass
class MultiplexedChannels:
    multiplexSelectorAddress: int
    isMultiplexed: bool
    multiplexedFunc: str
    hidden: bool
    x: int
    y: int
    multiplexedName: str
    isMuxImportant: bool
    ximportant: int
    yimportant: int
    initValMux: float
    muxActiveLow: bool

def sortData(data):
    chSetting = ChSetting(function=data.iloc[2], name=data.iloc[3], unit=data.iloc[4], k=float(data.iloc[5]), constant=float(data.iloc[6]), hidden=bool(data.iloc[7]), coordX=int(data.iloc[8]), coordY=int(data.iloc[9]), dacRange=int(data.iloc[10]), adcRange=int(data.iloc[11]), minValues=float(data.iloc[12]), maxValues=float(data.iloc[13]), initValues=int(data.iloc[14]), isImportant=bool(data.iloc[15]), Ximportant=int(data.iloc[16]), Yimportant=int(data.iloc[17]), activeLow=bool(data.iloc[18]), isExp=bool(data.iloc[19]), B=float(data.iloc[20]), r0=float(data.iloc[21]), t0=float(data.iloc[22]), enableInitVal=bool(data.iloc[23]), disablePowerDrop=bool(data.iloc[40]))
    alarms = Alarms(enableAlarm=bool(data.iloc[24]), aboveBelow=bool(data.iloc[25]), warningVal=float(data.iloc[26]), interlockVal=float(data.iloc[27]))
    mplxChns = MultiplexedChannels(multiplexSelectorAddress=int(data.iloc[28]), isMultiplexed=bool(data.iloc[29]), multiplexedFunc=str(data.iloc[30]), hidden=bool(data.iloc[31]), x=int(data.iloc[32]), y=int(data.iloc[33]), multiplexedName=data.iloc[34], isMuxImportant=bool(data.iloc[35]), ximportant=int(data.iloc[36]), yimportant=int(data.iloc[37]), initValMux=float(data.iloc[38]), muxActiveLow=bool(data.iloc[39]))
    return chSetting, alarms, mplxChns

def readExcel():
    excel_data = pd.read_excel('ADD_adapter_test.xlsm', sheet_name='Sheet1')
    excel_data = excel_data.fillna(value=0)
    add4_data = excel_data.iloc[[25, 4, 26, 5, 27, 6, 28, 7]]
    add3_data = excel_data.iloc[[9, 29, 10, 31, 54]]
    add1_data = excel_data.iloc[[18, 39, 20, 42, 21, 43, 44, 23]]
    mcp_data = excel_data.iloc[[13, 36, 15, 37, 38, 46, 47, 48, 49, 50, 51, 52, 55]]
    adc_data = excel_data.iloc[[11, 32, 12, 33, 34, 14, 35, 53]]
    pwr = excel_data.iloc[[8, 16, 17, 19, 22, 30, 40, 41]]

    mcp_data2 = [mcp_data.iloc[0], mcp_data.iloc[1], mcp_data.iloc[2], mcp_data.iloc[3], mcp_data.iloc[4], None, None, mcp_data.iloc[5], mcp_data.iloc[6], mcp_data.iloc[7], mcp_data.iloc[8], mcp_data.iloc[9], mcp_data.iloc[10], mcp_data.iloc[11], mcp_data.iloc[12], None]
    add1_data2 = [add1_data.iloc[i] for i in range(len(add1_data))]
    add3_data2 = [add3_data.iloc[0], add3_data.iloc[1], add3_data.iloc[2], add3_data.iloc[3], add3_data.iloc[4], None, None, None]
    add4_data2 = [add4_data.iloc[i] for i in range(len(add4_data))]
    adc_data2 = [adc_data.iloc[i] for i in range(len(adc_data))]
    pwr2 = [pwr.iloc[i] for i in range(len(pwr))]

    return mcp_data2, add1_data2, add3_data2, add4_data2, adc_data2, pwr2

def collect_chip_data(chip):
    completeChip = []
    for r in range(len(chip)):
        if chip[r] is None:
            completeChip.append(ChSetting(function='DIG_IN', name=f'hidden_channel{r}', unit='0', k=0.0, constant=0.0, hidden=True, coordX=0, coordY=0, dacRange=0, adcRange=0, minValues=0.0, maxValues=0.0, initValues=0, isImportant=False, Ximportant=0, Yimportant=0, activeLow=False, isExp=False, B=0.0, r0=0.0, t0=0.0, enableInitVal=False, disablePowerDrop=False))
        else:
            chipS, chipAlarm, chipMplx = sortData(chip[r])
            completeChip.append(chipS)
    return completeChip

def collect_chip_function(completeChip, command, name):
    slovarcek = {'ADC':1, 'DAC':2, 'DIG_IN':3, 'DIG_OUT':4}
    slovarMCP = {'DIG_OUT': 0, 'DIG_IN': 1}
    chipValues = []
    for channel in completeChip:
        if name == 'mcp':
            if command == 'setOperation':
                for config in slovarMCP:
                    if channel.function == config:
                        chipValues.append(slovarMCP[config])
                    else:
                        pass
            elif command == 'writeOperation':
                chipValues.append(channel.initValues)
            else:
                print('Wrong command!')
        elif name == 'add':
            if command == 'setOperation':
                for config in slovarcek:
                    if channel.function == config:
                        chipValues.append(slovarcek[config])
                    else:
                        pass
            elif command == 'writeOperation':
                chipValues.append(channel.initValues)
        else:
            print('wrong name!')
    
    return chipValues


@dataclass
class SerialSettings:
    port: str
    baud_rate: int = 115200
    timeout: int = 0.1

@dataclass
class PortSetting:
    portN: int
    mcp_settings: list = field(default_factory=lambda: [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    add1_settings: list = field(default_factory=lambda: [0,0,0,0,0,0,0,0])
    add3_settings: list = field(default_factory=lambda: [0,0,0,0,0,0,0,0])
    add4_settings: list = field(default_factory=lambda: [0,0,0,0,0,0,0,0])
    
    def updateChipSettings(self):
        mcp, add1, add3, add4, adc, pwr = readExcel()
        self.add1_settings = collect_chip_function(collect_chip_data(add1), 'setOperation', 'add')
        self.add3_settings = collect_chip_function(collect_chip_data(add3), 'setOperation', 'add')
        self.add4_settings = collect_chip_function(collect_chip_data(add4), 'setOperation', 'add')
        self.mcp_settings = collect_chip_function(collect_chip_data(mcp), 'setOperation', 'mcp')
        

@dataclass
class PortInit:
    mcp_init_values: list = field(default_factory=lambda: [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    add1_init_values: list = field(default_factory=lambda: [0,0,0,0,0,0,0,0])
    add3_init_values: list = field(default_factory=lambda: [0,0,0,0,0,0,0,0])
    add4_init_values: list = field(default_factory=lambda: [0,0,0,0,0,0,0,0])

    def updateChipInitial(self):
        mcp, add1, add3, add4, adc, pwr = readExcel()
        self.add1_init_values = collect_chip_function(collect_chip_data(add1), 'writeOperation', 'add')
        self.add3_init_values = collect_chip_function(collect_chip_data(add3), 'writeOperation', 'add')
        self.add4_init_values = collect_chip_function(collect_chip_data(add4), 'writeOperation', 'add')
        self.mcp_init_values = collect_chip_function(collect_chip_data(mcp), 'writeOperation', 'mcp')


class FLC_interface:
    def __init__(self, serial_settings:SerialSettings, settings:list[PortSetting], initVals:list[PortInit]):
        self.settings = settings
        self.initVals = initVals
        self.arduino = serial.Serial(port=serial_settings.port, baudrate=serial_settings.baud_rate, timeout=serial_settings.timeout)
        self.arduino.close()
        self.arduino.open()
        self.initialize_ports()

    def convert(self, list1):
        list2 = [f'{a}' for a in list1]
        result = "".join(list2)
        return result

    def initialize_ports(self):
        for port_setting in self.settings:
            portN = port_setting.portN
            setMCP = self.convert(port_setting.mcp_settings)
            setADD1 = self.convert(port_setting.add1_settings)
            setADD3 = self.convert(port_setting.add3_settings)
            setADD4 = self.convert(port_setting.add4_settings)

        for initVal in self.initVals:
            writeMCP = self.convert(initVal.mcp_init_values)
            writeADD1 = self.convert(initVal.add1_init_values)
            writeADD3 = self.convert(initVal.add3_init_values)
            writeADD4 = self.convert(initVal.add4_init_values)


        print('setValues:', setMCP, setADD1, setADD3, setADD4)
        print('writeValues:', writeMCP, writeADD1, writeADD3, writeADD4)

        self.set_operation(portN, 0, setMCP)
        self.set_operation(portN, 2, setADD1)
        self.set_operation(portN, 4, setADD3)
        self.set_operation(portN, 5, setADD4)

        for a in range(len(writeMCP)):
            self.write_digital(portN, 0, alphabet[a], writeMCP[a])

        self.writeADD(portN, writeADD1, setADD1, 2)
        self.writeADD(portN, writeADD3, setADD3, 4)
        self.writeADD(portN, writeADD4, setADD4, 5)

    def writeADD(self, portN, addW, addS, chN):
        for a in range(len(addS)):
            if addS[a] == '1' or addS[a] == '3' or addS[a] == '4':
                self.write_digital(portN, chN, alphabet[a], addW[a])
            elif addS[a] == '2':
                self.write_dac(portN, chN, alphabet[a], addW[a])
            else:
                print('Error')

    def write(self, x):
        data_to_send = bytes(x+"\n", 'utf-8')
        time.sleep(0.18)
        self.arduino.write(data_to_send)
        #print('Data was sent: %s' % data_to_send)

    def read(self):
        data = self.arduino.readlines()
        #print('Data was recieved: %s' % data)
        return data

    def write_digital(self, portN:int, chip:int, chN:int, val:int):
        string_to_send = f'p{portN}c{chip}w1c{chN}v{val}'
        self.write(string_to_send)
        print(string_to_send)
        #print("Successfully written.")

    def write_dac(self, portN:int, chip:int, chN:int, val:int):
        string_to_send = f'p{portN}c{chip}w0c{chN}v{val}'
        self.write(string_to_send)
        print(string_to_send)
        #print("Successfully written.")

    def set_operation(self, portN:int, chip:int, setVal:int):
        string_to_send = f'p{portN}c{chip}s{setVal}'
        print(string_to_send)
        self.write(string_to_send)

    def read_all(self, portN:int):
        string_to_send = f'p{portN}r'
        self.write(string_to_send)
        self.read()

    def read_chips(self, portN:int, readN:int):
        string_to_send = f'p{portN}r{readN}'
        self.write(string_to_send)
        self.read()


if __name__=="__main__":
    serial_settings = SerialSettings(port="COM15")
    port_settings = PortSetting(portN=0)
    port_settings.updateChipSettings()
    initVals = PortInit()
    initVals.updateChipInitial()
    flc1 = FLC_interface(serial_settings=serial_settings, settings=[port_settings], initVals=[initVals])
    print("--- %s seconds ---" % (time.time() - start_time))
