import sounddevice as sd

print(sd.query_devices())

a = np.zeros((44100//10))

def callback(indata, frames, time, status):
    print(indata.shape)
    a.put(list(range(indata.T[0].shape[0])), indata.T[0])

with sd.InputStream(device=1, callback=callback, blocksize=44100//10):
    sd.sleep(1000)
