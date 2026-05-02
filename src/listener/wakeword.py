import numpy as np
import time
from openwakeword.model import Model
from variables import config, state
from services import govee_local
import services.audio as audio

model = Model(wakeword_models=[config.wake_path], inference_framework="onnx")

def check_wakeword(data):
    audio_np = np.frombuffer(data, dtype=np.int16)
    prediction = model.predict(audio_np)
    score = list(prediction.values())[0]

    if score > config.wake_threshold and time.time() - state.wake_time > config.wake_period + 4:
        print(f"Wake word detected! Score: {score}")
        state.awake = True
        state.night = False
        state.wake_time = time.time()
        audio.enqueue_sound("universfield-interface-soft-click-131438.wav")
        govee_local.brightness("192.168.1.97", 90)
        return True

    return False