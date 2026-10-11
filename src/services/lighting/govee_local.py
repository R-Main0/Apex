import socket
import json
import queue
import threading

GOVEE_IPS = {
    "192.168.1.97",
    "192.168.1.174",
    "192.168.1.175",
    "192.168.1.102",
    "192.168.1.142"
}

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
govee_localq = queue.Queue()

def start_govee_local_engine():
    threading.Thread(target=queue_worker, daemon=True).start()

def queue_worker():
    while True:
        func, args = govee_localq.get()
        func(*args)
        govee_localq.task_done()


def switch(ip, val):
    govee_localq.put((goveeSingle, (ip, "turn", "value", val)))

def switchAll(val):
    govee_localq.put((goveeAll, ("turn", "value", val)))

def color(ip, r, g, b):
    val = {"r": r, "g": g, "b": b}
    govee_localq.put((goveeSingle, (ip, "colorwc", "color", val)))

def colorAll(r, g, b):
    val = {"r": r, "g": g, "b": b}
    govee_localq.put((goveeAll, ("colorwc", "color", val)))

def brightness(ip, val):
    govee_localq.put((goveeSingle, (ip, "brightness", "value", val)))

def brightnessAll(val):
    govee_localq.put((goveeAll, ("brightness", "value", val)))

def goveeSingle(ip, cmd, val_type, val):
    msg = {
        "msg": {
            "cmd": cmd,
            "data": {val_type: val}
        }
    }
    sock.sendto(json.dumps(msg).encode(), (ip, 4003))

def goveeAll(cmd, val_type, val):
    msg = {
        "msg": {
            "cmd": cmd,
            "data": {val_type: val}
        }
    }
    for ip in GOVEE_IPS:
        sock.sendto(json.dumps(msg).encode(), (ip, 4003))