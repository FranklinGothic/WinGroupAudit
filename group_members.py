import os, subprocess

class group_members:
    def __init__(self):
         pass
    
    @staticmethod
    def get_members(group):
        group_dict = {}
        command = fr"Get-ADGroupMember -Identity '{group}' | Where-Object {{$_.objectClass -eq 'group'}} | Select-Object -ExpandProperty Name"
        response = subprocess.Popen(f"powershell.exe -Command \"& {{ {command} }}\"", 
                        stdout=subprocess.PIPE, text=True)
        output, _ = response.communicate()
        group_list = output.strip().splitlines()
        for group_name in group_list:
            group_dict[group_name] = group_members.get_members(group_name)
        return group_dict