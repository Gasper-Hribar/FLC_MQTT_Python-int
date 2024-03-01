#Import the required librar
from ast import Num
from email import generator, message
import tkinter as tk
from tkinter import messagebox
import time
from random import randint
#Create an instance of tkinter frame or window
win = tk.Tk()

new_val = tk.StringVar()


def handle_click(btnType):
    if btnType == 'SwitchButton':
        print("Switchbutton was called!")
        
        new_val.set(f'{randint(0,100)} V')
        win.update_idletasks()
    elif btnType == 'ColorButton':
        print("ColorButton function was called")
        new_val.set(f'{randint(0,100)} V')
        win.update_idletasks()

class SwitchButton(tk.Radiobutton):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.pressed = True
        self.bind("<Button-1>", self.press)

    def press(self, *args):
        if self.pressed:
            self['fg'] = 'black'
            self['selectcolor'] = 'red'
            #self.messagef()
            handle_click("SwitchButton")
            #self.handle_click1("SwitchButton")
        else:
            self['fg'] = 'black'
            self['selectcolor'] = 'white'
        self.pressed = not self.pressed

    def handle_click1(self, btnType):
        new_val = tk.StringVar()
        if btnType == 'SwitchButton':
            print('SwitchButton was called!')
            new_val.set(f'{randint(0,100)} V')
            
        elif btnType == 'ColorButton':
            print("ColorButton function was called")
            new_val.set(f'{randint(0,100)} V')
        win.update_idletasks()

class LabelEntry:
    
    def __init__(self, parent, label, text, column=0, row=0):
        self.label = tk.Label(parent, text=label).grid(column=column, row=row)
        self.entry = tk.Entry(parent, textvariable=text, state='readonly', width=10).grid(column=column, row=row, padx=(120, 0))
        


SwitchButton(win, text='DIG_AD').grid(column=0, row=0)

LabelEntry(win, "TEST", new_val, column=0, row=1)

win.mainloop()

