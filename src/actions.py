import subprocess
import auxilery

def show_message():
    print("Hello from action system!");

def wake():
    print("Waking up systems...")
    auxilery.switch(1)

def sleep():
    print("Sleeping...")
    auxilery.switch(0)
    
def deactivate():
    print("Shutting Down Systems...")
    auxilery.switch(0)
    subprocess.run(["powercfg", "/hibernate", "off"])
    subprocess.run(["rundll32.exe", "powrprof.dll,SetSuspendState", "0,0,0"])
