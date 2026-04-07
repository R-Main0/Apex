import subprocess
import socket
import json

GOVEE_IPS = {
    "192.168.1.97",
    "192.168.1.174",
    "192.168.1.175",
    "192.168.1.102",
    "192.168.1.142"
}




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
    
def switch(ip, val):
    goveeSingle(ip, "turn", val)

def switchAll(val):
    goveeAll("turn", val)

def color(ip, r, g, b):
    msg = {
        "msg": {
            "cmd": "colorwc",
            "data": {"color": {"r": r, "g": g, "b": b}}
        },
        "colorTemInKelvin":9000
    }
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(json.dumps(msg).encode(), (ip, 4003))
    sock.close()

def colorAll(r, g, b):
    msg = {
        "msg": {
            "cmd": "colorwc",
            "data": {"color": {"r": r, "g": g, "b": b}}
        },
        "colorTemInKelvin":9000
    }
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for ip in GOVEE_IPS:
        sock.sendto(json.dumps(msg).encode(), (ip, 4003))
    sock.close()

def brightness(ip, val):
    goveeSingle(ip, "brightness", val)

def brightnessAll(val):
    goveeAll("brightness", val)

def goveeSingle(ip, cmd, val):
    msg = {
        "msg": {
            "cmd": cmd,
            "data": {"value": val}
        }
    }
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(json.dumps(msg).encode(), (ip, 4003))
    sock.close()

def goveeAll(cmd, val):
    msg = {
        "msg": {
            "cmd": cmd,
            "data": {"value": val}
        }
    }
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for ip in GOVEE_IPS:
        sock.sendto(json.dumps(msg).encode(), (ip, 4003))
    sock.close()