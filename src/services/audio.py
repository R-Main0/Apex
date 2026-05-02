import threading
import queue
import sounddevice as sd
import soundfile as sf
import os
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# --- Setup ---
audio_queue = queue.Queue()

SOUNDS_DIR = r"C:\Users\cathy\Apex\resources\audio"


# --- Queue API ---
#def enqueue_speak(text, priority=False):
#    audio_queue.put(("speak", text, priority))

def enqueue_sound(filename, priority=False):
    audio_queue.put(("sound", filename, priority))

# --- Worker Thread ---
def audio_worker():
    while True:
        task_type, data, priority = audio_queue.get()

        if priority:
            clear_queue()

        if task_type == "sound":
            path = os.path.join(SOUNDS_DIR, data)
            play_sound(path)

        audio_queue.task_done()

# --- Utility ---
def clear_queue():
    while not audio_queue.empty():
        try:
            audio_queue.get_nowait()
            audio_queue.task_done()
        except queue.Empty:
            break

# --- Start thread ---
def start_audio_engine():
    thread = threading.Thread(target=audio_worker, daemon=True)
    thread.start()

    #Initialize volume control
    #global volume
    #devices = AudioUtilities.GetSpeakers()
    #interface = devices.Activate(
    #    IAudioEndpointVolume._iid_, CLSCTX_ALL, None
    #)
    #volume = cast(interface, POINTER(IAudioEndpointVolume))
    

def play_sound(path):
    data, samplerate = sf.read(path)
    sd.play(data, samplerate)
    sd.wait()

'''
def setVolume(percent):
    min_db = -65.0
    max_db = 0.0
    
    percent = max(0, min(100, percent))  
    db = min_db + (percent / 100.0) * (max_db - min_db) # Map decibles from 0 to 100
    volume.SetMasterVolumeLevel(db, None)

def mute(val):
    volume.SetMute(val, None)

def getVolume():
    return volume.GetMasterVolumeLevel()
'''