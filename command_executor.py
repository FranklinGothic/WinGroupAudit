import os, subprocess
import yaml, json

class command:

    @staticmethod
    def powershell_execute(ps_cmd):
        """
        Executes powershell commands
        """
        response = subprocess.Popen(f"powershell.exe -Command \"& {ps_cmd}\"", 
                        stdout=subprocess.PIPE, text=True)
        output, error = response.communicate()

        return command.validate_execution(output, response.returncode, error)
    
    @staticmethod
    def terminal_execute(tm_cmd):
        """
        Executes commands through the command line
        """
        response = subprocess.Popen(tm_cmd, shell=True, 
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output, error = response.communicate()

        return command.validate_execution(output, response.returncode, error)
    
    @staticmethod
    def validate_execution(output, code, error):
        """
        Confirms that no errors occured during execution of any commands
        """
        if code != 0:
            print(f"command failed with return code {code}: {error}")
            return None

        print(f"Command succeeded with return code {code}")
        return output.strip()
    
    @staticmethod
    def clear_screen():
        """
        Clears terminal screen for cleanliness
        """
        os.system("cls")

    @staticmethod
    def get_commands_yaml():
        """
        Opens the yaml command file and returns all of the commands
        """
        with open("system_cmds.yaml", "r") as file:
            commands = yaml.safe_load(file)

        return commands
    
    @staticmethod
    def dump_to_json(audit_data):
        """
        Opens the json file and dumps all data into the file
        """
        with open("audit_results.json", "w") as file:
            json.dump(audit_data, file, indent=2)
        print("Dumped to json!")