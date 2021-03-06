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

blocksize = 50000  # величина блока, забираемого из потока
stacksize = 1  # число блоков для осреднения

# расставим частоты по-рояльному
base = 2
octaves = 8
fractions = 16  # на сколько частей делить октаву, со всеми бемолями - 16 частей
x1, x2 = 13.75, 13.75 * base ** octaves
bands = np.logspace(np.log(x1)/np.log(base), np.log(x2)/np.log(base),
                    num=octaves*fractions+1, base=base)
# эта дробь с логарифмами - логарифм по основанию base
# https://en.wikipedia.org/wiki/Logarithm#Change_of_base


fig = plt.figure()
xlim = (1e1, 1e4)  # диапазон частот
ylim = (1e-8, 1e4)  # диапазон плотностей
ax = plt.axes(xlim=xlim, ylim=ylim, xscale='log', yscale='log')

points = ax.plot([], [], marker='.')[0]  # заготовка для плотности
#point_extr = ax.plot([], [], 'ro')[0]  # заготовка для экстремума


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






def animate(i):
#    spec_stack = np.empty((stacksize, bands.size))
    spec_stack = np.empty((stacksize, 5653))
    for j in range(stacksize):

        bitrate = 44100

        block = np.empty((blocksize//500, 500))
        # будем брать блок чатсями, на 40000 глюки
        for i in range(block.shape[0]):
            def callback(indata, frames, time, status):
                block[i].put(np.arange(indata.T[0].size), indata.T[0])
            with sd.InputStream(device=1, callback=callback, blocksize=500):
                sd.sleep(int(block.shape[0] / bitrate * 1000))


        spec =  np.abs(np.fft.fft(block.flatten()))**2
        freq = np.fft.fftfreq(block.size, 1/bitrate)
#        idx = np.argwhere(freq < 5000)
        idx = np.argwhere((freq > 13.75) & (freq < 5000))
        spec_cut = spec[idx]
        freq_cut = freq[idx]
#        specbybands = bandsmeanamp(np.squeeze(spec_cut), np.squeeze(freq_cut), bands)

#        spec_stack[j] = specbybands.T
        spec_stack[j] = spec_cut.T



#    spec_aggr = np.mean(spec_stack, 0)  # TODO проработать "верхнюю огибающую"

#    points.set_data(bands, spec_aggr)  # отправка данных в заготовку
    points.set_data(freq_cut, spec_cut)  # отправка данных в заготовку

#    for k in range(spec_aggr.size - 1):
#        if spec_aggr[k + 1] < spec_aggr[k]:
#            x_extr = bands[k]
#            y_extr = spec_aggr[k]
#            break  # берем нижний экстремум
#        else:
#            x_extr, y_extr = np.nan, np.nan
#    point_extr.set_data(x_extr, y_extr)
#
#    print(x_extr, y_extr)

fps = 2
anim = animation.FuncAnimation(fig, animate, frames=42, interval=1000/fps)













