import threading
import sounddevice as sd
import queue
import json
import vosk
import time
import os
import actions  # Command file

# Command mapping
KEYWORDS = {
    "action": actions.show_message,
    "wake": actions.wake,
    "sleep": actions.sleep,
    "deactivate": actions.deactivate
}

# --- Setup Vosk model, sample rate, device, and running boolean ---
model = vosk.Model(r"C:\Users\cathy\Apex\vosk-model-small-en-us-0.15")  # path to model
sr = int(sd.query_devices(5)['default_samplerate'])
q = queue.Queue()
device = next(i for i, d in enumerate(sd.query_devices()) if "Microphone" in d["name"])
running = True

# --- Audio callback for streaming ---
def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))

# --- Main listening thread ---
def recognize_loop():
    rec = vosk.KaldiRecognizer(model, sr)
    awake = False
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
                    wake_time = time.time()

                # --- Process Commands if awake ---
                if awake:
                    # Timeout check
                    if time.time() - wake_time > 5:
                        print("Apex asleep")
                        awake = False

                    for keyword, func in KEYWORDS.items():
                        if keyword in text.lower():
                            func()
                            awake = False  # go back to sleep after command
                            break

def runStream():
    # --- Start the stream ---
    running = True
    stream = sd.RawInputStream(samplerate=sr, blocksize = 8000, channels=1, callback=audio_callback, device=device, dtype="int16")
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

