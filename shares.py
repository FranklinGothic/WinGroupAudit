import os, subprocess
import time
from group_members import group_members

class shares:
    def __init__(self, group_name):
        self.shares_dictionary = {}
        
        self.selected_shares = self.get_share_selection()
        self.get_share_tree()
        self.print_shares_dictionary()  # Replace the print statement with this

    def print_shares_dictionary(self):
        """
        Prints the shares dictionary in a formatted, readable way
        """
        print("\n" + "="*60)
        print("SHARE AUDIT RESULTS")
        print("="*60)
        
        for share_name, groups in self.shares_dictionary.items():
            print(f"\n📁 SHARE: {share_name}")
            print("-" * (len(share_name) + 8))
                
            for group_name, nested_groups in groups.items():
                print(f"   👥 GROUP: {group_name}")
                
                if not nested_groups:
                    print("      └── No nested groups")
                else:
                    self._print_nested_groups(nested_groups, indent="      ")
    
        print("\n" + "="*60)

    def _print_nested_groups(self, groups_dict, indent=""):
        """
        Recursively prints nested groups with proper indentation
        """
        for group_name, sub_groups in groups_dict.items():
            print(f"{indent}└── {group_name}")
            if sub_groups:
                self._print_nested_groups(sub_groups, indent + "    ")

    def get_share_selection(self):
        self.clear_screen()
        #Gets all shares - ALL NAMES
        share_name_command = r"Get-SmbShare | Where-Object {$_.Name -notmatch '\$$'} | Select-Object -ExpandProperty Name"
        response = subprocess.Popen(f"powershell.exe -Command \"& {{ {share_name_command} }}\"", 
                        stdout=subprocess.PIPE, text=True)
        
        output, _ = response.communicate()    # Wait for the process to finish and get the output
        shares = output.strip().splitlines()


        return_shares = self.user_share_selection(shares)
        return return_shares

    def user_share_selection(self, shares):
        keep_shares = []
        for print_share in shares:
            print(f"• 📁 {print_share}")
        print("Which shares would you like to audit?")
        print("[A] - ALL, [S] - Select specific shares, [R] - Select a range of shares")

        choice = input("")

        if choice.capitalize() == "A" or choice == "" or choice.capitalize() == "Y":
            keep_shares = shares
        elif choice.capitalize() == "S":
            self.clear_screen()
            while True:
                for print_share in shares:
                    print(f"• 📁 {print_share}")
                print("Please select one share at a time.")
                share_choice = input("")
                a_share = False
                for share in shares:
                    if share_choice == share:
                        a_share = True
                        keep_shares.append(share)

                if not a_share:
                    print("Not a share. Please make sure share exists.")
                    time.sleep(2)
                    self.clear_screen()
                    continue
                
                print("Would you like to enter another share? [Y or N]")
                end_choice = input("")
                self.clear_screen()
                if end_choice.capitalize() == "N":
                    break
    
        elif choice.capitalize() == "R":
            while True:
                self.clear_screen()
                for print_share in shares:
                    print(f"• 📁 {print_share}")
                print("Give a range of shares; e.x. (3-6)")
                range_input = input("")
                range_start = range_input[:range_input.find("-")]
                range_end = range_input[range_input.find("-")+1:]
                if int(range_start) > len(shares) + 1 or int(range_end) > len(shares) + 1 or int(range_start) > int(range_end):
                    print("❌ Please enter a valid range.")
                    time.sleep(3)
                else:
                    break


            index = 1
            for share in shares:
                if int(range_start) <= index <= int(range_end):
                    keep_shares.append(share)
                index += 1
        else:
            print("❌ Please choose one of our demonstated options.")
            time.sleep(3)
            self.clear_screen()
            keep_shares = self.user_share_selection(shares)
        self.clear_screen()
        return keep_shares
        
    
    
    def get_share_tree(self):
        for share in self.selected_shares:
            self.get_smb_group_list(share)

    def get_smb_group_list(self, share):
        #Get all groups associated with that share
        share_group_command = fr"Get-SmbShareAccess -Name '{share}' | ForEach-Object {{ $_.AccountName -replace '^.*\\', '' }}"
        response = subprocess.Popen(f"powershell.exe -Command \"& {{ {share_group_command} }}\"", 
                        stdout=subprocess.PIPE, text=True)

        output, _ = response.communicate()
        group_list = output.strip().splitlines()
        groups_to_keep = []
        for group in group_list:
            check_group_command = fr"Get-ADObject -Filter {{ SamAccountName -eq '{group}' }} -Properties objectClass | Select-Object -ExpandProperty ObjectClass"
            response = subprocess.Popen(f"powershell.exe -Command \"& {{ {check_group_command} }}\"", 
                            stdout=subprocess.PIPE, text=True)

            output, _ = response.communicate()
            if output.strip() == "group":
                groups_to_keep.append(group)
        
        self.shares_dictionary[share] = self.get_nested_groups(groups_to_keep)

    def get_nested_groups(self, resolved_groups):
        group_dict = {}
        for group in resolved_groups:
            group_dict[group] = group_members.get_members(group)
        return group_dict 

    def clear_screen(self):
        """
        clears screen - terminal
        """
        os.system("cls")

