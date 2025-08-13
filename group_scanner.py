from command_executor import command
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

class group_scanner:


    @staticmethod
    def process_single_group(parent_group, visited=None):
        """
        This will process a single group and return all nested groups
        """
        print(f"Working on {parent_group}")
        children_list = []
        
        commands = command.get_commands_yaml()
        get_children_cmd = commands["group_cmds"]["get_group_children"]

        children = command.powershell_execute(get_children_cmd.format(option=parent_group))
        print(children)

        if children:
            children_split = children.splitlines()
            for child in children_split:
                children_list.append(child.strip())

        return children_list