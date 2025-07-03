import os, subprocess
from group_members import group_members

class shares:
    def __init__(self):
        self.shares = {}

        self.get_shares()
    
    def get_shares(self):
        command = r"Get-SmbShare | Where-Object {$_.Name -notmatch '\$$'} | Select-Object -ExpandProperty Name"
        response = subprocess.Popen(f"powershell.exe -Command \"& {{ {command} }}\"", 
                        stdout=subprocess.PIPE, text=True)
        
        output, _ = response.communicate()    # Wait for the process to finish and get the output
        shares = output.strip().splitlines()

        for share in shares:
            group_list = self.get_group_list(share)
            self.shares[share] = group_list
        
        for share_name, g_list in self.shares.items():
            print(f"Who has permissions to <{share_name}>:")
            for group_name in g_list:
                group_members(group_name)
                print(f"\t  - {group_name}")

    def get_group_list(self, share):
        command = fr"Get-SmbShareAccess -Name '{share}' | Select-Object -ExpandProperty AccountName"
        response = subprocess.Popen(f"powershell.exe -Command \"& {{ {command} }}\"", 
                        stdout=subprocess.PIPE, text=True)

        output, _ = response.communicate()
        group_list = output.strip().splitlines()
        return group_list

shares()