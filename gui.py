from command_executor import command
import tkinter as tk #Frame, RadioButton, Button
import time, sys, string

class App:
    def __init__(self):
        self.audit_types = ["Shares", "DemoA", "DemoB"]
        self.audit_type = None

        self.confimed_groups = []

        self.root = tk.Tk()
        self.init_gui()

        self.main_frame = tk.Frame(self.root, padx=2, pady=2)
        self.main_frame.grid(column=0, row=0, sticky="NWES")

    def init_gui(self):
        """
        This sets up the gui so it doesnt clutter up the constructor
        """
        self.root.title("Windows Group Audit")
        self.root.geometry("900x600")
        self.root.minsize(600, 400)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

    def get_audit_type(self):
        """
        This sets up the audit type screen and adds all of the options that they choose
        """
        command.clear_screen_gui(self.main_frame)
        selected_value = tk.StringVar()

        for i in range(3):
            self.main_frame.columnconfigure(i, weight=1)

        for i, option in enumerate(self.audit_types):
            radio_button = tk.Radiobutton(self.main_frame, text=option, variable=selected_value, value=option)
            radio_button.grid(column=1, row=i, sticky="WENS")
        
        next_button = tk.Button(self.main_frame, text="Next", command=lambda: self.handle_audit_selection(selected_value.get()))
        next_button.grid(column=2, row=len(self.audit_types), pady=10)

        self.root.mainloop()

    def handle_audit_selection(self, selection):
        """
        This changes the audit type to the option that they choose
        """
        if selection:
            self.audit_type = selection
            self.root.quit()
        else:
            print("please make a selection!")
    
    def get_groups(self):
        command.clear_screen_gui(self.main_frame)

        selected_group = tk.StringVar()

        group_entry = tk.Entry(self.main_frame, textvariable=selected_group)
        group_entry.grid(column=1, row=0, padx=10, pady=10, sticky="EWS")

        add_button = tk.Button(self.main_frame, text="Add", command=lambda: self.add_group(selected_group.get()))
        add_button.grid(column=0, row=1, padx=10, pady=5, sticky="EW")

        self.root.mainloop()

    def add_group(self, group):
        commands = command.get_commands_yaml()
        check_cmd = commands["group_cmds"]["check_group_exists"]
        formatted_check_cmd = check_cmd.format(option=group)
        result = command.powershell_execute(formatted_check_cmd)
        
        if result and result.strip() == "group":
            if group not in self.confimed_groups:
                self.confimed_groups.append(group)
        print(self.confimed_groups)




