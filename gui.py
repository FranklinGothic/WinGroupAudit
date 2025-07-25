from command_executor import command
import tkinter as tk
from tkinter import Frame
import time, sys, string

class App:
    def __init__(self):
        root = tk.Tk()
        root.title("Windows Group Audit")
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        main_frame = tk.Frame(root, padx=2, pady=2)
        main_frame.grid(column=0, row=0, sticky="NWES")

        root.mainloop()


