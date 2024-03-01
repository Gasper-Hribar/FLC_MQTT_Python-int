"""

Debugging application for MQTT on the STM32. Connects to port with statically set IP, IPv4:1883. MQTT broker neccessary
for the MQTT protocol to work (currently in use mosquitto). Publishes to topic 'data', subscribed to every topic ("+").
Prints out all received MQTT messages.

Current debugging scheme and key binds:
- in use for debugging STM32 application for communicating with the FLC interface V 3.A.

    Key binds:
    - Home:     sends SET command for a certain chip on FLC interface board
    - Alt Gr:   sends WRITE command
    - Page Up:  sends READ command
    - Page Down:sends SET GAIN command for ADC chip.

    Commands that are sent are saved and read from commands.json file.
    Explanation of the commands and their decoding is written in the readme2comm file. The protocol is adapted from an
    Arduino application with the same use. 

"""


import paho.mqtt.client as mqtt_client
from pynput import keyboard
from pynput.keyboard import Key
import time
import json
import pyroute2
from pyroute2 import iproute

#
#  GLOBAL VARIABLES
#

broker = '192.168.1.1'
port = 1883
topic = "+"
client_id = "IDpython"

#
# APPLICATION 
#

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Successful connection to broker.")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        try:
            print(f"\n\rReceived: {msg.payload.decode()}; from topic: {msg.topic}.\n\r")
        except:
            client.publish("test", f"{msg.payload} from topic {msg.topic}")
    client.subscribe(topic)
    client.on_message = on_message


def main():

#    ip = iproute()
#    index = ip.link_lookup(ifname='em1')[0]
#    ip.addr('add', index, address='192.168.1.1', mask=24)
#    ip.close()
#    time.sleep(5)

    client = connect_mqtt()
    subscribe(client)
    client.publish("test", "Data from Python", qos=0, retain=False)
    client.loop_start()
    

    def on_press(key):

        if KeyboardInterrupt:
            # print(key)
            if key == Key.esc:

            # client.loop_stop()
            # 
                client.disconnect()
        
        return

    def on_release(key):
        with open("commands.json", "r") as file:
            data = json.load(file)
            # print(data["commands"][:][:][:])
        # write operation
        if key == Key.alt_gr:
            if client.is_connected():
                print("publish write")
                client.publish("data", data["commands"][:][0]["write"], qos=0, retain=False)
            else:
                client.connect(broker, port)
        
        # set operation
        if key == Key.home:
            if client.is_connected():
                print("publish set")
                client.publish("data", data["commands"][:][1]["set"], qos=0, retain=False)
            else:
                client.connect(broker, port)
                
        # read operation
        if key == Key.page_up:
            if client.is_connected():
                print("publish read")
                client.publish("data", data["commands"][:][2]["read"], qos=0, retain=False)
            else:
                client.connect(broker, port)

        # gain operation
        if key == Key.page_down:
            if client.is_connected():
                print("publish gain")
                client.publish("data", data["commands"][:][3]["gain"], qos=0, retain=False)
            else:
                client.connect(broker, port)
                
        
        return

    while True:
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
        

    return


if __name__ == "__main__":
    main()
