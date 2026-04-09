import subprocess
import auxilery
import listener
import keyboard
import time

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
    time.sleep(.2)
    auxilery.brightnessAll(100)
    time.sleep(.2)
    auxilery.color(LAMP_IP, 0, 0, 255)
    auxilery.color(CLOSET_IP, 220, 140, 50)
    auxilery.color(BATHROOM_IP1, 220, 140, 50)
    auxilery.color(BATHROOM_IP2, 220, 110, 50)
    auxilery.color(STRIP_IP, 20, 10, 255)
    subprocess.Popen([r"C:\Program Files (x86)\Steam\steamapps\common\wallpaper_engine\wallpaper32.exe", "-control", "openWallpaper", "-file",  r"C:\Program Files (x86)\Steam\steamapps\workshop\content\431960\3041448036\project.json" ])
    clear()
    
def wake():
    print("Waking up systems...")
    auxilery.switchAll(1)

def sleep():
    print("Sleeping...")
    auxilery.switchAll(0)
    listener.night = True
    keyboard.press_and_release('windows+x')
    time.sleep(0.2)
    keyboard.press_and_release('u')
    time.sleep(0.2)
    keyboard.press_and_release('s')    

def night():
    print("Activating night mode...")
    auxilery.brightnessAll(10)
    auxilery.colorAll(220, 140, 50)
    listener.night = True

def clear():
    print("Clearing Screen...")
    keyboard.send("windows+d")
    subprocess.Popen([r"C:\Program Files (x86)\Steam\steamapps\common\wallpaper_engine\wallpaper32.exe", "-control", "play"])

def fade():
    print("Welcome Aubrey...")
    auxilery.colorAll(255, 100, 170)
    auxilery.brightnessAll(30)
    subprocess.Popen([r"C:\Program Files (x86)\Steam\steamapps\common\wallpaper_engine\wallpaper32.exe", "-control", "openWallpaper", "-file",  r"C:\Program Files (x86)\Steam\steamapps\workshop\content\431960\2784382079\project.json" ])


def resume():
    print("Resuming Workstation")
    keyboard.send("windows+d")
    subprocess.Popen([r"C:\Program Files (x86)\Steam\steamapps\common\wallpaper_engine\wallpaper32.exe", "-control", "pause"])

    
def deactivate():
    print("Shutting Down Systems...")
    auxilery.switchAll(0)
    subprocess.run(["powercfg", "/hibernate", "off"])
    subprocess.run(["rundll32.exe", "powrprof.dll,SetSuspendState", "0,0,0"])

def xbox():
    print("Activating xbox...")
    auxilery.brightness(CLOSET_IP, 1)
    auxilery.brightness(BATHROOM_IP1, 1)
    auxilery.brightness(BATHROOM_IP2, 1)
    auxilery.colorAll(0, 0, 255)
    auxilery.color(LAMP_IP, 50, 0, 255)
    auxilery.color(STRIP_IP, 50, 0, 255)
    auxilery.power_on()
