from openwakeword.model import Model
import vosk
import time
import listener.actions as actions
import variables.state as state
import services.controller as controller
import services.govee_local as govee_local
import variables.config as config
import listener.recognition as recognition
import listener.wakeword as wakeword
import services.audio as audio

model = vosk.Model(config.vosk_path)  # path to model

recognizer = recognition.SpeechRecognizer()

# Main listening thread
def recognize_loop():

    while state.running:
        # Empty queue to prevent backlog 
        data = config.q.get()
        while not config.q.empty():
            data = config.q.get()

        if wakeword.check_wakeword(data):
            recognizer.reset()  # Clears old audio

        # FAST partial recognition
        if state.awake:
            # Feed audio to Vosk
            text = recognizer.process(data)

            if text:
                print(f"Partial: {text}")
                for keyword, func in recognition.KEYWORDS.items():
                    if keyword in text.lower():
                        func()
                        audio.enqueue_sound("universfield-smooth-gadget-activation-sound-250072.wav")
                        if not state.night:
                            govee_local.brightness("192.168.1.97", 50)
                        recognizer.reset()  #prevents repeated triggers

        # Timeout 
        if state.awake and (time.time() - state.wake_time > config.wake_period):
            print("Apex asleep")
            state.awake = False
            if not state.night:
                govee_local.brightness("192.168.1.97", 50)



