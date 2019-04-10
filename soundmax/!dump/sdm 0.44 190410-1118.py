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
stacksize = 100  # число блоков для осреднения
nperseg = 40  # число "столбцов" для расчета плотности scipy.signal.welch
assert nperseg <= blocksize

fig = plt.figure()
xlim = (1e1, 1e5)  # диапазон частот
ylim = (1e-2, 1e3)  # диапазон плотностей
ax = plt.axes(xlim=xlim, ylim=ylim, xscale='log', yscale='log')

points = ax.plot([], [], marker='.')[0]  # заготовка для плотности
point_extr = ax.plot([], [], 'ro')[0]  # заготовка для экстремума

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

def abydb(A1, Gdb):
    '''
    Получение новой амплитуды из исходной амплитуды и децибеллов (для звука)
    '''
    A2 = A1 * 10**(Gdb / 20)
    return A2


def animate(i):
#    Pxx_den_stack = np.empty((stacksize, nperseg // 2 + 1))
    Pxx_den_stack = np.empty((stacksize, blocksize))
    for j in range(stacksize):
        block = np.random.rand(blocksize)  ### симулируем поток realtime
        bitrate = 44100  ### атрибут потока # downsampling спасет мир scipy.signal.decimate(block, 10)  #берем каждого десятого
#        f, Pxx_den = scipy.signal.welch(block, bitrate, nperseg=nperseg)
#        Pxx_den_stack[j] = Pxx_den

        spec = np.abs(np.fft.fft(block)**2)
        freq = np.fft.fftfreq(block.size, 1/bitrate)

        f, Pxx_den = freq, spec

        Pxx_den_a = abydb(Pxx_den, np.interp(f, aw[0], aw[1]))  # A-weighting
        Pxx_den_stack[j] = Pxx_den_a
#        plt.plot(f, Pxx_den)
#        plt.plot(f, Pxx_den_a)

    Pxx_den_aggr = np.mean(Pxx_den_stack, 0)  # TODO проработать "верхнюю огибающую"
    points.set_data(f, Pxx_den_aggr)  # отправка данных в заготовку

    for k in range(Pxx_den_aggr.shape[0] - 1):
        if Pxx_den_aggr[k + 1] < Pxx_den_aggr[k]:
            x_extr = f[k]
            y_extr = Pxx_den_aggr[k]
            break  # берем нижний экстремум
        else:
            x_extr = np.nan
            y_extr = np.nan
    point_extr.set_data(x_extr, y_extr)

fps = 10
anim = animation.FuncAnimation(fig, animate, frames=42, interval=1000/fps)
