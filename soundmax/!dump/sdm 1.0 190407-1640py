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
stacksize = 1  # число блоков для осреднения
nperseg = 200  # число "столбцов" для расчета плотности scipy.signal.welch
assert nperseg <= blocksize

fig = plt.figure()
xlim = (1e1, 1e5)  # диапазон частот
ylim = (1e-8, 1e8)  # диапазон плотностей
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


def bandsmeanamp(amp, freq, bands):
    '''
    помещаем на сетку bands средние значения amp ближайших freq
    [10. 11. 20. 30. 40. 55. 60.]
    [-1.  10.1  8.1  8.2 16.  18.  12. ]
    [ 1.  2.  4.  8. 16.]
    >>> [10.    0.    0.   30.25 47.5 ]
    '''
    assert amp.size == freq.size
    c = np.subtract.outer(freq, bands)  # разности
    d = np.argmin(np.abs(c), 1)  # какой элемент из freq, ближайшие к bands
#    ameans = np.zeros_like(bands)  # можно заливать подложку np.full(bands.size, np.nan)
    ameans = np.full(bands.size, np.nan)
    for i in np.unique(d):
        ameans[i] = np.mean(amp[np.argwhere(i==d)])
    return ameans


#t = np.random.randint(10, 3000, 100)

#plt.plot(t, 'bo')

#f = summtobands(t, bands)
#plt.plot(f, bands, 'go')

##############################################################################

def animate(i):
#    Pxx_den_stack = np.empty((stacksize, nperseg // 2 + 1))  ####
#    Pxx_den_stack = np.empty((stacksize, blocksize // 2 + 1))  ###

    Pxx_den_stack = np.empty((stacksize, bands.size))  #############
    for j in range(stacksize):



#        block = np.random.rand(blocksize)  ### симулируем поток realtime

        bitrate = 44100
        block = np.zeros(blocksize)
        def callback(indata, frames, time, status):
            block.put(np.arange(indata.T[0].size), indata.T[0])
        with sd.InputStream(device=1, callback=callback, blocksize=blocksize):
            sd.sleep(int(blocksize / bitrate * 1000))
#        plt.plot(block)

#        f, Pxx_den = scipy.signal.welch(block, bitrate, nperseg=nperseg,
#                                        scaling='dencity') ####
#        f, Pxx_den = scipy.signal.periodogram(block, bitrate) ###



        spec =  np.abs(np.fft.fft(block))**2
        freq = np.fft.fftfreq(block.size, 1/bitrate)
        idx = np.argwhere(freq < 5000)
#        plt.semilogy(freq[idx], spec[idx])

        f, Pxx_den = bands, bandsmeanamp(np.squeeze(spec[idx]), np.squeeze(freq[idx]), bands)
#        plt.plot(f, Pxx_den)

        Pxx_den_stack[j] = Pxx_den.T
#        plt.plot(Pxx_den)

    Pxx_den_aggr = np.mean(Pxx_den_stack, 0)  # TODO проработать "верхнюю огибающую"
#    plt.plot(Pxx_den_aggr)
    points.set_data(f, Pxx_den_aggr)  # отправка данных в заготовку

    for k in range(Pxx_den_aggr.size - 1):
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
#    block.put(list(range(indata.T[0].size)), indata.T[0])

#with sd.InputStream(device=1, callback=callback, blocksize=44100//10):
#    sd.sleep(1000)













