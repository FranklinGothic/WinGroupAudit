import os, subprocess
from group_members import group_members

class shares:
    def __init__(self, group_name):
        self.shares_with_children = {}
        self.get_shares()
    
    def get_shares(self):
        #Gets all shares - ALL NAMES
        share_name_command = r"Get-SmbShare | Where-Object {$_.Name -notmatch '\$$'} | Select-Object -ExpandProperty Name"
        response = subprocess.Popen(f"powershell.exe -Command \"& {{ {share_name_command} }}\"", 
                        stdout=subprocess.PIPE, text=True)
        
        output, _ = response.communicate()    # Wait for the process to finish and get the output
        shares = output.strip().splitlines()

        for share in shares:
            group_list = self.get_smb_group_list(share)
            self.shares[share] = group_list
        """
        for share_name, g_list in self.shares.items():
            print(f"Who has permissions to <{share_name}>:")
            for group_name in g_list:
                print(f"\t  - {group_name}")
                group_members.get_members(group_name, 2)
            print("\n")
        """
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