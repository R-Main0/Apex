import sounddevice as sd
import queue
import json
from vosk import Model, KaldiRecognizer

import commands  # <-- your separate file

# Path to your Vosk model
MODEL_PATH = "C:/vosk-model-small-en-us-0.15"

q = queue.Queue()

# Audio callback (runs constantly)
def audio_callback(indata, frames, time, status):
    q.put(bytes(indata))

# Load model
model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, 16000)

# Command mapping
COMMANDS = {
    "start listening": commands.start_listener,
    "open browser": commands.open_browser,
    "hello": commands.show_message,
}

def handle_text(text):
    print("Heard:", text)

    for phrase, func in COMMANDS.items():
        if phrase in text:
            print(f"Triggering: {phrase}")
            func()
            return

# Start audio stream
with sd.RawInputStream(
    samplerate=16000,
    blocksize=8000,
    dtype='int16',
    channels=1,
    callback=audio_callback
):
    print("Listening for commands...")

    while True:
        data = q.get()

        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            text = result.get("text", "")

            if text:
                handle_text(text)