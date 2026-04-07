import auxilery
import pystray
import listener
import os
import subprocess
from PIL import Image

def end():
    print("Exiting...")
    subprocess.Popen(["pythonw", r"C:\Users\cathy\Apex\src\spark.py"],
    creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP)
    os._exit(0)

# --- Check if on home wifi ---
if not auxilery.connected():
    print("**Not connected to home wifi.**")
    #end()

# ----------------------------
# Main tray setup
# ----------------------------
def kill(icon):
    icon.stop()
    end()


img = Image.open("resources/ApexActive.ico")
icon = pystray.Icon(
    "Apex",
    img,
    "Deactivate Apex",
    menu=pystray.Menu(
        pystray.MenuItem("Stop", kill, default=True)  # Hidden Menu, only kills program when clicked
    )
)

# --- Program Entry Point ---
icon.run_detached()
listener.runStream()


