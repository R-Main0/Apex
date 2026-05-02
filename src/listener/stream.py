import threading
import sounddevice as sd
import queue
import variables.config as config
import listener.core as core
import os

device = next(i for i, d in enumerate(sd.query_devices()) if "Microphone" in d["name"])

def runStream():
    # --- Start the stream ---
    running = True
    stream = sd.RawInputStream(samplerate=config.sr, blocksize = 512, channels=1, callback=audio_callback, device=device, dtype="int16")
    with stream:
        threading.Thread(target=core.recognize_loop, daemon=True).start()
        print("Listening... Press Ctrl+C to stop.")
        try:
            while running:
                sd.sleep(1000)
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