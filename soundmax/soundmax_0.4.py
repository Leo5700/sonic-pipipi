
















import scipy.io.wavfile
import matplotlib.pyplot as plt
import numpy as np
import scipy
import scipy.signal


bitrate, data = scipy.io.wavfile.read('Windows Logon.wav')

xbeg = 33022
xend = xbeg + bitrate * 1
#x = data.T[0][int(xbeg):int(xend)]
x = data.T[0]



plt.plot(x)

f, Pxx_den = scipy.signal.welch(x, bitrate*2, nperseg=75)

plt.figure()
plt.semilogy(f, Pxx_den)
plt.plot(f, np.ones_like(f))

