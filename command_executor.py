import os, subprocess
import yaml, json

class command:

    @staticmethod
    def powershell_execute(ps_cmd):
        """
        Executes powershell commands
        """
        result = subprocess.run(
            f"powershell.exe -Command \"& {{ {ps_cmd} }}\"",
            capture_output=True,
            text=True,
            timeout=30
        )
        
        return command.validate_execution(result.stdout, result.returncode, result.stderr)
    
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
    def dump_to_json(data, type):
        """
        Opens the json file and dumps all data into the file
        """
        with open(f"audit_results_{type}.json", "w") as file:
            json.dump(data, file, indent=2)
        print(f"Dumped to {type} json!")

    @staticmethod
    def read_json(type):
        """
        This opens the json file and returns the data only upon user request
        """
        with open(f"audit_results_{type}.json", "r") as file:
            data = json.load(file)
        return data