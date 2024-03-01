import tkinter as tk
from tkinter.ttk import Combobox
root = tk.Tk()
frame = tk.Frame(root)
frame.grid()
root.title('ADD_adapter_test-port0')


class LabelEntry:
    
    def __init__(self, parent, label, column=0, row=0):
        self.label = tk.Label(parent, text=label).grid(column=column, row=row)
        self.entry = tk.Entry(parent, width=10).grid(column=column, row=row, padx=(120, 0))
    

class Composite1:
    def __init__(self, parent, label, column=0, row=0, start=0, stop=100, values=[1,2,3,4,5]):
        self.label1 = tk.Label(parent, text=label).grid(column=column, row=row, padx=(0,20))
        self.spinbox = tk.Spinbox(frame, from_=start, to=stop, width=6).grid(column=column, row=row, padx=(100,10))
        self.label2 = tk.Label(frame, text='V').grid(column=column, row=row, padx=(170,20))
        self.checkbutton = tk.Checkbutton(frame).grid(column=column, row=row, pady=(50,0), padx=(0,50))
        self.label3 = tk.Label(frame, text='Step').grid(column=column, row=row, pady=(50,0))
        self.combobox = Combobox(frame, values=values, width=6).grid(column=column, row=row, pady=(50,0), padx=(100,0))




tk.Radiobutton(frame, text='DIG_AD', value=2).grid(column=0, row=0)
tk.Button(frame, text='DIG_ADD_2').grid(column=0, row=1)
Composite1(frame, 'DAC_ADC', 0, 2, 0, 12, [1,2,3,4,5,6])
Composite1(frame, 'DAC_ADC', 0, 3, 0, 12, [1,2,3,4,5,6])
Composite1(frame, 'DAC_ADC', 0, 4, 0, 12, [1,2,3,4,5,6])
Composite1(frame, 'DAC_ADC', 0, 5, 0, 12, [1,2,3,4,5,6])
Composite1(frame, 'DAC_ADC', 0, 6, 0, 12, [1,2,3,4,5,6])
Composite1(frame, 'DAC_ADC', 0, 7, 0, 12, [1,2,3,4,5,6])
Composite1(frame, 'DAC_ADC', 0, 8, 0, 12, [1,2,3,4,5,6])
Composite1(frame, 'DAC_ADC', 0, 9, 0, 12, [1,2,3,4,5,6])



tk.Radiobutton(frame, text='DIG_AD', value=1).grid(column=1, row=0,)
tk.Button(frame, text='DIG_ADD_3').grid(column=1, row=1, padx=15)
LabelEntry(frame, 'ADC_ADC', 1, 2)
LabelEntry(frame, 'ADC_ADC', 1, 3)
LabelEntry(frame, 'ADC_ADC', 1, 4)
LabelEntry(frame, 'ADC_ADC', 1, 5)
tk.Radiobutton(frame, text='DAC_AD', value=3).grid(column=1, row=6)
LabelEntry(frame, 'DAC_ADC', 1, 7)
LabelEntry(frame, 'DAC_ADC', 1, 8)
LabelEntry(frame, 'DAC_ADC', 1, 9)
tk.Button(frame, text='DIG_DG_0').grid(column=1, row=10)
tk.Button(frame, text='DIG_DG_1').grid(column=1, row=11)
tk.Radiobutton(frame, text='DIG_DG', value=4).grid(column=1, row=12)
tk.Radiobutton(frame, text='DIG_DG', value=5).grid(column=1, row=13)
tk.Button(frame, text='DIG_ADD_4...').grid(column=1, row=14)
tk.Radiobutton(frame, text='DIG_AD', value=6).grid(column=1, row=15)
tk.Button(frame, text='DIG_ADD_4...').grid(column=1, row=16)
tk.Radiobutton(frame, text='DIG_AD', value=7).grid(column=1, row=17)



tk.Button(frame, text='PS_ON').grid(column=2, row=0, padx=20)
tk.Button(frame, text='STATUS_C...').grid(column=2, row=1)
tk.Button(frame, text='INTRLCK_C...').grid(column=2, row=2)
tk.Button(frame, text='ON2/IN11-O...').grid(column=2, row=3)
tk.Button(frame, text='PULSE2/IN1...').grid(column=2, row=4)
tk.Button(frame, text='ISO_EN').grid(column=2, row=5)
tk.Button(frame, text='SW_CLK/BU...').grid(column=2, row=6)
LabelEntry(frame, 'I_module', 2, 7)
Composite1(frame, 'INTR_LCK', 2, 8, 0, 12)
tk.Button(frame, text='ILD_SW').grid(column=2, row=9)

root.mainloop()
