import os, subprocess

class group_members:

    @staticmethod
    def get_members(group, wanted_group, visited=None):
        if visited is None:
            visited = set()
        
        # Prevent infinite recursion by checking if we've already processed this group
        if group in visited:
            return {}
        
        visited.add(group)
        
        group_dict = {}
        command = fr"Get-ADGroupMember -Identity '{group}' | Where-Object {{$_.objectClass -eq 'group'}} | Select-Object -ExpandProperty Name"
        response = subprocess.Popen(f"powershell.exe -Command \"& {{ {command} }}\"", 
                        stdout=subprocess.PIPE, text=True)
        output, _ = response.communicate()
        group_list = output.strip().splitlines()
        
        for group_name in group_list:
            # Pass a copy of visited set to maintain the tracking through recursion
            group_dict[group_name] = group_members.get_members(group_name, visited.copy())
        
        return group_dict