import subprocess
import os

def setup():
    if os.getuid() == 0:
        print("WARNING!!! Running as root. This can be very dangerous!")
        print("Unloading cmd module!")
        return False
    print("cmd setup")
    
def run(cmd=None, **kwargs):
    output = subprocess.check_output(cmd, shell=True)
    return output.decode('utf-8')
public = {
    "run": run
}
