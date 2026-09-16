import queue

def rgb(r, g, b) :
    return [r, g, b]

fall = rgb(255, 90, 0)
blue = rgb(10, 20, 230)
purple = rgb(25, 8, 200)

RGBpresets = [[255, 90, 0, "Fall"], [10, 20, 230, "Blue"], [25, 8, 200, "Purple"]]

vosk_path = r"C:\Users\cathy\Apex\vosk-model-small-en-us-0.15"
wake_path = "resources/Apex.onnx"

sr = 16000
q = queue.Queue(maxsize=50)
wake_period = 3
wake_threshold = .2

