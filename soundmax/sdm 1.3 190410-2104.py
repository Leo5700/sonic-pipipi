'''
* скрипт накапливает данные с микрофона, после чего расчитывает спектр,
осреднённый по амплитудам
* изначально планировалось вычленять из спектра доминирующие частоты, онако,
в итоге осталась только задача зрительного анализа спектра
* сигнал, сразу после получения, даунсемплится 1) для уменьшения числа
вычислений 2) т.к. частоты выше килогерца меня не интересуют 3) т.к. низкий
битрейт позволяет получить более высокое разрешение преобразование фурье
на низких частотах (из коробки, без плясок с бубном)
* можно включть/выключить анимацию, предварительно уменьшив (раз в 10) размеры
буфера и стека
* структура данных выглядит так:
┌ block ┐
│ block │ buffer ┐
│ block │ buffer │ stack
│ block │ ...    ┘
└ ...   ┘
'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import scipy.io.wavfile
import scipy.signal
import sounddevice as sd

devicenumber = 1  # номер микрофона sd.query_devices()

bitrate = 44100  # этот (и никакой другой) битрейт выдает мой микрофон
downsamplerate = 10  # даунсемплинг (методом децимации), в n раз
blocksize = 4410 # величина блока, забираемого из потока (на значениях более
# 20000 появляются nan)
buffersize = 10  # величина буфера (в блоках)
stacksize = 12  # величина стека (в буферах), стек осредняется

print(blocksize * buffersize * stacksize / bitrate)  # с, чистое время сбора
# с учетом вычислений, можно умножать на 2

# данные для a-weighting
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
aw = aw_data[::2], aw_data[1:][::2]  # проучение 2х столбцов данных

# Соотношения децибеллов и амплитуд (для звуковых колебаний)
# GdB = 20log_10(A2/A1)  # 20 -- это вылезает квадрат из под логорифма
# A2 = A1 * 10**(Gdb/20)

def abydb(A1, Gdb):
    '''
    изменение амплитуды в соответствии с коэффициентом усиления
    '''
    A2 = A1 * 10**(Gdb / 20)
    return A2

# заготовки для отрисовки
fig = plt.figure()
xlim = (1e1, 1e4)
ylim = (1e-9, 1e4)
ax = plt.axes(xlim=xlim, ylim=ylim, xscale='log', yscale='log')
points = ax.plot([], [], marker='.')[0]

def f():
    stack = np.array(())

    for j in range(stacksize):
        buffer = np.zeros((buffersize, blocksize//downsamplerate))

        for i in range(buffersize):
            def callback(indata, frames, time, status):  # получение и даунсемплинг сигнала
                dsblock = scipy.signal.decimate(indata.T[0], downsamplerate)
                buffer[i].put(np.arange(dsblock.size), dsblock)
            with sd.InputStream(device=devicenumber, callback=callback,  #
                                blocksize=blocksize, channels=1):
                sd.sleep(int(blocksize / bitrate * 1000 + 42))  # 42 мс про запас
            print(j, i, end='\t')  # "прогрессбар"

        spec = np.abs(np.fft.fft(buffer.flatten()))**2  # мощность сигнала
        freq = np.fft.fftfreq(buffer.flatten().size, 1/(bitrate/downsamplerate))  # сетка частот
        idx = np.argwhere((freq > 13.75) & (freq < 500000))  # отсечка хлама
        spec_cut = spec[idx]
        freq_cut = freq[idx]
        spec_cut_aw = abydb(spec_cut, np.interp(freq_cut, aw[0], aw[1]))   # A-weighting
        stack = np.append(stack, spec_cut_aw.flatten())

    points.set_data(freq_cut, np.mean(stack.reshape(int(stacksize), -1), 0))

# нижеследующий костыль организован для того, чтобы перекомментируя f()
# можно было включать анимацию для небольших значений времени сбора данных

f()  ###
def animate(i):
#    f() ###
    pass
fps = 10
anim = animation.FuncAnimation(fig, animate, frames=42, interval=1000/fps)
