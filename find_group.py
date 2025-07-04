class find:
    def __init__(self, unfiltered_dict, wanted_group):
        self.unfiltered_dict = unfiltered_dict
        self.wanted_group = wanted_group
        self.filtered_dict = {}
        self.find_group()
        print(self.filtered_dict)


    #SUPER JANK PLEASE FOR LOVE OF GOD FIX
    def find_group(self):
        for share, groups in self.unfiltered_dict.items():
            if groups:
                paths = self.search_nested_groups(groups, [])
                if paths:
                    self.filtered_dict[share] = paths
        return self.filtered_dict

    def search_nested_groups(self, groups_dict, current_path):
        found_path = []
        for group, sub_groups in groups_dict.items():
            new_path = current_path + [group]
            if group == self.wanted_group:
                found_path.append("->".join(new_path))
            if sub_groups:
                nested_paths = self.search_nested_groups(sub_groups, new_path)
                found_path.extend(nested_paths)
        return found_path