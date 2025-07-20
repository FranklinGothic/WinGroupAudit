from command_executor import command

class filter_groups:
    def __init__(self, wanted_groups):
        self.wanted_groups = wanted_groups

        self.full_audit = command.read_json("full")
        self.filtered_audit = {}

    def filter_groups(self):
        """
        This will look through the groups to find if any of the wanted groups occur in any of the paths
        """
        for parent, child_groups in self.full_audit.items():
            if child_groups:
                all_paths = []
                for child_group, nested_data in child_groups.items(): 
                    if child_group:
                        paths = self._get_all_paths(nested_data, [child_group])
                        all_paths.extend(paths)

                matching_paths = []
                for path in all_paths:
                    if any(group in path for group in self.wanted_groups):
                        matching_paths.append(path)
                
                if matching_paths:
                    self.filtered_audit[parent] = matching_paths
        
        return self.filtered_audit

    def _get_all_paths(self, nested_dict, current_path):
        """
        This will look through the nested groups recusively and return all possible paths in that group
        """
        all_paths = []

        if isinstance(nested_dict, dict) and nested_dict:
            for group_name, sub_nested in nested_dict.items():
                new_path = current_path + [group_name]
                
                deeper_paths = self._get_all_paths(sub_nested, new_path)
                if deeper_paths:
                    all_paths.extend(deeper_paths)
                else:
                    all_paths.append(new_path)
        else:
            all_paths.append(current_path)
        
        return all_paths