from functools import partial
import tkinter as tk
from tkinter.ttk import Combobox
root = tk.Tk()
frame = tk.Frame(root)
frame.grid()
root.title('ADD_adapter_test-port0')

class ColorButton(tk.Button):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.pressed = True
        self.bind("<Button-1>", self.press)
    def press(self, *args):
        if self.pressed:
            self['bg'] = 'skyblue'
            self['fg'] = 'red'
            self.messagef()
        else:
            self['bg'] = 'white'
            self['fg'] = 'black'
        self.pressed = not self.pressed
    def messagef(self):
        print("Some message")

class SwitchButton(tk.Radiobutton):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.pressed = True
        self.bind("<Button-1>", self.press)

    def press(self, *args):
        if self.pressed:
            self['fg'] = 'black'
            self['selectcolor'] = 'red'
            self.messagef()
        else:
            self['fg'] = 'black'
            self['selectcolor'] = 'white'
        self.pressed = not self.pressed

    def messagef(self):
        print("The button was clicked")
        

class LabelEntry:
    
    def __init__(self, parent, label, column=0, row=0):
        self.label = tk.Label(parent, text=label).grid(column=column, row=row)
        self.entry = tk.Entry(parent, width=10, state='readonly').grid(column=column, row=row, padx=(120, 0))
    

class Widget1:

    def __init__(self, parent, label, column=0, row=0, start=0, stop=100, values=[0, 0.1, 0.01, 1, 2, 10]):

        var1 = tk.IntVar(value=1)
        self.label1 = tk.Label(parent, text=label).grid(column=column, row=row, padx=(0,20))
        self.label2 = tk.Label(parent, text='V').grid(column=column, row=row, padx=(170,20))
        self.label3 = tk.Label(parent, text='Step').grid(column=column, row=row, pady=(50,0))

        self.spinbox = tk.Spinbox(parent)
        self.spinbox.grid(column=column, row=row, padx=(100,10))
        self.spinbox['from_'] = start
        self.spinbox['to'] = stop
        self.spinbox['width'] = 6
        self.spinbox['command'] = self.set_value
        self.spinbox['state'] = 'readonly'

        self.checkbutton = tk.Checkbutton(parent)
        self.checkbutton.grid(column=column, row=row, pady=(50,0), padx=(0,50))
        self.checkbutton['variable'] = var1
        self.checkbutton['command'] = partial(self.update, var1)
        
        self.combobox = Combobox(parent)
        self.combobox['width'] = 6
        self.combobox['values'] = values
        self.combobox.current(3) # default value of the combobox based on the values given
        self.combobox.grid(column=column, row=row, pady=(50,0), padx=(100,0))
        self.combobox.bind('<<ComboboxSelected>>', self.config_increment)

    def update(self, var):
        state = var.get()
        if state == 1:
            self.combobox.configure(state='readonly')
            self.spinbox.configure(increment = self.combobox.get())
        else:
            self.combobox.configure(state='disabled')
            self.spinbox.configure(increment = 0)

    def config_increment(self, event):
        self.spinbox.configure(increment = self.combobox.get())

    def set_value(self):
        increment = self.spinbox.get()
        print('This is your SetValue %s' % increment)


SwitchButton(frame, text='DIG_AD').grid(column=0, row=0)
ColorButton(frame, text='DIG_ADD_2').grid(column=0, row=1)
Widget1(frame, 'DAC_ADC', 0, 2, 0, 100, [0, 0.1, 0.01, 1, 2, 10])
Widget1(frame, 'DAC_ADC', 0, 3, 0, 100, [0, 0.1, 0.01, 1, 2, 10])
Widget1(frame, 'DAC_ADC', 0, 4, 0, 100, [0, 0.1, 0.01, 1, 2, 10])
Widget1(frame, 'DAC_ADC', 0, 5, 0, 100, [0, 0.1, 0.01, 1, 2, 10])
Widget1(frame, 'DAC_ADC', 0, 6, 0, 100, [0, 0.1, 0.01, 1, 2, 10])
Widget1(frame, 'DAC_ADC', 0, 7, 0, 100, [0, 0.1, 0.01, 1, 2, 10])
Widget1(frame, 'DAC_ADC', 0, 8, 0, 100, [0, 0.1, 0.01, 1, 2, 10])
Widget1(frame, 'DAC_ADC', 0, 9, 0, 100, [0, 0.1, 0.01, 1, 2, 10])



SwitchButton(frame, text='DIG_AD').grid(column=1, row=0)
ColorButton(frame, text='DIG_ADD_3').grid(column=1, row=1, padx=15)
LabelEntry(frame, 'ADC_ADC', 1, 2)
LabelEntry(frame, 'ADC_ADC', 1, 3)
LabelEntry(frame, 'ADC_ADC', 1, 4)
LabelEntry(frame, 'ADC_ADC', 1, 5)
SwitchButton(frame, text='DAC_AD').grid(column=1, row=6)
LabelEntry(frame, 'DAC_ADC', 1, 7)
LabelEntry(frame, 'DAC_ADC', 1, 8)
LabelEntry(frame, 'DAC_ADC', 1, 9)
ColorButton(frame, text='DIG_DG_0').grid(column=1, row=10)
ColorButton(frame, text='DIG_DG_1').grid(column=1, row=11)
SwitchButton(frame, text='DIG_DG').grid(column=1, row=12)
SwitchButton(frame, text='DIG_DG').grid(column=1, row=13)
ColorButton(frame, text='DIG_ADD_4...').grid(column=1, row=14)
SwitchButton(frame, text='DIG_AD').grid(column=1, row=15)
ColorButton(frame, text='DIG_ADD_4...').grid(column=1, row=16)
SwitchButton(frame, text='DIG_AD').grid(column=1, row=17)



ColorButton(frame, text='PS_ON').grid(column=2, row=0, padx=20)
ColorButton(frame, text='STATUS_C...').grid(column=2, row=1)
ColorButton(frame, text='INTRLCK_C...').grid(column=2, row=2)
ColorButton(frame, text='ON2/IN11-O...').grid(column=2, row=3)
ColorButton(frame, text='PULSE2/IN1...').grid(column=2, row=4)
ColorButton(frame, text='ISO_EN').grid(column=2, row=5)
ColorButton(frame, text='SW_CLK/BU...').grid(column=2, row=6)
LabelEntry(frame, 'I_module', 2, 7)
Widget1(frame, 'INTR_LCK', 2, 8, 0, 100)
ColorButton(frame, text='ILD_SW').grid(column=2, row=9)

root.mainloop()
