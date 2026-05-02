import services.controller as controller
import pystray
import listener.actions as actions
import listener.stream as stream
import services.audio as audio
import services.govee_local as govee_local
import variables.config as config
import os
import time
from PIL import Image
import win32event, win32api

# --- Check for other instances of program ---
mutex = win32event.CreateMutex(None, False, "ApexMutex")
if win32api.GetLastError() == 183:
    print("Already running")
    os._exit(0)

# --- Check if on home wifi and bluetooth---
if not controller.connectWifi():
    print("**Not connected to home wifi.**")
    controller.end()
#controller.connectBlueTooth()


# ----------------------------
# Main tray setup
# ----------------------------
def kill(icon):
    icon.stop()
    controller.end()


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
govee_local.start_govee_local_engine()
audio.start_audio_engine()
actions.boot()
time.sleep(2)
stream.runStream()


