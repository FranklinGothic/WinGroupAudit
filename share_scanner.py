from command_executor import command
from group_scanner import group_scanner

class share_scanner:
    def __init__(self, shares_to_audit):
        self.shares_to_audit = shares_to_audit
        self.shares_dictionary = {}

    def get_share_groups(self):
        """
        This gets the groups directly connected with the share - this is because the command to get these groups is different from getting nested groups
        """
        commands = command.get_commands_yaml()
        share_groups_cmd = commands["share_cmds"]["associated_groups"]

        for share_to_audit in self.shares_to_audit:
            share_groups_output = command.powershell_execute(share_groups_cmd.format(option=share_to_audit))
            share_groups = share_groups_output.splitlines()

            for share_group in share_groups:
                self.shares_dictionary[share_to_audit] = group_scanner.get_nested_groups(share_group)
        
        command.dump_to_json(self.shares_dictionary)