import os, subprocess

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
        
        print(self.shares)

    def get_group_list(self, share):
        command = fr"Get-SmbShareAccess -Name '{share}' | Select-Object -ExpandProperty AccountName"
        response = subprocess.Popen(f"powershell.exe -Command \"& {{ {command} }}\"", 
                        stdout=subprocess.PIPE, text=True)

        output, _ = response.communicate()
        group_list = output.strip().splitlines()
        return group_list

shares()