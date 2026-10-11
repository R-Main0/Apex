import numpy as np
import pandas
import time
from openwakeword.model import Model
from variables import config, state
from services.lighting import govee_local
import services.audio as audio

Debug = 0

pthresh = 100

def check_clap(data): 
    #--- +-32768 Max/Min ---
    samples = np.frombuffer(data, dtype=np.int16).astype(np.float32)
    #Energy Quantity
    rms = np.sqrt(np.mean(samples**2))
    peak = np.max(np.abs(samples))
    if (peak > pthresh):
        spectrum, frequencies = analyze(samples)
        if (Debug): print(f"Peak: {peak}  RMS: {rms}")

def analyze(samples):
    samples -= np.mean(samples)
    window = np.hanning(len(samples))
    spectrum = np.abs(np.fft.rfft(samples * window))
    frequencies = np.fft.rfftfreq(len(samples), 1 / config.sr)


    return spectrum, frequencies


