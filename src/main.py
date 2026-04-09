import auxilery
import pystray
import listener
import os
from PIL import Image
import win32event, win32api

mutex = win32event.CreateMutex(None, False, "ApexMutex")

if win32api.GetLastError() == 183:
    print("Already running")
    os._exit(0)

# --- Check if on home wifi ---
if not auxilery.connected():
    print("**Not connected to home wifi.**")
    auxilery.end()

# ----------------------------
# Main tray setup
# ----------------------------
def kill(icon):
    icon.stop()
    auxilery.end()


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


