import socket
import time

XBOX_IP = "192.168.1.117" 
LIVE_ID = b"F4001ED92767D53D" 

def power_on():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.bind(("", 0))

    payload = b'\x00' + bytes([len(LIVE_ID)]) + LIVE_ID.upper() + b'\x00'
    header  = b'\xdd\x02\x00' + bytes([len(payload)]) + b'\x00\x00'
    packet  = header + payload

    for _ in range(5):
        s.sendto(packet, ("255.255.255.255", 3074)) 
        time.sleep(0.3)

    s.close()