from cli import cli

class main:
    def __init__(self):
        self.init_cli()
        self.chosen_audit_type = None
        self.chosen_group = None


    def init_cli(self):
        cli_UI = cli()
        self.chosen_audit_type = cli_UI.get_audit_type()
        self.chosen_group = cli_UI.get_group()


if __name__ == "__main__":
    main()