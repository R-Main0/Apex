import subprocess
import os
from services import audio

def end():
    print("Exiting...")
    subprocess.Popen([
        r"C:\Users\cathy\AppData\Local\Python\pythoncore-3.14-64\pythonw.exe",
        r"C:\Users\cathy\Apex\src\spark.py"],
        creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP)
    os._exit(0)

def connectWifi():
    try:
        result = subprocess.check_output(
            ["netsh", "wlan", "show", "interfaces"], encoding="utf-8"
        )
        for line in result.split("\n"):
            if "SSID" in line and "BSSID" not in line:
                ssid = line.split(":", 1)[1].strip()
                return ssid == "4 Big Boys With Everything"
        # If no SSID line found, not connected
        return False
    
    except subprocess.CalledProcessError:
        # Command failed, assume not connected
        return False
    
def connectBlueTooth():
    subprocess.run([r"C:\Tools\nircmd\nircmd.exe", "setdefaultsounddevice", "SW-208"])

