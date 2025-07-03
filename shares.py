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
        shares = output.strip().split()
        groups = self.get_groups(shares)

        self.write_shares(shares, groups)

    def get_groups(self, shares):
        for share in shares:
            command = fr"Get-SmbShareAccess -Name '{share}'"
            response = subprocess.Popen(f"powershell.exe -Command \"& {{ {command} }}\"", 
                            stdout=subprocess.PIPE, text=True)

            groups, _ = response.communicate()
            print(groups)

    def write_shares(self, shares, groups):
        for share in shares:
            pass

shares()