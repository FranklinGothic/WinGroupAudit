import os, subprocess
import yaml, json
import threading, sys

class command:
    _thread_local = threading.local()

    @staticmethod
    def init_ps():
        """
        This initalizes a powershell session for each thread so they don't interupt each other during command execution
        """
        if not hasattr(command._thread_local, 'ps_process') or command._thread_local.ps_process.poll() is not None:
            command._thread_local.ps_process = subprocess.Popen(
                ["powershell.exe", "-NoLogo", "-NoProfile"],      
                stdin=subprocess.PIPE, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True, 
                bufsize=1
            )
            
            # Initialize AD module for this thread
            command._thread_local.ps_process.stdin.write("Import-Module ActiveDirectory\n")
            command._thread_local.ps_process.stdin.flush()

    @staticmethod
    def powershell_execute(ps_cmd):
        """
        Executes powershell commands in thread-local session
        """
        command.init_ps()
        
        ps_process = command._thread_local.ps_process
        
        ps_process.stdin.write(f"{ps_cmd}\n")
        ps_process.stdin.write("Write-Output 'COMMAND_END'\n")
        ps_process.stdin.flush()
        
        output_lines = []
        while True:
            line = ps_process.stdout.readline().strip()
            if line == 'COMMAND_END':
                break
            # Filter out unwanted lines - this is just last layer of security to prevent unwanted lines from corrupting the data
            if (line and not line.startswith('PS ') and line != ps_cmd.strip() and line != ""
                and line not in "Write-Output 'COMMAND_END'" and "|" not in line):
                output_lines.append(line)
        
        output = '\n'.join(output_lines)
        return command.validate_execution(output, 0, None)

    @staticmethod
    def end_session():
        """
        End the thread-local powershell session
        """
        if hasattr(command._thread_local, 'ps_process') and command._thread_local.ps_process is not None:
            try:
                command._thread_local.ps_process.stdin.write("exit\n")
                command._thread_local.ps_process.wait(timeout=5)
            except:
                command._thread_local.ps_process.kill()
            finally:
                command._thread_local.ps_process = None
    
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
            return None

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
        if getattr(sys, 'frozen', False):
            # Running as EXE
            bundle_dir = sys._MEIPASS
            yaml_path = os.path.join(bundle_dir, "system_cmds.yaml")
        else:
            # Running as Python script
            yaml_path = "system_cmds.yaml"
        
        with open(yaml_path, "r") as file:
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