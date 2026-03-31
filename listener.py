import threading
import sounddevice as sd
import queue
import json
import vosk

import actions  # Command file

# Command mapping
KEYWORDS = {
    "action": actions.show_message
}

# --- Setup Vosk model ---
model = vosk.Model("vosk-model-small-en-us-0.15")  # path to your model
q = queue.Queue()

# --- Audio callback for streaming ---
def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))

# --- Main listening thread ---
def recognize_loop():
    global running
    rec = vosk.KaldiRecognizer(model, 16000)
    while running:
        data = q.get()
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            text = result.get("text", "")
            if text:
                print(f"Recognized: {text}")
                for keyword, func in KEYWORDS.items():
                    if keyword in text.lower():
                        func()

# --- Start the stream ---
running = True
stream = sd.InputStream(samplerate=16000, channels=1, callback=audio_callback)
with stream:
    threading.Thread(target=recognize_loop, daemon=True).start()
    print("Listening... Press Ctrl+C to stop.")
    try:
        while running:
            sd.sleep(1000)
    except KeyboardInterrupt:
        running = False
        print("Stopped by user")