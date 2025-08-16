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
        Fixed version with flat structure
        """
        print(f"working on share: {share_to_audit}")
        commands = command.get_commands_yaml()
        share_groups_cmd = commands["share_cmds"]["associated_groups"]
        share_groups_output = command.powershell_execute(share_groups_cmd.format(option=share_to_audit))
        
        if not share_groups_output:
            return share_to_audit, []
        
        share_groups = [group.strip() for group in share_groups_output.splitlines() if group.strip()]
        share_data = []

        for share_group in share_groups:
            # Get complete group chain in one pass - NO RECURSION
            group_chain = self._get_group_chain(share_group, share_to_audit)
            
            permission_entry = {
                "group_chain": group_chain,
            }
            share_data.append(permission_entry)
        
        return share_to_audit, share_data

    def _get_group_chain(self, start_group, share, max_depth=15):
        """
        Breadth-first traversal with depth tracking per group - AI assisted bc data storage hard :(
        """
        inherited_access = self._extract_share_permissions(start_group, share)
        chain = [{"group_name": start_group, 
                "account_type": group_scanner.get_account_type(start_group),
                "access_rights": inherited_access,
                "depth": 0
                }]
        visited = {start_group} 
        current_groups = [start_group]
        depth = 0
        
        while current_groups and depth < max_depth:
            next_level_groups = []
            
            for group in current_groups:
                nested_groups = group_scanner.process_single_group(group)
                if nested_groups:
                    for nested_group in nested_groups:
                        if nested_group not in visited:
                            visited.add(nested_group)
                            chain.append({"group_name": nested_group, 
                                        "account_type": group_scanner.get_account_type(nested_group),
                                        "access_rights" : inherited_access,
                                        "depth": depth + 1
                                        })
                            next_level_groups.append(nested_group)
        
            current_groups = next_level_groups
            depth += 1
        
        return chain

    def _extract_share_permissions(self, account, share):
        """
        This takes a group and checks what it's permissions are for a particular group
        """
        commands = command.get_commands_yaml()
        access_cmd = commands["share_cmds"]["access_rights"]
        access = command.powershell_execute(access_cmd.format(share=share, account=account))

        return access
