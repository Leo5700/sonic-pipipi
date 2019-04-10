# dencity spectrum median

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import scipy.io.wavfile
import scipy.signal

'''
┌ [block] ┐ 
│ [block] │
│ [block] │ stack
│ [block] │ 
└ [block] ┘
'''

blocksize = 1000
stacksize = 10
nperseg = 200  # чисто "столбцов" для расчета плотности scipy.signal.welch
assert nperseg <= blocksize

fig = plt.figure()
ax = plt.axes(xlim = (1e1, 1e5), ylim = (1e-6, 1e-4), xscale='log', yscale='log')

points = ax.plot([], [], marker='o')[0]


def animate(i):
#    windows = np.empty((stacksize, blocksize))
    Pxx_den_stack = np.empty((stacksize, nperseg // 2 + 1))
    for j in range(stacksize):
        block = np.random.rand(blocksize)  ### симулируем поток realtime
        bitrate = 44100  ### атрибут потока
        f, Pxx_den = scipy.signal.welch(block, bitrate, nperseg=nperseg)
        Pxx_den_stack[j] = Pxx_den
        
    Pxx_den_aggr = np.mean(Pxx_den_stack, 0)  # TODO проработать "верхнюю огибающую"
    points.set_data(f, Pxx_den_aggr)



anim = animation.FuncAnimation(fig, animate, frames=1000, interval=1000/10)














