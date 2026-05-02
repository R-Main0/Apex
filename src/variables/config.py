import queue

RGBpresets = [[200, 0, 0, "Red"], [30, 180, 30, "Green"], [10, 20, 230, "Blue"]]

vosk_path = r"C:\Users\cathy\Apex\vosk-model-small-en-us-0.15"
wake_path = "resources/Apex.onnx"

sr = 16000
q = queue.Queue(maxsize=50)
wake_period = 3
wake_threshold = .2

