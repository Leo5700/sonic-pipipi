
















import scipy.io.wavfile
import matplotlib.pyplot as plt
import numpy as np
import scipy
import scipy.signal


bitrate, data = scipy.io.wavfile.read('Windows Logon.wav')

xbeg = 33000
xend = xbeg + bitrate * 0.1
x = data.T[0][int(xbeg):int(xend)]

#####

plt.plot(x)

#####

plt.figure()
count, bins, ignored = plt.hist(x, 15, density=True)

#####

N = x.size
X = scipy.fft(x)
Xdb = 20*scipy.log10(scipy.absolute(X))
f = scipy.linspace(0, bitrate, N, endpoint=False)

plt.figure()
plt.plot(f, Xdb)

#####

spec = np.fft.fft(x)
freq = np.fft.fftfreq(x.size, d=1/bitrate)

plt.figure()
plt.plot(freq, spec)
#plt.xlim(0, 1000)
#plt.xscale('log')
#plt.yscale('log')

plt.figure()
plt.plot(freq, np.abs(spec))
#plt.xlim(0, 10000)
plt.xscale('log')
plt.yscale('log')

#####

f, Pxx_den = scipy.signal.welch(x, bitrate*2, nperseg=75)

plt.figure()
plt.semilogy(f, Pxx_den)
plt.plot(f, np.ones_like(f))
















