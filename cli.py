from command_executor import command
import time, sys

class genrl_cli:

    def __init__(self):
        self.audit_types = ["Shares"]

    def get_audit_type(self):
        """
        Has the user define what type of audit they are conducting - unused for now as shares are the only option
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
    
    def get_groups(self):
        """
        Has the user give the name of the group(s) they are auditing
        """
        selected_groups = []
        
        while True:
            command.clear_screen()
            print("What is the name of the [GROUP(S)] you are auditing?")
            
            if selected_groups:
                print(f"\nCurrently selected: {len(selected_groups)} groups")
                print(f"Selected: {', '.join(selected_groups)}")
            
            print("\nEnter group name (or 'done' to finish, 'clear' to reset):")
            choice = input("").strip()
            
            # SPECIAL COMMANDS
            if choice.lower() == 'done':
                if selected_groups:
                    break
                else:
                    print("❌ Please select at least one group.")
                    time.sleep(2)
                    continue
            elif choice.lower() == 'clear':
                selected_groups.clear()
                print("✅ Selection cleared!")
                time.sleep(1)
                continue
            elif not choice:
                print("❌ Please enter a group name.")
                time.sleep(1)
                continue

            # Validate group exists
            commands = command.get_commands_yaml()
            check_cmd = commands["group_cmds"]["check_group_exists"]
            formatted_check_cmd = check_cmd.format(option=choice)
            result = command.powershell_execute(formatted_check_cmd)
            
            if result and result.strip() == "group":
                if choice not in selected_groups:
                    selected_groups.append(choice)
                    print(f"✅ Added '{choice}' to selection!")
                else:
                    print(f"⚠️ '{choice}' is already selected.")
            else:
                print(f"❌ '{choice}' does not exist. Please enter a valid group.")
            
            time.sleep(1)
        
        return selected_groups

class share_cli:

    def __init__(self):
        self.keep_shares = []
        self.share_list = None
    
    def _print_shares(self):
        """
        Prints out the shares in order so the user can add them to their audit
        """
        for i, print_share in enumerate(self.share_list, 1):
            print(f"{i}. [SHARE] {print_share}")

    def get_share_selection(self):
        """
        If the user selects to audit the shares this will prompt them to select if they want to audit specific shares
        """
        command.clear_screen()

        commands = command.get_commands_yaml()
        get_shares = commands["share_cmds"]["get_all_shares"]

        result = command.powershell_execute(get_shares)
        self.share_list = result.splitlines()

        self._print_shares()
        print("Which shares would you like to audit?")
        print("[A] - ALL, [S] - Select specific shares, [R] - Select a range of shares")

        choice = input("")

        if choice.capitalize() == "A" or choice.capitalize() == "Y" or choice == "":
            return self.share_list
        elif choice.capitalize() == "S":
            return self._select_shares()
        elif choice.capitalize() == "R":
            return self._range_of_shares()
        else:
            print("❌ Please choose one of our options.")
            time.sleep(3)
            return self.get_share_selection()
    
    def _select_shares(self):
        """
        Allows user to select specific shares from the available list

        Claude Sonnet 4 was used in this method to aid in user error handling and better and clearer messages
        """
        command.clear_screen()
        
        while True:
            self._print_shares()
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
    
    def _range_of_shares(self):
        """
        Allows user to select a range of shares by index numbers

        Claude Sonnet 4 was used in this method to aid in user error handling because the amount of ways someone can enter a number
        wrong is astounding
        """
        while True:
            command.clear_screen()
            self._print_shares()
            
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
                command.clear_screen()
                print(f"✅ Selected {len(selected_shares)} shares:")
                for share in selected_shares:
                    print(f"  • {share}")
                
                time.sleep(2)
                return selected_shares
                
            except ValueError:
                print("❌ Please enter valid numbers (e.g., 1-3)")
                time.sleep(2)
                continue

class data_present_cli:
    def __init__(self, audit_type):
        self.audit_type = audit_type

        self.all_data = command.read_json("full")
        self.filtered_data = command.read_json("filtered")
        self.RED = '\033[91m'
        self.RESET = '\033[0m'

    def present(self):
        """
        Determines how data will be presented to the user
        """
        command.clear_screen()
        self._general_print()

    def _print_case(self, special_distinction):
        """
        Prints the data in a formatted, readable way - For share audits
        """
        target_groups = self._get_target_groups()
        
        for share_name, groups in self.all_data.items():
            print(f"\n{special_distinction}: {share_name}")
            print("-" * (len(share_name) + 8))
                
            for group_name, nested_groups in groups.items():
                # Check if this top-level group leads to targets
                is_path_to_target = self._contains_target_groups(group_name, nested_groups, target_groups)
                
                if is_path_to_target:
                    print(f"   [GROUP]: {self.RED}{group_name}{self.RESET}")
                else:
                    print(f"   [GROUP]: {group_name}")
                
                if not nested_groups:
                    print("      └── No nested groups")
                else:
                    self._general_nested_print(nested_groups, indent="      ", target_groups=target_groups)

    def _general_print(self):
        """
        Prints the data in a formatted, readable way
        """
        print("\n" + "="*60)
        print("AUDIT RESULTS")
        print("="*60)

        match self.audit_type:

            case "Shares":
                self._print_case("[SHARE]")

        print("\n" + "="*60)

        input("\nEnter to exit.")
        print("\nExiting...")
        time.sleep(3)
        sys.exit()

    def _general_nested_print(self, nested_groups, indent, target_groups=None):
        """
        Gets all nested groups under a group for printing with highlighting
        """
        if target_groups is None:
            # Get target groups from filtered data or somewhere else
            target_groups = self._get_target_groups()
        
        for group_name, sub_groups in nested_groups.items():
            # Check if this group or any nested groups contain target groups
            is_path_to_target = self._contains_target_groups(group_name, sub_groups, target_groups)
            
            if is_path_to_target:
                print(f"{indent}└── {self.RED}{group_name}{self.RESET}")
            else:
                print(f"{indent}└── {group_name}")
                
            if sub_groups:
                self._general_nested_print(sub_groups, indent + "    ", target_groups)

    def _contains_target_groups(self, current_group, nested_dict, target_groups):
        """
        Check if current group or any nested groups contain target groups
        """
        # Check current group
        if current_group in target_groups:
            return True
        
        # Check nested groups recursively
        if isinstance(nested_dict, dict):
            for group_name, sub_nested in nested_dict.items():
                if self._contains_target_groups(group_name, sub_nested, target_groups):
                    return True
        
        return False

    def _get_target_groups(self):
        """
        Extract target groups from filtered data or get from main class
        """
        # Option 1: Extract from filtered data
        target_groups = set()
        for share_name, groups in self.filtered_data.items():
            if isinstance(groups, list):
                # If your filtered data is in list format
                for path in groups:
                    target_groups.update(path)
            elif isinstance(groups, dict):
                # If your filtered data is in dict format
                target_groups.update(groups.keys())
        
        return target_groups