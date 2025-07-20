from command_executor import command
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

class group_scanner:


    @staticmethod
    def _process_single_group(parent_group, top_level_group, visited=None):
        """
        This will process a single group and return all nested groups
        """
        if visited is None:
            visited = set()
        
        # Prevent infinite recursion
        if parent_group in visited:
            return {}
        
        visited.add(parent_group)

        commands = command.get_commands_yaml()
        get_children_cmd = commands["group_cmds"]["get_group_children"]

        children_output = command.powershell_execute(get_children_cmd.format(option=parent_group))

        child_groups = {}

        if children_output:
            children_list = children_output.splitlines()
            
            for child in children_list:
                child = child.strip()
                if child:
                    child_groups[child] = group_scanner._process_single_group(child, False, visited.copy())
        if top_level_group:
            return parent_group, child_groups
        else:
            return child_groups

    @staticmethod
    def get_nested_groups(parent_groups, max_workers=5): #create more threads for thoretical greater speed but may cause degregration if too many
        """
        This will return a dictionary of all of the nested groups inside of a particular group and process in parallel
        """
        group_data = {}
        lock = threading.Lock()
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures_to_execute = [
                executor.submit(group_scanner._process_single_group, parent, True) for parent in parent_groups
            ]
        
        for future in as_completed(futures_to_execute):
            parent_data, child_data = future.result()
            with lock:
                group_data[parent_data] = child_data
        
        return group_data