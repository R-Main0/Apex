import subprocess
import socket
import json

#--- Device Variables ---
GOVEE_IP = "192.168.1.97"

def connected():
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
    
def switch(val):
    msg = {
        "msg": {
            "cmd": "turn",
            "data": {"value": val}
        }
    }
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(json.dumps(msg).encode(), (GOVEE_IP, 4003))
    sock.close()