from share_scanner import shares
from command_executor import command
import time

class genrl_cli:

    def __init__(self):
        self.audit_types = ["Shares"]

    def get_audit_type(self):
        """
        Has the user define what type of audit they are conducting
        """
        command.clear_screen()
        print("What would you like to audit?")

        for audit_type in self.audit_types:
            print(f"• {audit_type}")

        choice = input("")
        while choice.capitalize() not in self.audit_types:
            print("❌ False input. Please select one of our options!")
            choice = input("")

        return choice.capitalize()

    def get_group(self):
        """
        Has the user give the name of the group they are auditing
        """
        command.clear_screen()
        print("What is the name of the 👥 group you are auditing?")
        choice = input("")

        commands = command.get_commands_yaml()
        check_cmd = commands["group_cmds"]["check_group_exists"]

        formatted_check_cmd = check_cmd.format(option=choice)
        result = command.powershell_execute(formatted_check_cmd)
        if result and result == "group":
            return choice
        else:
            print("❌ This group does not exist. Please enter a valid group.")
            time.sleep(3)
            return self.get_group()

class share_cli:

    def __init__(self):
        self.keep_shares = []
        self.share_list = None
    
    def print_shares(self):
        """
        Prints out the shares in order so the user can add them to their audit
        """
        for i, print_share in enumerate(self.share_list, 1):
            print(f"{i}. 📁 {print_share}")

    def get_share_selection(self):
        """
        If the user selects to audit the shares this will prompt them to select if they want to audit specific shares
        """
        command.clear_screen()

        commands = command.get_commands_yaml()
        get_shares = commands["share_cmds"]["get_all_shares"]

        result = command.powershell_execute(get_shares)
        self.share_list = result.splitlines()

        self.print_shares()
        print("Which shares would you like to audit?")
        print("[A] - ALL, [S] - Select specific shares, [R] - Select a range of shares")

        choice = input("")

        if choice.capitalize() == "A" or choice.capitalize() == "Y" or choice == "":
            return self.share_list
        elif choice.capitalize() == "S":
            return self.select_shares()
        elif choice.capitalize() == "R":
            return self.range_of_shares()
        else:
            print("❌ Please choose one of our options.")
            time.sleep(3)
            return self.get_share_selection()
    
    def select_shares(self):
        """
        Allows user to select specific shares from the available list

        Claude Sonnet 4 was used in this method to aid in user error handling and better and clearer messages
        """
        command.clear_screen()
        
        while True:
            self.print_shares()
            print(f"\nCurrently selected: {len(self.keep_shares)} shares")
            if self.keep_shares:
                print(f"Selected: {', '.join(self.keep_shares)}")
            
            print("\nEnter share name (or 'done' to finish, 'clear' to reset):")
            share_choice = input("").strip()
            
            # SPECIAL COMMANDS
            if share_choice.lower() == 'done':
                break
            elif share_choice.lower() == 'clear':
                self.keep_shares.clear()
                print("✅ Selection cleared!")
                time.sleep(1)
                command.clear_screen()
                continue
            elif not share_choice:
                print("❌ Please enter a share name.")
                time.sleep(1)
                command.clear_screen()
                continue
            
            # Check if share exists and isn't already selected
            if share_choice in self.share_list:
                if share_choice not in self.keep_shares:
                    self.keep_shares.append(share_choice)
                    print(f"✅ Added '{share_choice}' to selection!")
                else:
                    print(f"⚠️ '{share_choice}' is already selected.")
            else:
                print(f"❌ '{share_choice}' is not a valid share.")
                
            time.sleep(1)
            command.clear_screen()
        
        return self.keep_shares
    
    def range_of_shares(self):
        """
        Allows user to select a range of shares by index numbers

        Claude Sonnet 4 was used in this method to aid in user error handling because the amount of ways someone can enter a number
        wrong is astounding
        """
        while True:
            command.clear_screen()
            self.print_shares()
            
            print(f"Enter a range (e.g., 1-3 or 2-5). Valid range: 1-{len(self.share_list)}")
            range_input = input("").strip()
            
            # Validate input format
            if "-" not in range_input:
                print("❌ Please use format: start-end (e.g., 1-3)")
                time.sleep(2)
                continue
            
            try:
                # Parse the range
                range_parts = range_input.split("-")
                if len(range_parts) != 2:
                    raise ValueError("Invalid range format")
                
                range_start = int(range_parts[0].strip())
                range_end = int(range_parts[1].strip())
                
                # Validate range bounds
                if range_start < 1 or range_end < 1:
                    print("❌ Range must start from 1 or higher.")
                    time.sleep(2)
                    continue
                
                if range_start > len(self.share_list) or range_end > len(self.share_list):
                    print(f"❌ Range cannot exceed {len(self.share_list)}.")
                    time.sleep(2)
                    continue
                
                if range_start > range_end:
                    print("❌ Start number must be less than or equal to end number.")
                    time.sleep(2)
                    continue
                
                # Extract the selected shares (convert to 0-based indexing)
                selected_shares = self.share_list[range_start-1:range_end]
                
                print(f"✅ Selected {len(selected_shares)} shares:")
                for share in selected_shares:
                    print(f"  • {share}")
                
                time.sleep(2)
                return selected_shares
                
            except ValueError:
                print("❌ Please enter valid numbers (e.g., 1-3)")
                time.sleep(2)
                continue