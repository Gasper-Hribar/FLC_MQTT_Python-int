from tkinter import Spinbox
import tkinter as tk
root = tk.Tk()
def print_item_values():
    print(item_1.get())
item_1 = Spinbox(root, from_= 0, to = 10, command=print_item_values, width = 5)
item_1.grid(row = 0, column = 0)



root.mainloop()