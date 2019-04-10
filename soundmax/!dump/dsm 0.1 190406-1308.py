# dencity spectrum median

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import scipy.io.wavfile
import scipy.signal
import time


bitrate, data = scipy.io.wavfile.read('Windows Logon.wav')
xbeg = 17740
xend = 77740
x = data.T[0][int(xbeg):int(xend)]
#plt.plot(x)

blocksize = 1000
stacksize = 100

fig = plt.figure()
ax = plt.axes(xlim = (1e1, 1e5), ylim = (1e-6, 1e6), xscale='log', yscale='log')

points = ax.plot([], [], marker='o')[0]

# получаем поток из трека:
#def animate(i):
#    windows = x.reshape(-1, blocksize * stacksize)[i]
#    for window in windows.reshape(-1, blocksize):
#        f, Pxx_den = scipy.signal.welch(window, bitrate, nperseg=blocksize)
#        points.set_data(f, Pxx_den)



# симулируем поток realtime:

def animate(i):
#    windows = np.empty((stacksize, blocksize))
    Pxx_den_stack = np.empty((stacksize, blocksize // 2 + 1))
    for j in range(stacksize):
        block = np.random.rand(blocksize)  ### Здесь получаем данные потока
        f, Pxx_den = scipy.signal.welch(block, bitrate, nperseg=blocksize)
        Pxx_den_stack[j] = Pxx_den
        
    Pxx_den_med = np.mean(Pxx_den_stack, 0)
    points.set_data(f, Pxx_den_med)



anim = animation.FuncAnimation(fig, animate, frames=x.shape[0] // (blocksize * stacksize), interval=1000/10)














