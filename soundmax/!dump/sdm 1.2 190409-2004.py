



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

bitrate = 44100
downsamplerate = 10  # осреднение пачками по n (микрофон не дает ничего, кроме 44100)
blocksize = 4410  # величина блока, забираемого из потока (на значениях более 20000 глючит)
buffersize = 2  # величина буфера (в блоках)
stacksize = 1  # величина стека осреднения (в буферах)

aw_data = np.array((6.3, -85.4,
                    6.3, -85.4,
                      8, -77.8,
                     10, -70.4,
                   12.5, -63.4,
                     16, -56.7,
                     20, -50.5,
                     25, -44.7,
                     31.5, -39.4,
                     40, -34.6,
                     50, -30.2,
                     63, -26.2,
                     80, -22.5,
                    100, -19.1,
                    125, -16.1,
                    160, -13.4,
                    200, -10.9,
                    250, -8.6,
                    315, -6.6,
                    400, -4.8,
                    500, -3.2,
                    630, -1.9,
                    800, -0.8,
                   1000, 0,
                   1250, 0.6,
                   1600, 1,
                   2000, 1.2,
                   2500, 1.3,
                   3150, 1.2,
                   4000, 1,
                   5000, 0.5,
                   6300, -0.1,
                   8000, -1.1,
                  10000, -2.5,
                  12500, -4.3,
                  16000, -6.6,
                  20000, -9.3))
aw = aw_data[::2], aw_data[1:][::2]

#GdB = 20log_10(A2/A1)
#A2 = A1 * 10**(Gdb/20)

def abydb(A1, Gdb):
    A2 = A1 * 10**(Gdb / 20)
    return A2










fig = plt.figure()
xlim = (1e1, 1e4)  # диапазон частот
ylim = (1e-9, 1e4)  # диапазон плотностей
ax = plt.axes(xlim=xlim, ylim=ylim, xscale='log', yscale='log')

points = ax.plot([], [], marker='.')[0]  # заготовка

def animate(i):
    stack = np.zeros((stacksize, 438))
    for j in range(stacksize):

        # %%
        buffer = np.zeros((buffersize, blocksize//downsamplerate))
        for i in range(buffersize):
            def callback(indata, frames, time, status):
                dsblock = scipy.signal.decimate(indata.T[0], downsamplerate)
    #                print(dsblock.shape)
                buffer[i].put(np.arange(dsblock.size), dsblock)
            with sd.InputStream(device=1, callback=callback,
                                blocksize=blocksize, channels=1):
                sd.sleep(int(blocksize / bitrate * 1000 + 42))

        spec =  np.abs(np.fft.fft(buffer.flatten()))**2
        freq = np.fft.fftfreq(buffer.flatten().size, 1/(bitrate/downsamplerate))
        idx = np.argwhere((freq > 13.75) & (freq < 500000))
        spec_cut = spec[idx]
        freq_cut = freq[idx]
        spec_cut_aw = abydb(spec_cut, np.interp(freq_cut, aw[0], aw[1]))   # A-weighting
    #        ax = plt.axes(xlim=xlim, ylim=ylim, xscale='log', yscale='log')
    #        ax.plot(freq_cut, spec_cut)
    #        spec_cut.shape

        # %%

        stack[j] = spec_cut_aw.flatten()
    #        print(np.mean(stack, 0).shape)
    points.set_data(freq_cut, np.mean(stack, 0))


fps = 2
anim = animation.FuncAnimation(fig, animate, frames=42, interval=1000/fps)







