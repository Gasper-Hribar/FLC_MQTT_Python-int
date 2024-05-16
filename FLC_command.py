#!/usr/local/lib/python3.11

from sys import platform
import os
from os.path import dirname, abspath
import yaml
from dataclasses import dataclass, field
import time
import pandas as pd
import paho.mqtt.client as mqtt_client
import threading


#
#  GLOBAL VARIABLES
#


PROCESS_PASSED = 0
PROCESS_FAILED = -1

file_directory = dirname(abspath(__file__))
os.chdir(file_directory)

alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P']
add_chipnames = {'ADD1': 2, 'ADD3': 4, 'ADD4': 5}

broker = '192.168.1.1'
broker_port = 1883
topic = "+"
client_id = "IDpython"
transmit_ended_msg = "All sent."
comms_end_flag = 0
comms_end_event = threading.Event()
err_message = ""
recursion_depth = 0 

read_values = {
    'ADC0R': "",
    'ADD1R': "",
    'ADD3R': "",
    'ADD4R': "",
    'MCP0S': "",
    'ADD1D': "",
    'ADD3D': "",
    'ADD4D': "",
}

read_data = {
    'ADC0R': [],
    'ADD1R': [],
    'ADD3R': [],
    'ADD4R': [],
    'MCP0S': 0,
    'ADD1D': 0,
    'ADD3D': 0,
    'ADD4D': 0,
}

#
# APPLICATION 
#

if platform == "linux":
    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION2, client_id)
else:
    client = mqtt_client.Client(client_id)


def connect_to_broker(client: mqtt_client):
    """ 
        MQTT connect to broker function.
    	
        If broker is not yet initialized, this function starts it and then connects to it as a client.
        Possible bug since the app is sometimes required to be opened twice instead of once. It seems
        like the broker hijacks command line and stops the app execution.
    """
   
    if platform == 'linux':
        try:
            import netifaces as ni

            ni.ifaddresses('eth0')
            ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
            print(ip)

            if ip == broker:
                try: 
                    client.connect(broker, broker_port)
                    print("Connected to broker.")
                    return PROCESS_PASSED
                except:
                    os.system('mosquitto -c /etc/mosquitto/conf.d/mosquitto.conf')
                    
                    client.connect(broker, broker_port)
                    print("Connected to broker.")
                    return PROCESS_PASSED
        except:
            return PROCESS_FAILED
    
    else: 
        try:
            client.connect(broker, broker_port)
            return PROCESS_PASSED
        except:
            return PROCESS_FAILED

    return 0


def subscribe(client: mqtt_client, topic='+'):
    """
        MQTT subscribe to topic function.

        Subscribes the client to a + topic, which means the client subscribes to all the topics
        available. Needs a remake if there is to be more than one specific device connected to
        the broker and thus to the GUI.
    """

    def on_message(client, userdata, msg):
        # print("In on_message")
        if msg.topic == "ID1pub":
            # print("On message.")
            result = on_message_to_pub(client=client, userdata=userdata, message=msg)
            if not result == None:
                print(result)
        elif msg.topic == "debug":
            try:
                print(f'Debug message: {msg.payload.decode()}')
            except:
                print(f"Error: Message payload cannot be decoded. [ {msg.payload} ]")
               

    client.subscribe(topic)
    client.on_message = on_message
    return


def on_message_to_pub(client, userdata, message):
    """
        Decode function for received messages via MQTT.

        Decodes the messages and writes the data in key:value pairse inside the dictionary.
        Will also need a remake for it to work with multiple STMs.
    """

    i = 0
    rec_message = message.payload
    try:
        if message.topic == "ID1pub":
            global comms_end_flag
            
            while rec_message and not (b'A' <= rec_message[0:1] <= b'Z'):
                rec_message = rec_message[1:]

            msg = rec_message.decode()

            if transmit_ended_msg in msg:
                comms_end_flag = 1
                comms_end_event.set()
                return 
            else:
                comms_end_flag = 0
                key = msg[0:5]
                read_values[key] = msg[6:]
                return
            
    except Exception:
        print(Exception)
        comms_end_flag = -1
        err_message = f"Error: Message payload cannot be decoded. [ {message.payload} ]"
        print(err_message)
        return err_message
   

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

def readExcel(file):
    excel_data = pd.read_excel(file, sheet_name='Sheet1')
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

def collect_range_data(file):
    range_data = pd.read_excel(file, sheet_name='Sheet1', usecols='K:L')
    range_data.fillna(value=0)
    add4_gains = [float(range_data.iloc[25,0]), float(range_data.iloc[25,1])]
    add3_gains = [float(range_data.iloc[9,0]), float(range_data.iloc[9,1])]
    add1_gains = [float(range_data.iloc[18,0]), float(range_data.iloc[18,1])]
    adc_gains = [float(range_data.iloc[11,0]), float(range_data.iloc[11,1])]
    dac_dict = {'ADD1': add1_gains[0], 'ADD3': add3_gains[0], 'ADD4': add4_gains[0]}
    adc_dict = {'ADD1': add1_gains[1], 'ADD3': add3_gains[1], 'ADD4': add4_gains[1], 'LTC': adc_gains[1]}
    
    return dac_dict, adc_dict

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
            elif command == 'convert_voltage':
                chipValues.append(channel.initValues)
                chipValues.append(channel.k)
                chipValues.append(channel.constant)
                chipValues.append(channel.unit)
                break
            elif command == 'activeLow':
                chipValues.append(channel.activeLow)
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
            elif command == 'convert_voltage':
                channelValues = []
                channelValues.append(channel.initValues)
                channelValues.append(channel.k)
                channelValues.append(channel.constant)
                channelValues.append(channel.unit)
                chipValues.append(channelValues)
            elif command == 'activeLow':
                chipValues.append(channel.activeLow)
            else:
                print('Wrong command!')
        elif name == 'adc':
            if command == 'convert_voltage':
                chipValues.append(channel.initValues)
                chipValues.append(channel.k)
                chipValues.append(channel.constant)
                chipValues.append(channel.unit)
                break
            elif command == 'activeLow':
                chipValues.append(channel.activeLow)
            else:
                print('Wrong command!')
        else:
            print('wrong name!')
    
    return chipValues


@dataclass
class SerialSettings:
    port: str = ""
    baud_rate: int = 115200
    timeout: int = 0.1

@dataclass
class PortSetting:
    portN: int
    mcp_settings: list = field(default_factory=lambda: [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    add1_settings: list = field(default_factory=lambda: [0,0,0,0,0,0,0,0])
    add3_settings: list = field(default_factory=lambda: [0,0,0,0,0,0,0,0])
    add4_settings: list = field(default_factory=lambda: [0,0,0,0,0,0,0,0])
    
    def updateChipSettings(self, excel_address):
        mcp, add1, add3, add4, adc, pwr = readExcel(excel_address)
        self.add1_settings = collect_chip_function(collect_chip_data(add1), 'setOperation', 'add')
        self.add3_settings = collect_chip_function(collect_chip_data(add3), 'setOperation', 'add')
        self.add4_settings = collect_chip_function(collect_chip_data(add4), 'setOperation', 'add')
        self.mcp_settings = collect_chip_function(collect_chip_data(mcp), 'setOperation', 'mcp')
        self.mcp_reversed = self.mcp_settings.copy()
        self.mcp_reversed.reverse()

        print(self.add4_settings)
        

@dataclass
class PortInit:
    mcp_init_values: list = field(default_factory=lambda: [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    add1_init_values: list = field(default_factory=lambda: [0,0,0,0,0,0,0,0])
    add3_init_values: list = field(default_factory=lambda: [0,0,0,0,0,0,0,0])
    add4_init_values: list = field(default_factory=lambda: [0,0,0,0,0,0,0,0])

    def updateChipInitial(self, excel_address):
        mcp, add1, add3, add4, adc, pwr = readExcel(excel_address)
        self.add1_init_values = collect_chip_function(collect_chip_data(add1), 'writeOperation', 'add')
        self.add3_init_values = collect_chip_function(collect_chip_data(add3), 'writeOperation', 'add')
        self.add4_init_values = collect_chip_function(collect_chip_data(add4), 'writeOperation', 'add')
        self.mcp_init_values = collect_chip_function(collect_chip_data(mcp), 'writeOperation', 'mcp')


class FLC_interface:
    def __init__(self, serial_settings:SerialSettings, settings:list[PortSetting], initVals:list[PortInit]):
        self.settings = settings
        self.initVals = initVals
        self.mqtt_client = client

    def initialize_ADDrange(self, excel_address):
        dac_range, adc_range = collect_range_data(excel_address)
        dac_gain = {}
        adc_gain = {}
        for key, value in dac_range.items():
            if value == 5.0:
                dac_gain[key] = 1
            elif value == 2.5:
                dac_gain[key] = 0
            else:
                print("ADD gain has to be 2.5 or 5.0!")
                dac_gain[key] = 1

        for key, value in adc_range.items():
            if value == 5.0:
                adc_gain[key] = 1
            elif value == 2.5:
                adc_gain[key] = 0
            elif key == 'LTC':
                pass
            else:
                print("ADD gain has to be 2.5 or 5.0!")
                adc_gain[key] = 1

        for port_setting in self.settings:
            portN = port_setting.portN

        for chipname, chipnum in add_chipnames.items():
            time.sleep(0.3)
            init_state = f'p{portN}c{chipnum}gA{adc_gain[chipname]}D{dac_gain[chipname]}'
            # print(init_state)
            self.write(init_state)
    
    def convert(self, list1):
        list2 = [f'{a}' for a in list1]
        result = "".join(list2)
        return result

    def sort_writeADD_data(self, chip_data, setVals, activeLow, rangeV):
        ADDresolution = 4095
        write_values = []
        for channel in range(len(chip_data)):
            init_value, k, c, unit = chip_data[channel]
            if unit != '0':
                if setVals[channel] == 2:
                    voltage = (init_value - c)/k
                    write_data = round((voltage/rangeV)*ADDresolution)
                    write_values.append(write_data)
                else:
                    write_values.append(init_value)
            else:
                write_values.append(0)

        write_values2 = self.check_activeL(write_values, activeLow)
        return write_values2
        
    def check_activeL(self, writeVals, activeLow):
        writeV = []
        for el in range(len(activeLow)):
            if activeLow[el] == 1:
                writeV.append(int(not writeVals[el]))
            else:
                writeV.append(writeVals[el])
        return writeV

    def initialize_ports(self, excel_address):
        mcp, add1, add3, add4, adc, pwr = readExcel(excel_address)
        dac_range, adc_range = collect_range_data(excel_address)

        # initvalue, k, c, unit
        add1_complete = collect_chip_function(collect_chip_data(add1), 'convert_voltage', 'add')
        add3_complete = collect_chip_function(collect_chip_data(add3), 'convert_voltage', 'add')
        add4_complete = collect_chip_function(collect_chip_data(add4), 'convert_voltage', 'add')

        mcp_aL = collect_chip_function(collect_chip_data(mcp), 'activeLow', 'mcp')
        add1_aL = collect_chip_function(collect_chip_data(add1), 'activeLow', 'add')
        add3_aL = collect_chip_function(collect_chip_data(add3), 'activeLow', 'add')
        add4_aL = collect_chip_function(collect_chip_data(add4), 'activeLow', 'add')


        for port_setting in self.settings:
            portN = port_setting.portN
            setMCP = self.convert(port_setting.mcp_reversed)
            # print("setMCP", setMCP)
            reversed_setMCP = self.convert(port_setting.mcp_settings)
            # print("reversedMCP", reversed_setMCP)
            setADD1 = self.convert(port_setting.add1_settings)
            setADD3 = self.convert(port_setting.add3_settings)
            setADD4 = self.convert(port_setting.add4_settings)
            write_data1 = self.sort_writeADD_data(add1_complete, port_setting.add1_settings, add1_aL, dac_range['ADD1'])
            write_data3 = self.sort_writeADD_data(add3_complete, port_setting.add3_settings, add3_aL, dac_range['ADD3'])
            write_data4 = self.sort_writeADD_data(add4_complete, port_setting.add4_settings, add4_aL, dac_range['ADD4'])

        for initVal in self.initVals:
            writeMCP = self.check_activeL(initVal.mcp_init_values, mcp_aL)
            # print("writeMCP", writeMCP)

        self.set_operation(portN, 0, setMCP)
        self.set_operation(portN, 2, setADD1)
        self.set_operation(portN, 4, setADD3)
        self.set_operation(portN, 5, setADD4)

        for a in range(len(writeMCP)):
            if reversed_setMCP[a] == '0':
                self.write_digital(portN, 0, alphabet[a], writeMCP[a])
            else:
                pass

        self.writeADD(portN, write_data1, setADD1, 2)
        self.writeADD(portN, write_data3, setADD3, 4)
        self.writeADD(portN, write_data4, setADD4, 5)

    def writeADD(self, portN, addW, addS, chN):
        for a in range(len(addW)):
            if addS[a] == '4':
                self.write_digital(portN, chN, alphabet[a], addW[a])
            elif addS[a] == '2':
                self.write_dac(portN, chN, alphabet[a], addW[a])
            else:
                pass

    def write(self, message):
        global read_data, read_values

        read_values = {
            'ADC0R': "",
            'ADD1R': "",
            'ADD3R': "",
            'ADD4R': "",
            'MCP0S': "",
            'ADD1D': "",
            'ADD3D': "",
            'ADD4D': "",
        }

        read_data = {
            'ADC0R': [],
            'ADD1R': [],
            'ADD3R': [],
            'ADD4R': [],
            'MCP0S': 0,
            'ADD1D': 0,
            'ADD3D': 0,
            'ADD4D': 0,
        }

        self.mqtt_client.publish('data', message, qos=0, retain=False)
        # print("Sent: ", x, "\n")

    def read(self):
        comms_end_event.wait(5)
        comms_end_event.clear()

        for key, val in read_values.items():
            for i in val.split(','):
                if not i == '':
                    if key[4] == 'R':
                        # print(key)
                        read_data[key].append(int(i))
                    else:
                        read_data[key] = int(i)
                        # print(f'{key} = {int(i)}')
        # print(read_data)
        return read_data, comms_end_flag 

    def write_digital(self, portN:int, chip:int, chN:int, val:int):
        string_to_send = f'p{portN}c{chip}w1c{chN}v{val}'
        self.write(string_to_send)
        # print(string_to_send)

    def write_dac(self, portN:int, chip:int, chN:int, val:int):
        string_to_send = f'p{portN}c{chip}w0c{chN}v{val}'
        self.write(string_to_send)
        # print(string_to_send)

    def set_operation(self, portN:int, chip:int, setVal:int):
        string_to_send = f'p{portN}c{chip}s{setVal}'
        # print(string_to_send)
        self.write(string_to_send)

    def read_all(self, portN:int, gain:int):
        string_to_send = f'p{portN}rg{gain}'
        self.write(string_to_send)
        result, flag = self.read()
        return (result, flag)

    def read_chips(self, portN:int, readN:int):
        string_to_send = f'p{portN}r{readN}'
        self.write(string_to_send)
        result, flag = self.read()
        return (result, flag)

    def read_ADC(self, portN:int, gain:int):
        string_to_send = f'p{portN}r1g{gain}'
        self.write(string_to_send)
        result, flag = self.read()
        return (result, flag)
    
serial_settings = SerialSettings()

if __name__=="__main__":
    
    ports = {}
    with open("port_settings.yaml", "r") as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    for key, value in data.items():
        if key.startswith('port'):
            ports[int(key[4])] = value
        else:
            pass
    # print(ports)
    for portnum, excel_address in ports.items():
        mcp, add1, add3, add4, adc, pwr = readExcel(excel_address)
        dac_range, adc_range = collect_range_data(excel_address)
        port_settings = PortSetting(portN=portnum)
        port_settings.updateChipSettings(excel_address)
        initVals = PortInit()
        initVals.updateChipInitial(excel_address)
        flc1 = FLC_interface(serial_settings=serial_settings, settings=[port_settings], initVals=[initVals])
        
        time.sleep(0.1)
