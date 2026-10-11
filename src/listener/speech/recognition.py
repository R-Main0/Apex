import vosk
import json
from variables import config
import listener.actions as actions

# Command mapping
KEYWORDS = {
    "return": actions.home,
    "fade": actions.fade,
    "box": actions.xbox_on,
    "night": actions.night,
    "fire": actions.fire,
    "deep": actions.deep,
    "blow": actions.explosion,
    "rise": actions.rise,
    "rocket": actions.party,
    "wake": actions.wake,
    "sleep": actions.sleep,
    "clear": actions.clear,
    "deactivate": actions.deactivate,
    "action": actions.show_message,
    "real": actions.real,
    "gravity": actions.interstellar,
    "cycle": actions.rotate
}

model = vosk.Model(config.vosk_path_lgraph)
#grammar = json.dumps(list(KEYWORDS.keys()))

class SpeechRecognizer:
    def __init__(self):
        self.rec = vosk.KaldiRecognizer(model, config.sr)

    def process(self, data):
        self.rec.AcceptWaveform(data)
        partial = json.loads(self.rec.PartialResult())
        return partial.get("partial", "")

    def reset(self):
        self.rec.Reset()