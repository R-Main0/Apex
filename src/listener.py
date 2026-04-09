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
import auxilery # Support file

# Command mapping
KEYWORDS = {
    "home": actions.home,
    "return": actions.home,
    "resume": actions.resume,
    "fade": actions.fade,
    "box": actions.xbox,
    "night": actions.night,
    "shut": auxilery.end,
    "wake": actions.wake,
    "sleep": actions.sleep,
    "clear": actions.clear,
    "deactivate": actions.deactivate,
    "own": actions.home,
    "phone": actions.home,
    "action": actions.show_message
}

# --- Setup Vosk model, wakeword model, sample rate, device, and running boolean ---
model = vosk.Model(r"C:\Users\cathy\Apex\vosk-model-small-en-us-0.15")  # path to model
wModel = Model(wakeword_models=["resources/Apex.onnx"])
sr = 16000
q = queue.Queue()
wakePeriod = 3
wake_time = 0
device = next(i for i, d in enumerate(sd.query_devices()) if "Microphone" in d["name"])
running = True
awake = False
night = False

# --- Audio callback for streaming ---
def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))

# --- Main listening thread ---
def recognize_loop():
    rec = vosk.KaldiRecognizer(model, sr)
    global awake, wake_time, night

    while running:
        data = q.get()
        audioNp = np.frombuffer(data, dtype=np.int16)

        # --- Wake word detection ---
        prediction = wModel.predict(audioNp)
        score = list(prediction.values())[0]

        if score > 0.05 and time.time() - wake_time > wakePeriod + 4:
            print(f"Wake word detected! Score: {score}")
            awake = True
            night = False
            wake_time = time.time()
            auxilery.brightness("192.168.1.97", 90)
            rec.Reset()  #Clears old audio

        # --- FAST partial recognition ---
        if awake:
            partial = json.loads(rec.PartialResult())
            text = partial.get("partial", "")

            if text:
                print(f"Partial: {text}")
                for keyword, func in KEYWORDS.items():
                    if keyword in text.lower():
                        func()
                        if not night:
                            auxilery.brightness("192.168.1.97", 50)
                        rec.Reset()  #prevents repeated triggers

        # --- Feed audio to Vosk ---
        rec.AcceptWaveform(data)

        # --- Timeout ---
        if awake and (time.time() - wake_time > wakePeriod):
            print("Apex asleep")
            awake = False
            if not night:
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

