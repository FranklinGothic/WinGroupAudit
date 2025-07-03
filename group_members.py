import os, subprocess

class group_members:
    def __init__(self):
         pass
    
    @staticmethod
    def get_members(group, add_distance):
        i = 0
        command = fr"Get-ADGroupMember -Identity '{group}' | Where-Object {{$_.objectClass -eq 'group'}} | Select-Object -ExpandProperty Name"
        response = subprocess.Popen(f"powershell.exe -Command \"& {{ {command} }}\"", 
                        stdout=subprocess.PIPE, text=True)
        output, _ = response.communicate()
        group_list = output.strip().splitlines()
        for group_name in group_list:
            i = 0
            while i < add_distance:
                print("\t", end="")
                i+=1
            print(f"\t - {group_name}")
            group_members.get_members(group_name, add_distance + 1)