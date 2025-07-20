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
                for child_group, nested_data in child_groups.items(): 
                    if child_group:
                        path_start = []
                        path_start.append(child_group)

                        final_path = self._filter_nested_groups(nested_data, path_start)
                        if any(group in final_path for group in self.wanted_groups):
                            self.filtered_audit[parent] = final_path
    
        return self.filtered_audit

    def _filter_nested_groups(self, nested_dict, current_path):
        """
        This will look through the nested groups and add them to the path
        """
        processing_path = current_path.copy() 
        
        if isinstance(nested_dict, dict):
            for group_name, sub_nested in nested_dict.items():
                processing_path.append(group_name)
                return self._filter_nested_groups(sub_nested, processing_path)
        
        return processing_path