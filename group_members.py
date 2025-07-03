import os, subprocess

class group_members:
    def __init__(self, group):
        self.group = group
        self.get_members()
    
    def get_members(self):

        command = fr"Get-ADGroupMember -Identity '{self.group}' -Recursive | Where-Object {{ $_.objectClass -eq 'group' }} | Select-Object -ExpandProperty Name"
        response = subprocess.Popen(f"powershell.exe -Command \"& {{ {command} }}\"", 
                        stdout=subprocess.PIPE, text=True)
        
        output, _ = response.communicate()    # Wait for the process to finish and get the output
        print(output.strip())