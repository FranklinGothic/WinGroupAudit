from command_executor import command
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

class group_scanner:


    @staticmethod
    def process_single_group(parent_group, visited=None):
        """
        This will process a single group and return all nested groups
        """
        children_dict = {}
        
        commands = command.get_commands_yaml()
        get_children_cmd = commands["group_cmds"]["get_group_children"]

        children = command.powershell_execute(get_children_cmd.format(option=parent_group))

        if children:
            children_list = children.splitlines()
            for child in children_list:
                child = child.strip()
                if child:
                    children_dict[parent_group] = child

        return children_dict