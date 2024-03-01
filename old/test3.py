from functools import partial
import tkinter as tk
from time import sleep
import sys
from tkinter.ttk import Combobox
frame = tk.Tk()




class Composite1:

    def __init__(self, parent, label, column=0, row=0, start=0, stop=100, values=[0, 0.1, 0.01, 1, 2, 10]):

        var1 = tk.IntVar(value=1)
        self.label1 = tk.Label(parent, text=label).grid(column=column, row=row, padx=(0,20))
        self.label2 = tk.Label(parent, text='V').grid(column=column, row=row, padx=(150,20))
        self.label3 = tk.Label(parent, text='Step').grid(column=column, row=row, pady=(50,0))

        self.spinbox = tk.Spinbox(parent)
        self.spinbox.grid(column=column, row=row, padx=(100,10))
        self.spinbox['from_'] = start
        self.spinbox['to'] = stop
        self.spinbox['width'] = 6
        self.spinbox['command'] = self.set_value

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

        
Composite1(frame, "Composite")
frame.mainloop()