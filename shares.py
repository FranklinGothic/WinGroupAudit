import os, subprocess
import time
from group_members import group_members

class shares:
    def __init__(self, group_name):
        self.shares_dictionary = {}
        
        self.selected_shares = self.get_share_selection()
        self.get_share_tree()
    
    def get_share_selection(self):
        self.clear_screen()
        #Gets all shares - ALL NAMES
        share_name_command = r"Get-SmbShare | Where-Object {$_.Name -notmatch '\$$'} | Select-Object -ExpandProperty Name"
        response = subprocess.Popen(f"powershell.exe -Command \"& {{ {share_name_command} }}\"", 
                        stdout=subprocess.PIPE, text=True)
        
        output, _ = response.communicate()    # Wait for the process to finish and get the output
        shares = output.strip().splitlines()


        keep_shares = []
        for print_share in shares:
            print(f"• {print_share}")
        print("Which shares would you like to audit?")
        print("[A] - ALL, [S] - Select specific shares, [R] - Select a range of shares")

        choice = input("")

        if choice.capitalize() == "A" or choice == "" or choice.capitalize() == "Y":
            keep_shares = shares
        elif choice.capitalize() == "S":
            self.clear_screen()
            while True:
                for print_share in shares:
                    print(f"• {print_share}")
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
            self.clear_screen()
            for print_share in shares:
                print(f"• {print_share}")
            print("Give a range of shares; e.x. (3-6)")
            range_input = input("")
            range_start = range_input[:range_input.find("-")]
            range_end = range_input[range_input.find("-")+1:]

            index = 1
            for share in shares:
                if int(range_start) <= index <= int(range_end):
                    keep_shares.append(share)
                index += 1
        print(keep_shares)
        return keep_shares
    
    def get_share_tree(self):
        for share in self.selected_shares:
            group_list = self.get_smb_group_list(share)
            self.shares[share] = group_list

        for share_name, g_list in self.shares.items():
            print(f"Who has permissions to <{share_name}>:")
            for group_name in g_list:
                print(f"\t  - {group_name}")
                group_members.get_members(group_name, 2)
            print("\n")

    def clear_screen(self):
        """
        clears screen - terminal
        """
        os.system("cls")


"""
        for share in shares:
            group_list = self.get_smb_group_list(share)
            self.shares[share] = group_list

        for share_name, g_list in self.shares.items():
            print(f"Who has permissions to <{share_name}>:")
            for group_name in g_list:
                print(f"\t  - {group_name}")
                group_members.get_members(group_name, 2)
            print("\n")

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
        return groups_to_keep
        """
