from command_executor import command

class group_scanner:

    @staticmethod
    def get_nested_groups(parent_group, visited=None):
        """
        This will return a dictionary of all of the nested groups inside of a particular group
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
            unfiltered_children_list = children_output.splitlines()
            filtered_children_list = []
            filter_children = commands["group_cmds"]["group_filtering"]
            for unfiltered_child in unfiltered_children_list:
                results = command.powershell_execute(filter_children.format(option=unfiltered_child))
                if results and results == "group":
                    filtered_children_list.append(unfiltered_child)
            
            for child in filtered_children_list:
                child = child.strip()
                if child:
                    child_groups[child] = group_scanner.get_nested_groups(child, visited.copy())

        return child_groups
