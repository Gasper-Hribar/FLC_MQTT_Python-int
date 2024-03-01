import tkinter as tk
import FLC_command as flc

class Button(tk.Button):

    ON_config = {'bg': 'green',
                 'relief': 'sunken',
                 }
    OFF_config = {'bg': 'white',
                 'relief': 'raised',
                 }
    
    def __init__(self, parent, toggleVal, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.toggleVal = toggleVal
        self.toggled = False
        self.config = self.OFF_config
        self.config_button()
        if self.toggleVal == True:
            self.bind("<Button-1>", self.toggle)

    def toggle(self, *args):
        if self.toggled:
            self.config = self.OFF_config
        else:
            self.config = self.ON_config
        
        self.toggled = not self.toggled
        return self.config_button()

    def config_button(self):
        self['bg'] = self.config['bg']
        self['relief'] = self.config['relief']
        return "break"

    def __str__(self):
        return f"{self['bg']}, {self['relief']}"

class ButtonAndText(tk.Label, Button):
    def __init__(self, frame, tgVal=0, textL=0):
        tk.Label.__init__(self, master=frame, text=textL)
        Button.__init__(self, frame, toggleVal=tgVal)
        self.tgVal = tgVal
        self.textL = textL
        self.frame = frame
        self.new_widget()
    def new_widget(self):
        tk.Label(master=frame, text=self.textL).grid(column=0, row=3)
        Button(frame, toggleVal=self.tgVal).grid(column=1, row=3)


root = tk.Tk()
frame = tk.Frame(root)
frame.grid()

Button(frame, toggleVal=1, text='DIG_AD').grid(column=0, row=0)
#tk.Label(frame, text="DIG_AD").grid(column=1, row=0)
Button(frame, toggleVal=1, text='DIG_AD').grid(column=1, row=0,)
#tk.Label(frame, text='DIG_AD').grid(column=3, row=0)
Button(frame, toggleVal=1, text='PS_ON').grid(column=2, row=0, padx=20)
Button(frame, toggleVal=1, text='DIG_ADD_2').grid(column=0, row=1)
Button(frame, toggleVal=1, text='DIG_ADD_3').grid(column=1, row=1, padx=15)
Button(frame, toggleVal=1, text='STATUS_C...').grid(column=2, row=1)
Button(frame, toggleVal=1, text='INTRLCK_C...').grid(column=2, row=2)
Button(frame, toggleVal=1, text='ON2/IN11-O...').grid(column=2, row=3)
Button(frame, toggleVal=1, text='PULSE2/IN1...').grid(column=2, row=4)
Button(frame, toggleVal=1, text='ISO/EN').grid(column=2, row=5)
Button(frame, toggleVal=1, text='SW_CLK/BU...').grid(column=2, row=6)

#tk.Checkbutton(frame).grid(column=0, row=2)
#tk.Entry(frame,width=5,textvariable = tk.StringVar(), font=('calibre',10,'normal')).grid(column=2, row=2)
#tk.Button(frame, text='<').grid(column=1, row=2)
#tk.Button(frame, text='>').grid(column=3, row=2)
#ButtonAndText(frame, tgVal=1, textL='DIG_AD')




root.mainloop()




#root = Tk()
#frm = ttk.Frame(root, padding=10)
#frm.grid()
#ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
#ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
#root.mainloop()