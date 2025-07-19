from cli import genrl_cli, share_cli
from share_scanner import shares

class main:
    def __init__(self):
        self.chosen_audit_type = None
        self.chosen_group = None
        self.run_cli()
        self.run_audit()

    def run_cli(self):
        """
        Initializes the cli and runs the required methods to dictate the rest of program
        """
        cli_UI = genrl_cli()
        self.chosen_audit_type = cli_UI.get_audit_type()
        self.chosen_group = cli_UI.get_group()

    def run_audit(self):
        """
        Runs the program and matches the chosen audit type to the correct audit flow
        """
        match self.chosen_audit_type:

            case "Shares": 
                share_cli_UI = share_cli()
                shares_to_audit = share_cli_UI.get_share_selection()


if __name__ == "__main__":
    main()