import vosk
import json
from variables import config

model = vosk.Model(config.vosk_path)

class SpeechRecognizer:
    def __init__(self):
        self.rec = vosk.KaldiRecognizer(model, config.sr)

    def process(self, data):
        self.rec.AcceptWaveform(data)
        partial = json.loads(self.rec.PartialResult())
        return partial.get("partial", "")

    def reset(self):
        self.rec.Reset()