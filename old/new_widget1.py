from distutils.cmd import Command
from functools import partial
from multiprocessing.sharedctypes import Value
import tkinter as tk
from tkinter.ttk import Combobox
import customtkinter as ctk
import pandas as pd

frame = ctk.CTk()
frame.grid()

class Widget1:

    def __init__(self, parent, label, column=0, row=0, values=[0.1, 0.01, 1]):
        
        row1 = row + 1
        self.var1 = 0
        self.writeVal = ctk.StringVar(value=0)
        self.values = [str(a) for a in values]
        self.noStepSelected = True
        self.checkboxVal = ctk.BooleanVar(parent, value=True)
        self.increment = ctk.IntVar(parent, value=1)
        self.textvar = ctk.IntVar(parent, value=100)

        self.label1 = ctk.CTkLabel(parent, text=label).grid(column=column, row=row, padx=(0,150))

        self.button1 = ctk.CTkButton(parent, width=40, border_width=2, fg_color=None, command=self.increase, text='>')
        self.button1.grid(column=column, row=row, padx=(200,0))

        self.button2 = ctk.CTkButton(parent, width=40, border_width=2, fg_color=None, command=self.decrease, text='<')
        self.button2.grid(column=column, row=row, padx=(0,30))

        self.entry = ctk.CTkEntry(parent, width=70, state='readonly', textvariable=self.writeVal)
        self.entry.grid(column = column, row = row, padx=(100,14.495))

        self.checkbutton = ctk.CTkCheckBox(parent, variable=self.checkboxVal, command=self.checkbox, text="")
        self.checkbutton.grid(column=column, row=row1, padx=(0,50))
        
        self.combobox = ctk.CTkComboBox(parent, width=130, variable = self.increment, command=self.config_increment, values=self.values)
        self.combobox['width'] = 6
        self.combobox.grid(column=column, row=row1, padx=(110,0))
        # self.combobox.bind('<<ComboboxSelected>>', self.config_increment)
        

    def checkbox(self):
        if self.checkboxVal.get():
            self.combobox.configure(state=tk.NORMAL)
            self.entry.configure(state='readonly')
            self.button1.configure(state=tk.NORMAL)
            self.button2.configure(state=tk.NORMAL)
            self.var1 = 0
        else:
            self.combobox.configure(state=tk.DISABLED)
            self.entry.configure(state=tk.DISABLED)
            self.button1.configure(state=tk.DISABLED)
            self.button2.configure(state=tk.DISABLED)
            self.writeVal.set('0')
    def increase(self):
        if self.noStepSelected:
            self.var1 += self.increment.get()
            to_display = '{:.2f}'.format(self.var1)
            self.writeVal.set(to_display)
            print(self.var1)
        else:
            self.var1 += self.increment
            to_display = '{:.2f}'.format(self.var1)
            self.writeVal.set(to_display)
            print(self.var1)
    def decrease(self):
        if self.noStepSelected:
            self.var1 -= self.increment.get()
            if self.var1 < 0:
                self.var1 = 0
            to_display = '{:.2f}'.format(self.var1)
            self.writeVal.set(to_display)
            print(self.var1)
        else:
            self.var1 -= self.increment
            if self.var1 < 0:
                self.var1 = 0
            to_display = '{:.2f}'.format(self.var1)
            self.writeVal.set(to_display)
            print(self.var1)

    def config_increment(self, event):
        self.noStepSelected = False
        self.increment = float(self.combobox.get())


Widget1(frame, 'DAC_ADC', 0, 2, [0.1, 0.01, 1])

frame.mainloop()