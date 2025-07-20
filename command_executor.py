import os, subprocess
import yaml, json

class command:

    _ps_process = None


    @staticmethod
    def init_ps():
        if command._ps_process is None:
            command._ps_process = subprocess.Popen(["powershell.exe", "-NoLogo", "-NoProfile"],      
            stdin=subprocess.PIPE, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True, 
            bufsize=1) 

            command._ps_process.stdin.write("Import-Module ActiveDirectory\n")
            command._ps_process.stdin.write("Write-Output 'AD_MODULE_READY'\n")
            command._ps_process.stdin.flush()

            while True:
                line = command._ps_process.stdout.readline().strip()
                if line == 'AD_MODULE_READY':
                    print("✅ AD Module loaded - session ready")
                    break

    @staticmethod
    def powershell_execute(ps_cmd):
        """
        Executes powershell commands in persistent session
        """
        command._init_session()
        
        command._ps_process.stdin.write(f"{ps_cmd}\n")
        command._ps_process.stdin.write("Write-Output 'COMMAND_END'\n")
        command._ps_process.stdin.flush()
        
        output_lines = []
        while True:
            line = command._ps_process.stdout.readline().strip()
            if line == 'COMMAND_END':
                break
            if line:
                output_lines.append(line)
        
        output = '\n'.join(output_lines)
        return command.validate_execution(output, 0, None)
    
    @staticmethod
    def end_session():
        """
        This is to end the powershell session
        """
        if command._ps_process is not None:
            try:
                command._ps_process.stdin.write("exit\n")
                command._ps_process.stdin.flush()
                command._ps_process.wait(timeout=5)
                
            except:
                command._ps_process.kill()
        
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