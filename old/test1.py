import serial
import time
arduino = serial.Serial(port='COM8', baudrate=115200, timeout=.1)
arduino.close()
arduino.open()

settings = [0,[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [2,0,0,0,0,0,0,0,0], [4,0,0,0,0,0,0,0,0], [5,0,0,0,0,0,0,0,0]]
initVals = [[0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0]]

def write(x):
        data_to_send = bytes(x+"\n", 'utf-8')
        time.sleep(0.5)
        arduino.write(data_to_send)
        print('Data was sent: %s' % data_to_send)

def read():
    data = arduino.readlines()
    print('Data was recieved: %s' % data)
    return data

def write_digital(portN:int, chip:int, chN:int, val:bool):
    string_to_send = f'p{portN}c{chip}w{1}c{chN}v{val}'
    write(string_to_send)
    print("Successfully written.")

def write_dac(portN:int, chip:int, chN:int, val:bool):
    string_to_send = f'p{portN}c{chip}w{0}c{chN}v{val}'
    write(string_to_send)
    print("Successfully written.")

def set_operation(portN:int, chip:int, setVal:int):
    string_to_send = f'p{portN}c{chip}s{setVal}'
    print("The following command was sent: ", string_to_send)
    write(string_to_send)

def read_all(portN:int):
    string_to_send = f'p{portN}r'
    write(string_to_send)
    read()

def read_chips(portN:int, readN:int):
    string_to_send = f'p{portN}r{readN}'
    write(string_to_send)
    read()

def initialize_ports():
    for port_setting in settings:
        set_operation(port_setting.portN, port_setting[0], port_setting[1:])

initialize_ports()