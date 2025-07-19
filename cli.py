import yaml, time
from share_scanner import shares
from command_executor import command

class cli:

    def __init__(self):
        self.audit_types = {"Shares": shares}

    def get_audit_type(self):
        """
        Has the user define what type of audit they are conducting
        """
        command.clear_screen()
        print("What would you like to audit?")

        for audit_type in self.audit_types.keys():
            print(f"• {audit_type}")

        choice = input("")
        while choice.capitalize() not in self.audit_types.keys():
            print("❌ False input. Please select one of our options!")
            choice = input("")

        return self.audit_types[choice.capitalize()]

    def get_group(self):
        """
        Has the user give the name of the group they are auditing
        """
        command.clear_screen()
        print("What is the name of the 👥 group you are auditing?")
        choice = input("")

        with open("system_cmds.yaml", "r") as file:
            commands = yaml.safe_load(file)
        check_cmd = commands["group_cmds"]["check_group_exists"]

        formatted_check_cmd = check_cmd.format(option=choice)
        result = command.powershell_execute(formatted_check_cmd)
        if result and result == "group":
            return result
        else:
            print("❌ This group does not exist. Please enter a valid group.")
            time.sleep(3)
            return self.get_group()
