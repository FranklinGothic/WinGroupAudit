import os
from shares import shares

class main:
    def __init__(self):
        """
        Constructs the main object
        """
        self.audit_types = {"Shares": shares}

        self.audit_type_choice = self.get_audit_type()
        self.group_choice = self.get_group()
        self.conduct_audit()
    
    def get_audit_type(self):
        """
        Has the user define what type of audit they are conducting - terminal based
        """

        print("What would you like to audit?")

        for audit_type in self.audit_types.keys():
            print(f"• {audit_type}")

        choice = input("")
        while choice.capitalize() not in self.audit_types.keys():
            print("False input 💔. Please select one of our options!")
            choice = input("")

        self.clear_screen()
        return choice.capitalize()
    
    def get_group(self):
        """
        Has the user give the name of the group they are auditing - terminal based
        """
        print("What is the name of the 👥 group you are auditing?")
        choice = input("")

        return choice
    
    def conduct_audit(self):
        for type in self.audit_types.keys():
            if type == self.audit_type_choice:
                audit_instance = self.audit_types[type](self.group_choice)
    
    def clear_screen(self):
        """
        clears screen - terminal
        """
        os.system("cls")

if __name__ == "__main__":
    main()