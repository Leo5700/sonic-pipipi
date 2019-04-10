# dencity spectrum median

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import scipy.io.wavfile
import scipy.signal
import sounddevice as sd

'''
┌ [block] ┐
│ [block] │
│ [block] │ stack
│ [block] │
└ [block] ┘
'''

blocksize = 800  # величина блока, забираемого из потока
stacksize = 10  # число блоков для осреднения
nperseg = 800  # число "столбцов" для расчета плотности scipy.signal.welch
assert nperseg <= blocksize

fig = plt.figure()
xlim = (1e1, 1e5)  # диапазон частот
ylim = (1e-14, 1e1)  # диапазон плотностей
ax = plt.axes(xlim=xlim, ylim=ylim, xscale='log', yscale='log')

points = ax.plot([], [], marker='.')[0]  # заготовка для плотности
point_extr = ax.plot([], [], 'ro')[0]  # заготовка для экстремума

def animate(i):
    Pxx_den_stack = np.empty((stacksize, nperseg // 2 + 1))  ####
#    Pxx_den_stack = np.empty((stacksize, blocksize // 2 + 1))  ###
    for j in range(stacksize):



#        block = np.random.rand(blocksize)  ### симулируем поток realtime

        block = np.zeros(blocksize)
        def callback(indata, frames, time, status):
#       print(indata.shape)
            block.put(list(range(indata.T[0].shape[0])), indata.T[0])
#        with sd.InputStream(device=1, callback=callback, blocksize=blocksize):
        with sd.InputStream(device=1, callback=callback, blocksize=blocksize, channels=1):

            sd.sleep(10)

#        plt.plot(block)

        bitrate = 44100  ### атрибут потока
        f, Pxx_den = scipy.signal.welch(block, bitrate, nperseg=nperseg) ####
#        f, Pxx_den = scipy.signal.periodogram(block, bitrate) ###

        Pxx_den_stack[j] = Pxx_den
#        plt.plot(Pxx_den)

    Pxx_den_aggr = np.mean(Pxx_den_stack, 0)  # TODO проработать "верхнюю огибающую"
#    plt.plot(Pxx_den_aggr)
    points.set_data(f, Pxx_den_aggr)  # отправка данных в заготовку

    for k in range(Pxx_den_aggr.shape[0] - 1):
        if Pxx_den_aggr[k + 1] < Pxx_den_aggr[k]:
            x_extr = f[k]
            y_extr = Pxx_den_aggr[k]
            break  # берем нижний экстремум
        else:
            x_extr, y_extr = 1, 1
    point_extr.set_data(x_extr, y_extr)

fps = 10
anim = animation.FuncAnimation(fig, animate, frames=42, interval=1000/fps)


a = np.zeros((44100//10))

#def callback(indata, frames, time, status):
#    print(indata.shape)
#    block.put(list(range(indata.T[0].shape[0])), indata.T[0])

#with sd.InputStream(device=1, callback=callback, blocksize=44100//10):
#    sd.sleep(1000)













