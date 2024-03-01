import tkinter as tk
from tkinter import ttk
from functools import partial
 
class Window:
    def __init__(self, root):
        self.box = ttk.Combobox(root)
        self.box['values'] = [1,2,3,4,5,6,7,8,9]
        self.box.current(0)
        self.box.pack()
 
        bt1 = tk.StringVar()
        self.chkbtn = ttk.Checkbutton(root, text='Enable')
        self.chkbtn.pack(side='left')
        self.chkbtn['variable'] = bt1
        self.chkbtn['onvalue'] = 'on'
        self.chkbtn['offvalue'] = 'off'
        self.chkbtn['command'] = partial(self.update, bt1)
 
 

    def update(self, var):
        btn = var.get()
        if btn == 'on':
            self.box.configure(state='disabled')
            self.chkbtn['text'] = 'Disable'
        else:
            self.box.configure(state='normal')
            self.chkbtn['text'] = 'Enable'
 
 
 
def main():
    root = tk.Tk()
    Window(root)
    root.mainloop()
 
main()