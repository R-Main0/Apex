import vosk
import json
from variables import config
import listener.actions as actions

# Command mapping
KEYWORDS = {
    "home": actions.home,
    "return": actions.home,
    "fade": actions.fade,
    "box": actions.xbox_on,
    "night": actions.night,
    "fire": actions.fire,
    "deep": actions.deep,
    "blow": actions.explosion,
    "rise": actions.rise,
    "party": actions.party,
    "wake": actions.wake,
    "sleep": actions.sleep,
    "clear": actions.clear,
    "deactivate": actions.deactivate,
    "own": actions.home,
    "phone": actions.home,
    "action": actions.show_message,
    "real": actions.real,
    "gravity": actions.interstellar,
    "rotate": actions.rotate
}

model = vosk.Model(config.vosk_path)
grammar = json.dumps(list(KEYWORDS.keys()))

class SpeechRecognizer:
    def __init__(self):
        self.rec = vosk.KaldiRecognizer(model, config.sr, grammar)

    def process(self, data):
        self.rec.AcceptWaveform(data)
        partial = json.loads(self.rec.PartialResult())
        return partial.get("partial", "")

    def reset(self):
        self.rec.Reset()