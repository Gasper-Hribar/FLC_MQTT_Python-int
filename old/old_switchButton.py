import tkinter as tk
root = tk.Tk()
class SwitchButton(tk.Checkbutton):
    ON_config = {'fg': 'red',
    'selectcolor': 'red'}

    OFF_config = {'fg': 'black',
    'selectcolor': 'white'}

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.pressed = False
        self.config = self.OFF_config
        self.config_button()
        self.bind("<Button-1>", self.press)

    def press(self, *args):
        if self.pressed:
            self.config = self.ON_config
            
        else:
            self.config = self.OFF_config

        self.pressed = not self.pressed
        return self.config_button()

    def config_button(self):
        self['fg'] = self.config['fg']
        self['selectcolor'] = self.config['selectcolor']
        return "break"
SwitchButton(root).pack()
root.mainloop()