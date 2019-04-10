import sounddevice as sd

print(sd.query_devices())

def callback(indata, frames, time, status):
    a = indata

with sd.InputStream(device=1, callback=callback, blocksize=44100//10):
    sd.sleep(1000)
