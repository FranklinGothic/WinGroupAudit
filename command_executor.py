import os, subprocess

class command:

    @staticmethod
    def powershell_execute(ps_cmd, option=None):
        """
        Executes powershell commands
        """
        response = subprocess.Popen(f"powershell.exe -Command \"& {ps_cmd}\"", 
                        stdout=subprocess.PIPE, text=True)
        output, error = response.communicate()

        return command.validate_execution(output, response.returncode, error)
    
    @staticmethod
    def terminal_execute(tm_cmd, option=None):
        """
        Executes commands through the command line
        """
        response = subprocess.Popen(f"{tm_cmd}", shell=True, 
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

        return output.strip()
    
    @staticmethod
    def clear_screen():
        """
        Clears terminal screen for cleanliness
        """
        os.system("cls")