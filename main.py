from cli import genrl_cli, share_cli
from filter_groups import filter_groups
from share_scanner import share_scanner
from command_executor import command
import atexit

class main:
    def __init__(self):
        atexit.register(command.end_session)

        self.chosen_audit_type = None
        self.chosen_groups = None
        self.run_cli()
        self.run_audit()

    def run_cli(self):
        """
        Initializes the cli and runs the required methods to dictate the rest of program
        """
        cli_UI = genrl_cli()
        self.chosen_audit_type = cli_UI.get_audit_type()
        self.chosen_groups = cli_UI.get_groups()

    def run_audit(self):
        """
        Runs the program and matches the chosen audit type to the correct audit flow
        """
        match self.chosen_audit_type:

            case "Shares": 
                share_cli_UI = share_cli()
                shares_to_audit = share_cli_UI.get_share_selection()

                scan_shares = share_scanner(shares_to_audit)
                results = scan_shares.get_share_groups()

        
        command.dump_to_json(results, "full")

        input("\nFilter data?")
        filter = filter_groups(self.chosen_groups)
        filtered_data = filter.filter_groups()
        command.dump_to_json(filtered_data, "filtered")




if __name__ == "__main__":
    main()