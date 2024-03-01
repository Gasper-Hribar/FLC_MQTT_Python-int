## Using the FLC interface controller program

Before you start using the program be sure that your computer meets the following software requirements to run the program:
- installed PlatformIO for VS code
- installed Arduino Software IDE

When you meet all of these requirements, connect your Arduino DUE to the FLC interface via FPGA interface and be sure to connect all cables (Ground, 3.3V, MISO, MOSI, CLOCK, CS1, CS0 (DA pin), DE pin) - look for pinout diagrams

Now open the program with PlatformIO and select `Upload`. When the program is done uploading, open Arduino Software IDE and open Serial Monitor, select baud rate 115200 and enter your **Serial API commands**.


## Serial API commands

### Write operation
**p**{portN}**c**{chipN}**w**{DAC/dig}**c**{chn}**v**{val} 

- `portN` - port number
- `chipN` - chip number(0-MCP, 2-ADD1, 4-ADD3, 5-ADD4)
- `DAC/dig` - DAC=0; dig=1
- `chn` - channel number from A(channel number 0) to P(channel number 15) for MCP chip and from A(channel number 0) to H(channel number 7) for ADD chips
- `val` - 1/0 (dig); number 0-4095 (DAC)

*examples:*

 `p0c5w1cBv1` - this command will set channel number 1 of the ADD4 on port 0 HIGH

 `p0c4w0cCv255` - this command will write 255 to the channel 2 of the ADD3 on port 0

### Set operation
**p**{portN}**c**{chipN}**s**{setValue}

- `portN` - port number
- `chipN` - chip number(0-MCP, 2-ADD1, 4-ADD3, 5-ADD4)
- `setValue` - for MCP chip: 16 bit number (1 - input/0 - output), for ADD chips: 8 numbers (1-ADC, 2-DAC, 3-digital input, 4-digital output)

*examples:*

 `p0c2s11223344` - this command will set the channels (of the ADD1 on port 0) 0 and 1 to ADC, 2 and 3 to DAC, 4 and 5 to digital input, 6 and 7 to digital output

 `p0c0s1111111111111111` - this command will set all channels of MCP2 on port 0 to input

 **Attention!**
 When setting the MCP chip: MCP set values are in reversed order - if we use the set command `p0c0s0000000011111111` - the channels from 0 to 7 are set as inputs and channels from 8 to 15 are set as outputs

### Read operation
**p**{portN}**r**{readN}**g**{gainN}

- `portN` - port number
- `readN` - number from which to read (0-MCP, 1-ADC(LTC), 2-ADD1, 4-ADD3, 5-ADD4); if there is no read number the program reads all chips
- `gainN` - gain number ONLY FOR ADC (LTC) chip: 0 - input range ±5V; 1 - input range ±10V; 2 - input range from 0V to 5V; 3 - input range from 0V to 10V

*examples:*

`p0rg1` - this command will read values of all chips in the following sequence: 8 LTC values (input range ±10V), 8 ADD1 values, 8 ADD3 values, 8 ADD4 values, 1 MCP value, 1 digital ADD1 value, 1 digital ADD3 value, 1 digital ADD4 value

`p0r1g2` - this command will read values from the ADC (LTC) chip (input range from 0V to 5V)

### Gain operation (ADD chips only)
**p**{portN}**c**{chipN}**gA**{ADCgain}**D**{DAC gain}

- `portN` - port number
- `chipN` - chip number(2-ADD1, 4-ADD3, 5-ADD4)
- `ADCgain` - ADC gain number (0 - sets ADC gain from 0 to 2.5 V; 1 - sets ADC gain from 0 to 5 V)
- `DACgain` - DAC gain number (0 - sets DAC gain from 0 to 2.5 V; 1 - sets DAC gain from 0 to 5 V)
