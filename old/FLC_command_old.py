import serial
import time
arduino = serial.Serial(port='COM8', baudrate=115200, timeout=.1)
arduino.close()
arduino.open()

def write(x):
    data_to_send = bytes(x+"\n", 'utf-8')
    time.sleep(0.5)
    arduino.write(data_to_send)
    #print('Data was sent: %s' % data_to_send)

def read():
    data = arduino.readlines()
    print('Data was recieved: %s' % data)
    return data

while True:
    cmd = input("Enter your command: ") # Taking input from user
    if cmd == "end":
        arduino.close()
        exit()
    write(cmd)
    read()
    
