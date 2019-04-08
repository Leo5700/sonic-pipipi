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

blocksize = 666  # величина блока, забираемого из потока
stacksize = 1000  # число блоков для осреднения
nperseg = 40  # число "столбцов" для расчета плотности scipy.signal.welch
assert nperseg <= blocksize

fig = plt.figure()
xlim = (1e1, 1e5)  # диапазон частот
ylim = (1e-6, 1e-4)  # диапазон плотностей
ax = plt.axes(xlim=xlim, ylim=ylim, xscale='log', yscale='log')

points = ax.plot([], [], marker='.')[0]  # заготовка
point_extr = ax.plot([], [], 'ro')[0]  # заготовка

def animate(i):
    Pxx_den_stack = np.empty((stacksize, nperseg // 2 + 1))
    for j in range(stacksize):
        block = np.random.rand(blocksize)  ### симулируем поток realtime
        bitrate = 44100  ### атрибут потока
        f, Pxx_den = scipy.signal.welch(block, bitrate, nperseg=nperseg)
        Pxx_den_stack[j] = Pxx_den

    Pxx_den_aggr = np.mean(Pxx_den_stack, 0)  # TODO проработать "верхнюю огибающую"
    points.set_data(f, Pxx_den_aggr)  # отправка данных в заготовку

fps = 10
anim = animation.FuncAnimation(fig, animate, frames=42, interval=1000/fps)







