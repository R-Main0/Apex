import threading
import queue
import sounddevice as sd
import soundfile as sf
import os

# --- Setup ---
audio_queue = queue.Queue()

SOUNDS_DIR = r"C:\Users\cathy\Apex\resources\audio"

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
    

def play_sound(path):
    data, samplerate = sf.read(path)
    sd.play(data, samplerate)
    sd.wait()


#def clap_check():