from email.policy import default
from mimetypes import init
from wsgiref.util import setup_testing_defaults
import serial
from dataclasses import dataclass, field
import time
import pandas as pd
import numpy as np

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
    initValues: float
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

#disablePowerDrop

def sortData(data, channel):
    chSetting = ChSetting(function=data.iloc[channel,2], name=data.iloc[channel,3], unit=data.iloc[channel,4], k=float(data.iloc[channel,5]), constant=float(data.iloc[channel,6]), hidden=bool(data.iloc[channel,7]), coordX=int(data.iloc[channel,8]), coordY=int(data.iloc[channel,9]), dacRange=int(data.iloc[channel,10]), adcRange=int(data.iloc[channel,11]), minValues=float(data.iloc[channel,12]), maxValues=float(data.iloc[channel,13]), initValues=float(data.iloc[channel,14]), isImportant=bool(data.iloc[channel,15]), Ximportant=int(data.iloc[channel,16]), Yimportant=int(data.iloc[channel,17]), activeLow=bool(data.iloc[channel,18]), isExp=bool(data.iloc[channel,19]), B=float(data.iloc[channel,20]), r0=float(data.iloc[channel,21]), t0=float(data.iloc[channel,22]), enableInitVal=bool(data.iloc[channel,23]), disablePowerDrop=bool(data.iloc[channel,40]))
    alarms = Alarms(enableAlarm=bool(data.iloc[channel, 24]), aboveBelow=bool(data.iloc[channel,25]), warningVal=float(data.iloc[channel,26]), interlockVal=float(data.iloc[channel,27]))
    mplxChns = MultiplexedChannels(multiplexSelectorAddress=int(data.iloc[channel,28]), isMultiplexed=bool(data.iloc[channel,29]), multiplexedFunc=str(data.iloc[channel,30]), hidden=bool(data.iloc[channel,31]), x=int(data.iloc[channel,32]), y=int(data.iloc[channel,33]), multiplexedName=data.iloc[channel,34], isMuxImportant=bool(data.iloc[channel,35]), ximportant=int(data.iloc[channel,36]), yimportant=int(data.iloc[channel,37]), initValMux=float(data.iloc[channel,38]), muxActiveLow=bool(data.iloc[channel,39]))
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
    mcp_data2 = [mcp_data.iloc[0], mcp_data.iloc[1], mcp_data.iloc[2], mcp_data.iloc[3], None, None, mcp_data.iloc[4], mcp_data.iloc[5], mcp_data.iloc[6], mcp_data.iloc[7], mcp_data.iloc[8], mcp_data.iloc[9], mcp_data.iloc[10], mcp_data.iloc[11], mcp_data.iloc[12], None]
    
    #print(mcp_data2)
    #chipSettings, chipAlarm, chipMplx = sortData(adc_data, channel=7)
    #print("Chip settings: ", chipSettings)
    #print("Alarm", chipAlarm)
    #print("MplxChns", chipMplx)
    #print(mcp_data.iloc[1])
    #print(mcpc_data2)
    print(add4_data.iloc[0].iloc[2])

    return mcp_data, add1_data, add3_data, add4_data, adc_data, pwr

    


    #for i in range(1, 24): #40
    #    print(add4_data.iloc[0,i])

    #for i in range(len(adc_data)):
        #print(adc_data.iloc[i,1])
     #   print(pwr.iloc[i, 1])


    #print(mcp_data)
    #add4_settings, add4_values = collect_add_data(add4_data)
    #add3_settings, add3_values = collect_add_data(add3_data)
    #add1_settings, add1_values = collect_add_data(add1_data)
    #mcp_settings, mcp_values = collect_mcp_data(mcp_data)

    #return add1_settings, add1_values, add3_settings, add3_values, add4_settings, add4_values, mcp_settings, mcp_values

def collect_add_data(add_data):
    add_settings = []
    add_values = []
    slovarcek = {'ADC':1, 'DAC':2, 'DIG_IN':3, 'DIG_OUT':4}
    for i in range(len(add_data)):
        for config in slovarcek:
            if add_data.iloc[i,2] == config:
                add_settings.append(slovarcek[config])
            else:
                pass
        add_values.append(int(add_data.iloc[i, 14]))
    while len(add_settings) < 8:
        add_settings.append(3)
    while len(add_values) < 8:
        add_values.append(0)
    return add_settings, add_values


def collect_mcp_data(mcp_data):
    mcp_settings = []
    mcp_values = []
    slovarMCP = {'DIG_OUT': 0, 'DIG_IN': 1}
    for n in range(4):
        mcp_values.append(int(mcp_data.iloc[n, 14]))
        for config in slovarMCP:
            if mcp_data.iloc[n, 2] == config:
                mcp_settings.append(slovarMCP[config])
            else:
                pass

    mcp_settings.append(1)
    mcp_settings.append(1)
    mcp_values.append(0)
    mcp_values.append(0)
    for n in range(4, len(mcp_data)):
        mcp_values.append(int(mcp_data.iloc[n, 14]))
        for config in slovarMCP:
            if mcp_data.iloc[n, 2] == config:
                mcp_settings.append(slovarMCP[config])
            else:
                pass

    while len(mcp_settings) < 16:
        mcp_settings.append(1)
    while len(mcp_values) < 16:
        mcp_values.append(0)
    return mcp_settings, mcp_values

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
        chips={'mcp': 0, 'add1': 2, 'add3': 4, 'add4': 5}
        mcp, add1, add3, add4, adc, pwr = readExcel()
        #self.add1_settings = self.collect_chip_data(add1, 8)
        #self.add3_settings = self.collect_chip_data(add3, 5)
        #self.add4_settings = self.collect_chip_data(add4, 8)
        #print(self.add1_settings, self.add3_settings, self.add4_settings)
        self.collect_chip_data(mcp, 16, '')

    def collect_chip_data(self, chip, length, name):
        slovarcek = {'ADC':1, 'DAC':2, 'DIG_IN':3, 'DIG_OUT':4}
        slovarMCP = {'DIG_OUT': 0, 'DIG_IN': 1}
        chipChannels = []
        chipFunction = []
        completeChip = []
        
        #for r in range(len(chip)):
        #    chipS, chipAlarm, chipMplx = sortData(chip[r], r)
        #    chipChannels.append(chipS.function)
        #print(chipChannels)
            
            #if r is None:
            #    completeChip.append(ChSetting(function='DIG_IN', name='hidden_channel', unit='0', k=0.0, constant=0.0, hidden=True, coordX=0, coordY=0, dacRange=0, adcRange=0, minValues=0.0, maxValues=0.0, initValues=0.0, isImportant=False, Ximportant=0, Yimportant=0, activeLow=False, isExp=False, B=0.0, r0=0.0, t0=0.0, enableInitVal=False, disablePowerDrop=False))
            #else:
            #    chipS, chipAlarm, chipMplx = sortData(chip[r], r)
            #    completeChip.append(chipS)
        #print(completeChip)
            

            
           # if r is None:
           #     item = ChSetting(function='DIG_IN', name='hidden_channel', unit='0', k=0.0, constant=0.0, hidden=True, coordX=0, coordY=0, dacRange=0, adcRange=0, minValues=0.0, maxValues=0.0, initValues=0.0, isImportant=False, Ximportant=0, Yimportant=0, activeLow=False, isExp=False, B=0.0, r0=0.0, t0=0.0, enableInitVal=False, disablePowerDrop=False)
           #     chipChannels.append(item)
           # chipS, chipAlarm, chipMplx = sortData(chip, r)
           # chipChannels.append(chipS)
        #print(chipChannels)
            
            #for index, item in enumerate(chipChannels):
                #print(index, item)
                #if item == None:
                    #chipChannels[index] = ChSetting(function='DIG_IN', name='hidden_channel', unit='0', k=0.0, constant=0.0, hidden=True, coordX=0, coordY=0, dacRange=0, adcRange=0, minValues=0.0, maxValues=0.0, initValues=0.0, isImportant=False, Ximportant=0, Yimportant=0, activeLow=False, isExp=False, B=0.0, r0=0.0, t0=0.0, enableInitVal=False, disablePowerDrop=False)
        #        for config in slovarcek:
        #            if item.function == config:
        #                chipFunction.append(slovarcek[config])
        #            else:
        #                pass
        #    while len(chipFunction) < 8:
        #        chipFunction.append(slovarcek['DIG_IN'])
        #print(chipChannels)
        #return chipFunction

        #print(chipFunction)

        #chipSettings, chipAlarm, chipMplx = sortData(mcp_data, channel=7)
        #print("Chip settings: ", chipSettings)
        #print("Alarm", chipAlarm)
        #print("MplxChns", chipMplx)
        

@dataclass
class PortInit:
    mcp_init_values: list = field(default_factory=lambda: [0,0,0,0,0,0,0,0])
    add1_init_values: list = field(default_factory=lambda: [0,0,0,0,0,0,0,0])
    add3_init_values: list = field(default_factory=lambda: [0,0,0,0,0,0,0,0])
    add4_init_values: list = field(default_factory=lambda: [0,0,0,0,0,0,0,0])

    def updateChipInitial(self, readData):
        pass


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
            if addS[a] != 2:
                self.write_digital(portN, chN, alphabet[a], addW[a])
            elif addS[a] == 2:
                self.write_dac(portN, chN, alphabet[a], addW[a])
            else:
                print('ERROR')


    def write(self, x):
        data_to_send = bytes(x+"\n", 'utf-8')
        time.sleep(0.5)
        self.arduino.write(data_to_send)
        # print('Data was sent: %s' % data_to_send)

    def read(self):
        data = self.arduino.readlines()
        # print('Data was recieved: %s' % data)
        return data

    def write_digital(self, portN:int, chip:int, chN:int, val:bool):
        string_to_send = f'p{portN}c{chip}w{1}c{chN}v{val}'
        self.write(string_to_send)
        # print("Successfully written.")

    def write_dac(self, portN:int, chip:int, chN:int, val:bool):
        string_to_send = f'p{portN}c{chip}w{0}c{chN}v{val}'
        self.write(string_to_send)
        # print("Successfully written.")

    def set_operation(self, portN:int, chip:int, setVal:int):
        string_to_send = f'p{portN}c{chip}s{setVal}'
        # print(string_to_send)
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
    #add1S, add1W, add3S, add3W, add4S, add4W, mcpS, mcpW = readExcel()
    serial_settings = SerialSettings(port="COM8")
    port_settings = PortSetting(portN=0)
    port_settings.updateChipSettings()
    #print(port_settings)
    initVals = PortInit()
    flc1 = FLC_interface(serial_settings=serial_settings, settings=port_settings, initVals=initVals)
    #port_settings = [PortSetting(portN=0, mcp_settings=mcpS, add1_settings=add1S, add3_settings=add3S, add4_settings=add4S)]
    #initVals = [PortInit(mcp_init_values=mcpW, add1_init_values=add1W, add3_init_values=add3W, add4_init_values=add4W)]
    #flc1 = FLC_interface(serial_settings=serial_settings,settings=port_settings, initVals=initVals)
#readExcel()