from sys import platform
import os
from os.path import dirname, abspath
import yaml
from dataclasses import dataclass, field
import time
import pandas as pd
import paho.mqtt.client as mqtt_client
import threading

def main():
    path = 'LDpumpCWP_v5_2a-12-15A-Int-ILD-Int-OnP.xlsm'
    excel_data = pd.read_excel(path, sheet_name='Sheet1')

    excel_data = excel_data.fillna(value=0)
    add4_data = excel_data.iloc[[25, 4, 26, 5, 27, 6, 28, 7]]
    print(add4_data.keys())


if __name__ == '__main__':
    main()
