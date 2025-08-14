from command_executor import command
from group_scanner import group_scanner
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

class share_scanner:
    def __init__(self, shares_to_audit):
        self.shares_to_audit = shares_to_audit

        self.shares_dictionary = command.set_up_json_dict("Shares")

        self.lock = threading.Lock()

    def get_share_groups(self, max_workers=3): #create more threads for thoretical greater speed but may cause degregration if too many
        """
        This will split the share processing into multiple threads so execution can complete exponetially faster
        """
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_share = [
                executor.submit(self._process_single_share, share) for share in self.shares_to_audit
            ]
            
            for future in as_completed(future_to_share):
                share_name, share_data = future.result()
                with self.lock:
                    share_object = {
                        "share_name" : share_name,
                        "permissions" : share_data
                        }
                    self.shares_dictionary["Shares"].append(share_object)

        
        return self.shares_dictionary

    def _process_single_share(self, share_to_audit):
        """
        This will process a single share and will be used in parallel
        """
        print(f"working on share: {share_to_audit}")
        commands = command.get_commands_yaml()
        share_groups_cmd = commands["share_cmds"]["associated_groups"]
        share_groups_output = command.powershell_execute(share_groups_cmd.format(option=share_to_audit))
        share_groups = share_groups_output.splitlines()

        share_data = []

        for share_group in share_groups:
            share_group_object = {
                "account_name" : share_group,
                "account_type" : "",
                "access_rights" : "",
                "nested_accounts" : self._process_share_group(share_group)
            }
            share_data.append(share_group_object)
        return share_to_audit, share_data
    
    def _process_share_group(self, group, visited=None):
        """
        This will process the whole line of groups branching from the groups directly under the share
        """
        if visited is None:
            visited = set()
        
        # Prevent infinite recursion
        if group in visited:
            return []
        
        visited.add(group)

        group_data = []
        nested_groups = group_scanner.process_single_group(group)

        if nested_groups:
            for nested_group in nested_groups:
                group_object = {
                "account_name" : nested_group,
                "account_type" : "",
                "access_rights" : "",
                "nested_accounts" : self._process_share_group(nested_group, visited.copy())
                }
                group_data.append(group_object)
        
        return group_data

    def _extract_share_permissions(self, group):
        """
        This takes a group and checks what it's permissions are for a particular group
        """