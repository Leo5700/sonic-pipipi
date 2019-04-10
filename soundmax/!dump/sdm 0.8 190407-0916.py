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

blocksize = 4410  # величина блока, забираемого из потока
stacksize = 10  # число блоков для осреднения
nperseg = 200  # число "столбцов" для расчета плотности scipy.signal.welch
assert nperseg <= blocksize

fig = plt.figure()
xlim = (1e1, 1e5)  # диапазон частот
ylim = (1e-2, 1e1)  # диапазон плотностей
ax = plt.axes(xlim=xlim, ylim=ylim, xscale='log', yscale='log')

points = ax.plot([], [], marker='.')[0]  # заготовка для плотности
point_extr = ax.plot([], [], 'ro')[0]  # заготовка для экстремума


# расставим частоты по-рояльному
base = 2
octaves = 8
fractions = 3  # на сколько частей делить октаву, со всеми бемолями - 16 частей
x1, x2 = 13.75, 13.75 * base ** octaves
bands = np.logspace(np.log(x1)/np.log(base), np.log(x2)/np.log(base),
                    num=octaves*fractions+1, base=base)
# эта дробь с логарифмами - логарифм по основанию base
# https://en.wikipedia.org/wiki/Logarithm#Change_of_base
#plt.plot(bands, 'ro')


def summtobands(data, bands):  # TODO нужно не суммировать, а осреднять
    '''
    a = np.array((0, 0.1, 8.1, 8.2))
    b = np.array((1.0,  2,  4,  8, 16))
    >>> [ 0.1  0.   0.  16.3  0. ]
    '''
    a = data
    b = bands
    c = np.subtract.outer(a, b)  # разности
    d = np.argmin(np.abs(c), 1)  # индексы *a*, ближайших к *b*
    f = np.zeros_like(b)
    for a1, d1 in zip(a, d):
        f[d1] += a1
    return f


#t = np.random.randint(10, 3000, 100)

#plt.plot(t, 'bo')

#f = summtobands(t, bands)
#plt.plot(f, bands, 'go')

##############################################################################

def animate(i):
#    Pxx_den_stack = np.empty((stacksize, nperseg // 2 + 1))  ####
#    Pxx_den_stack = np.empty((stacksize, blocksize // 2 + 1))  ###

    Pxx_den_stack = np.empty((stacksize, 2202))  #############
    for j in range(stacksize):



#        block = np.random.rand(blocksize)  ### симулируем поток realtime

        bitrate = 44100
        block = np.zeros(blocksize)
        def callback(indata, frames, time, status):
            block.put(np.arange(indata.T[0].shape[0]), indata.T[0])
        with sd.InputStream(device=1, callback=callback, blocksize=blocksize):
            sd.sleep(int(blocksize / bitrate * 1000))
#        plt.plot(block)

#        f, Pxx_den = scipy.signal.welch(block, bitrate, nperseg=nperseg,
#                                        scaling='dencity') ####
#        f, Pxx_den = scipy.signal.periodogram(block, bitrate) ###



        spec =  np.abs(np.fft.fft(block))**2
        freq = np.fft.fftfreq(block.shape[0], 1/bitrate)
        idx = np.argwhere(25 < freq)
#        plt.semilogy(freq[idx], spec[idx])

        f, Pxx_den = freq[idx], spec[idx]


        Pxx_den_stack[j] = Pxx_den.T
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


#a = np.zeros((44100//10))

#def callback(indata, frames, time, status):
#    print(indata.shape)
#    block.put(list(range(indata.T[0].shape[0])), indata.T[0])

#with sd.InputStream(device=1, callback=callback, blocksize=44100//10):
#    sd.sleep(1000)













