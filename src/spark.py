import subprocess
import pystray
import os
from PIL import Image
import win32event
import win32api

mutex = win32event.CreateMutex(None, False, "ApexSparkMutex")

if win32api.GetLastError() == 183:
    print("Already running")
    os._exit(0)

# ----------------------------
# Main tray setup
# ----------------------------
def kill(icon):
    icon.stop()
    subprocess.Popen(["pythonw", r"C:\Users\cathy\Apex\src\main.py"],
    creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP)
    os._exit(0)  # exits immediately

img = Image.open("resources/Apex.ico") #ico image
icon = pystray.Icon(
    "Apex", 
    img,
    menu=pystray.Menu(
        pystray.MenuItem("Stop", kill, default=True)  # Hidden Menu, only kills program when clicked
    )
)

# --- Program Entry Point ---
icon.run_detached()