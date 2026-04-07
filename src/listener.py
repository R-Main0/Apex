import threading
import sounddevice as sd
import numpy as np
from openwakeword.model import Model
import queue
import json
import vosk
import time
import os
import actions  # Command file
import auxilery # Support File

# Command mapping
KEYWORDS = {
    "action": actions.show_message,
    "wake": actions.wake,
    "sleep": actions.sleep,
    "clear": actions.clear,
    "deactivate": actions.deactivate,
    "home": actions.home,
    "resume": actions.resume,
    "aubrey": actions.aubrey
}

# --- Setup Vosk model, wakeword model, sample rate, device, and running boolean ---
model = vosk.Model(r"C:\Users\cathy\Apex\vosk-model-small-en-us-0.15")  # path to model
#wModel = Model(wakeword_models=["resources/Apex.onnx"])
sr = int(sd.query_devices(5)['default_samplerate'])
q = queue.Queue()
device = next(i for i, d in enumerate(sd.query_devices()) if "Microphone" in d["name"])
running = True
awake = False

# --- Audio callback for streaming ---
def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))

# --- Main listening thread ---
def recognize_loop():
    rec = vosk.KaldiRecognizer(model, sr)
    global awake
    while running:
        data = q.get()
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            text = result.get("text", "")
            if text:
                print(f"Recognized: {text}")

                # --- Check Wake Word "Apex" ---
                if "apex" in text:
                    print("Apex awake")
                    awake = True
                    auxilery.brightness("192.168.1.97", 90)
                    wake_time = time.time()

                if awake:
                    for keyword, func in KEYWORDS.items():
                        if keyword in text.lower():
                            func()
                            break

        # --- Process Commands if awake ---
        if awake:
            # Timeout check
            if time.time() - wake_time > 6:
                print("Apex asleep")
                awake = False
                auxilery.brightness("192.168.1.97", 50)

def runStream():
    # --- Start the stream ---
    running = True
    stream = sd.RawInputStream(samplerate=sr, blocksize = 512, channels=1, callback=audio_callback, device=device, dtype="int16")
    with stream:
        threading.Thread(target=recognize_loop, daemon=True).start()
        print("Listening... Press Ctrl+C to stop.")
        try:
            while running:
                sd.sleep(1000)
        except KeyboardInterrupt:
            running = False
            print("Stopped by user")
            os._exit(0)

