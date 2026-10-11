import threading
import sounddevice as sd
import queue
import variables.config as config
import listener.core as core
import os

device_list = sd.query_devices()
device = next(i for i, d in enumerate(device_list) if "Microphone" in d["name"])
print(f"Microphone: {device_list[device]["name"]}")

def runStream():
    # --- Start the stream ---
    running = True
    stream = sd.RawInputStream(samplerate=config.sr, blocksize = config.blocksize, channels=1, callback=audio_callback, device=device, dtype="int16")
    with stream:
        threading.Thread(target=core.recognize_loop, daemon=True).start()
        print("Listening... Press Ctrl+C to stop.")
        try:
            while running:
                sd.sleep(10)
        except KeyboardInterrupt:
            running = False
            print("Stopped by user")
            os._exit(0)

# --- Audio callback for streaming ---
def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    try:
        config.q.put_nowait(bytes(indata))
    except queue.Full:
        pass