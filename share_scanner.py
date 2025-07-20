from command_executor import command
from group_scanner import group_scanner
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

class share_scanner:
    def __init__(self, shares_to_audit):
        self.shares_to_audit = shares_to_audit
        self.shares_dictionary = {}
        self.lock = threading.Lock()

    def _process_single_share(self, share_to_audit):
        """
        This will process a single share and will be used in parallel
        """
        print(f"working on share: {share_to_audit}")
        commands = command.get_commands_yaml()
        share_groups_cmd = commands["share_cmds"]["associated_groups"]
        share_groups_output = command.powershell_execute(share_groups_cmd.format(option=share_to_audit))
        share_groups = share_groups_output.splitlines()

        share_data = {}


        share_data = group_scanner.get_nested_groups(share_groups)
        return share_to_audit, share_data
    
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
                    self.shares_dictionary[share_name] = share_data
        
        return self.shares_dictionary