import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import scipy.io.wavfile
import scipy.signal


bitrate, data = scipy.io.wavfile.read('Windows Logon.wav')
xbeg = 17740
xend = 77740
x = data.T[0][int(xbeg):int(xend)]
#plt.plot(x)

stacksize = 400

fig = plt.figure()
ax = plt.axes(xlim = (100, 5000), ylim = (1, 10e5), xscale='log', yscale='log')

points = ax.plot([], [], marker='o')[0]

def animate(i):
    x_tek = x.reshape(-1, stacksize)[i]
    f, Pxx_den = scipy.signal.welch(x_tek, bitrate, nperseg=stacksize)
    points.set_data(f, Pxx_den)
       

anim = animation.FuncAnimation(fig, animate, frames=x.shape[0]//stacksize, interval=1000/20)

