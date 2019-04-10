



'''
┌ [[block, block, ...]]  ┐
│ [buffer]               │
│ [buffer]               │ stack
│ [buffer]               │
└ [...]                  ┘
'''


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import scipy.io.wavfile
import scipy.signal
import sounddevice as sd

blocksize = 4410  # величина блока, забираемого из потока
bitrate = 44100
downsamplerate = 10  # осреднение пачками по n (микрофон не дает ничего, кроме 44100)
buffersize = 4
stacksize = 2  # число блоков для осреднения

fig = plt.figure()
xlim = (1e1, 1e5)  # диапазон частот
ylim = (1e-8, 1e16)  # диапазон плотностей
ax = plt.axes(xlim=xlim, ylim=ylim, xscale='log', yscale='log')

points = ax.plot([], [], marker='.')[0]  # заготовка

def animate(i):
    stack = np.zeros((stacksize, 876))
    for j in range(stacksize):

        # %%
        buffer = np.zeros((buffersize, blocksize//downsamplerate))
        for i in range(buffersize):
            def callback(indata, frames, time, status):
                dsblock = scipy.signal.decimate(indata.T[0], downsamplerate)
                print(dsblock.shape)
                buffer[i].put(np.arange(dsblock.size), dsblock)
            with sd.InputStream(device=1, callback=callback,
                                blocksize=blocksize, channels=1):
                sd.sleep(int(blocksize / bitrate * 1000 + 42))

        spec =  np.abs(np.fft.fft(buffer.flatten()))**2
        freq = np.fft.fftfreq(buffer.flatten().size, 1/(bitrate/downsamplerate))
        idx = np.argwhere((freq > 13.75) & (freq < 500000))
        spec_cut = spec[idx]
        freq_cut = freq[idx]
#        ax = plt.axes(xlim=xlim, ylim=ylim, xscale='log', yscale='log')
#        ax.plot(freq_cut, spec_cut)
        spec_cut.shape

        # %%

        stack[j] = spec_cut.flatten()
#        print(np.mean(stack, 0).shape)
    points.set_data(freq_cut, np.mean(stack, 0))


fps = 1/5
anim = animation.FuncAnimation(fig, animate, frames=42, interval=1000/fps)







