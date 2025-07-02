import os, subprocess

class shares:
    def __init__(self):
        command = r"Get-SmbShare | Where-Object {$_.Name -notmatch '\$$'} | Select-Object -ExpandProperty Name"
        shares = subprocess.Popen(f"powershell.exe -Command \"& {{ {command} }}\"", 
                        stdout=subprocess.PIPE, text=True)
        
        output, _ = shares.communicate()    # Wait for the process to finish and get the output
        print(output.strip())

shares()