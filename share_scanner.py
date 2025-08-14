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

        share_groups = [group.strip() for group in share_groups_output.splitlines()]
        share_data = []

        for share_group in share_groups:

            group_chain = self._get_group_chain(share_group)

            permission_entry = {
                "account_name" : share_group,
                "account_type" : "",
                "access_rights" : "",
                "group_chain": group_chain,
                "chain_length": len(group_chain)
            }
            share_data.append(permission_entry)
        return share_to_audit, share_data
    
    def _get_group_chain(self, group, visited=None):
        """
        Get flattened chain of group memberships
        """
        if visited is None:
            visited = set()

        if group in visited:
            return [group]  # Circular reference - just return the group

        visited.add(group)
        chain = [group]

        nested_groups = group_scanner.process_single_group(group)

        if nested_groups:
            # Just get the first level - don't go infinitely deep
            for nested_group in nested_groups:
                if nested_group not in visited:
                    sub_chain = self._get_group_chain(nested_group, visited.copy())
                    # Add to chain but keep it manageable
                    chain.extend(sub_chain[1:])  # Skip the first item to avoid duplication
                    break  # Only follow one path to keep it simple

        return chain

    def _extract_share_permissions(self, group):
        """
        This takes a group and checks what it's permissions are for a particular group
        """