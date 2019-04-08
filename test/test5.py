#!/usr/bin/env python3
import numpy as np
import sounddevice as sd

#print(sd.query_devices())
sd.default.device = 1


duration = 6 #in seconds

def audio_callback(indata, frames, time, status):
    volume_norm = np.linalg.norm(indata) * 10
    #print("|" * int(volume_norm))
    #print(np.histogram(indata))
    print(indata.shape)
    #if indata.shape[0] < 50:
    #    print(indata)
    print(min(indata), max(indata))


stream = sd.InputStream(callback=audio_callback, channels=1)
with stream:
    sd.sleep(duration * 1000)
