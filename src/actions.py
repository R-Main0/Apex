import subprocess
import auxilery
import listener
import keyboard

#--- Device Variables ---
STRIP_IP = "192.168.1.97"
LAMP_IP = "192.168.1.174"
CLOSET_IP = "192.168.1.175"
BATHROOM_IP1 = "192.168.1.102"
BATHROOM_IP2 = "192.168.1.142"

def show_message():
    print("Hello from action system!")

def home():
    print("Initializing default...")
    auxilery.switchAll(1)
    auxilery.brightnessAll(100)
    auxilery.color(LAMP_IP, 20, 10, 255)
    auxilery.color(CLOSET_IP, 220, 110, 50)
    auxilery.color(BATHROOM_IP1, 220, 110, 50)
    auxilery.color(BATHROOM_IP2, 220, 110, 50)
    auxilery.color(STRIP_IP, 20, 10, 255)
    clear()
    
def wake():
    print("Waking up systems...")
    auxilery.switchAll(1)

def sleep():
    print("Sleeping...")
    listener.awake = False
    auxilery.switchAll(0)

def clear():
    print("Clearing Screen...")
    keyboard.send("windows+d")
    subprocess.Popen([r"C:\Program Files (x86)\Steam\steamapps\common\wallpaper_engine\wallpaper32.exe", "-control", "play"])

def aubrey():
    print("Welcome to the barbie dream house...")
    auxilery.colorAll(255, 100, 170)

def resume():
    print("Resuming Workstation")
    keyboard.send("windows+d")
    subprocess.Popen([r"C:\Program Files (x86)\Steam\steamapps\common\wallpaper_engine\wallpaper32.exe", "-control", "pause"])

    
def deactivate():
    print("Shutting Down Systems...")
    auxilery.switchAll(0)
    subprocess.run(["powercfg", "/hibernate", "off"])
    subprocess.run(["rundll32.exe", "powrprof.dll,SetSuspendState", "0,0,0"])
