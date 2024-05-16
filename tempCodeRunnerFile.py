from sys import platform
import os
from os.path import dirname, abspath
import yaml
from dataclasses import dataclass, field
import time
import pandas as pd
import paho.mqtt.client as mqtt_client
import threading


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


def collect_chip_data(chip):
    completeChip = []
    for r in range(len(chip)):
        if chip[r] is None:
            completeChip.append(ChSetting(function='DIG_IN', name=f'hidden_channel{r}', unit='0', k=0.0, constant=0.0, hidden=True, coordX=0, coordY=0, dacRange=0, adcRange=0, minValues=0.0, maxValues=0.0, initValues=0, isImportant=False, Ximportant=0, Yimportant=0, activeLow=False, isExp=False, B=0.0, r0=0.0, t0=0.0, enableInitVal=False, disablePowerDrop=False))
        else:
            chipS, chipAlarm, chipMplx = sortData(chip[r])
            completeChip.append(chipS)
    return completeChip


def sortData(data):
    chSetting = ChSetting(function=data.iloc[2], name=data.iloc[3], unit=data.iloc[4], k=float(data.iloc[5]), constant=float(data.iloc[6]), hidden=bool(data.iloc[7]), coordX=int(data.iloc[8]), coordY=int(data.iloc[9]), dacRange=int(data.iloc[10]), adcRange=int(data.iloc[11]), minValues=float(data.iloc[12]), maxValues=float(data.iloc[13]), initValues=int(data.iloc[14]), isImportant=bool(data.iloc[15]), Ximportant=int(data.iloc[16]), Yimportant=int(data.iloc[17]), activeLow=bool(data.iloc[18]), isExp=bool(data.iloc[19]), B=float(data.iloc[20]), r0=float(data.iloc[21]), t0=float(data.iloc[22]), enableInitVal=bool(data.iloc[23]), disablePowerDrop=bool(data.iloc[40]))
    alarms = Alarms(enableAlarm=bool(data.iloc[24]), aboveBelow=bool(data.iloc[25]), warningVal=float(data.iloc[26]), interlockVal=float(data.iloc[27]))
    mplxChns = MultiplexedChannels(multiplexSelectorAddress=int(data.iloc[28]), isMultiplexed=bool(data.iloc[29]), multiplexedFunc=str(data.iloc[30]), hidden=bool(data.iloc[31]), x=int(data.iloc[32]), y=int(data.iloc[33]), multiplexedName=data.iloc[34], isMuxImportant=bool(data.iloc[35]), ximportant=int(data.iloc[36]), yimportant=int(data.iloc[37]), initValMux=float(data.iloc[38]), muxActiveLow=bool(data.iloc[39]))
    return chSetting, alarms, mplxChns


def main():
    path = 'LDpumpCWP_v5_2a-12-15A-Int-ILD-Int-OnP.xlsm'
    excel_data = pd.read_excel(path, sheet_name='Sheet1')

    excel_data = excel_data.fillna(value=0)
    add4_data = excel_data.iloc[[25, 4, 26, 5, 27, 6, 28, 7]]
    chip4 = collect_chip_data(add4_data)
    print(chip4)



if __name__ == '__main__':
    main()
