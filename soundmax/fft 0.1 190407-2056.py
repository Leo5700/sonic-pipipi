# плотность мощности через быстрое преобразование Фурье

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import scipy.io.wavfile
import scipy.signal
import sounddevice as sd
import time

'''
┌ [block] ┐
│ [block] │
│ [block] │ stack
│ [block] │
└ [block] ┘
'''

blocksize = 44100//8  # величина блока, забираемого из потока
stacksize = 1000  # число блоков для осреднения амплитуд

base = 2  # основание интеграла для расчёта сетки частот, октава = 2
octaves = 8
fractions = 3  # делитель октавы, со всеми бемолями - 16 частей
x1, x2 = 13.75, 13.75 * base ** octaves
bands = np.logspace(np.log(x1)/np.log(base), np.log(x2)/np.log(base),
                    num=octaves*fractions+1, base=base)  # log по осн. base

xlim = (1e1, 1e3)  # диапазон частот
ylim = (1e-6, 1e1)  # диапазон плотностей


fig = plt.figure()
xlim = (1e1, 1e3)  # диапазон частот
ylim = (1e-6, 1e1)  # диапазон плотностей
ax = plt.axes(xlim=xlim, ylim=ylim, xscale='log', yscale='log')

bitrate = 44100

#spec_stack = np.empty((stacksize, 119))
spec_stack = []
for j in range(stacksize):
    block = np.empty(blocksize)
    def callback(indata, frames, time, status):
        block.put(np.arange(indata.T[0].size), indata.T[0])
    with sd.InputStream(device=1, callback=callback, blocksize=blocksize):
        sd.sleep(int(blocksize / bitrate * 1000))
#    time.sleep(1)
    spec =  np.abs(np.fft.fft(block))**2
    freq = np.fft.fftfreq(block.size, 1/bitrate)
    idx = np.argwhere((freq > 42) & (freq < 1000))
    if not np.isnan(spec[idx]).any():
#        spec_stack[j] = np.squeeze(spec[idx])
        spec_stack.append(np.squeeze(spec[idx]))

#    ax.plot(freq[idx], spec[idx])

spec_aggr = np.mean(np.array(spec_stack), 0)
ax.plot(freq[idx], spec_aggr, 'ro')

#plt.plot(freq[idx], spec_aggr)
#















