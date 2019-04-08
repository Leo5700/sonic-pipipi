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

blocksize = 3333  # величина блока, забираемого из потока
stacksize = 2  # число блоков для осреднения
nperseg = 3333  # число "столбцов" для расчета плотности scipy.signal.welch
assert nperseg <= blocksize

bitrate = 44100  ### атрибут потока

fig = plt.figure()
xlim = (1e2, 1e3)  # диапазон частот
ylim = (1e-14, 1e-4)  # диапазон плотностей
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

            sd.sleep(int(blocksize / bitrate * 1000 + 1))


#        plt.plot(block)


        f, Pxx_den = scipy.signal.welch(block, bitrate, nperseg=nperseg) ####
#        f, Pxx_den = scipy.signal.periodogram(block, bitrate) ###


        Pxx_den_stack[j] = Pxx_den
#        Pxx_den_stack[j] = scipy.signal.lfilter(b, a, Pxx_den)
#        plt.plot(Pxx_den)

    idx = np.argwhere((f > 105) & (f < 900))
    Pxx_den_aggr = np.max(Pxx_den_stack[:, idx], 0)  # TODO проработать "верхнюю огибающую"
#    plt.plot(Pxx_den_aggr)
    points.set_data(f[idx], Pxx_den_aggr)  # отправка данных в заготовку

#    for k in range(Pxx_den_aggr.shape[0] - 2):
#        if Pxx_den_aggr[k] > Pxx_den_aggr[k + 1]:
#            x_extr = f[idx][k]
#            y_extr = Pxx_den_aggr[k]
#            break  # берем нижний экстремум
#        else:
#            x_extr, y_extr = np.nan, np.nan
    iextr = np.argmax(Pxx_den_aggr)
    x_extr, y_extr = f[idx][iextr], Pxx_den_aggr[iextr]
    point_extr.set_data(x_extr, y_extr)

fps = 20
anim = animation.FuncAnimation(fig, animate, frames=1, interval=1000/fps)


#a = np.zeros((44100//10))

#def callback(indata, frames, time, status):
#    print(indata.shape)
#    block.put(list(range(indata.T[0].shape[0])), indata.T[0])

#with sd.InputStream(device=1, callback=callback, blocksize=44100//10):
#    sd.sleep(1000)

'''

from numpy import pi, convolve
from scipy.signal.filter_design import bilinear
#from scipy.signal import lfilter
def a_weighting_coeffs_design(sample_rate):
    """Returns b and a coeff of a A-weighting filter.

    Parameters
    ----------
    sample_rate : scalar
        Sample rate of the signals that well be filtered.

    Returns
    -------
    b, a : ndarray
        Filter coefficients for a digital weighting filter.

    Examples
    --------
    >>> b, a = a_weighting_coeff_design(sample_rate)

    To Filter a signal use scipy lfilter:

    >>> from scipy.signal import lfilter
    >>> y = lfilter(b, a, x)

    See Also
    --------
    b_weighting_coeffs_design : B-Weighting coefficients.
    c_weighting_coeffs_design : C-Weighting coefficients.
    weight_signal : Apply a weighting filter to a signal.
    scipy.lfilter : Filtering signal with `b` and `a` coefficients.
    """

    f1 = 20.598997
    f2 = 107.65265
    f3 = 737.86223
    f4 = 12194.217
    A1000 = 1.9997
    numerators = [(2*pi*f4)**2 * (10**(A1000 / 20.0)), 0., 0., 0., 0.];
    denominators = convolve(
        [1., +4*pi * f4, (2*pi * f4)**2],
        [1., +4*pi * f1, (2*pi * f1)**2]
    )
    denominators = convolve(
        convolve(denominators, [1., 2*pi * f3]),
        [1., 2*pi * f2]
    )
    return bilinear(numerators, denominators, sample_rate)
b, a = a_weighting_coeffs_design(bitrate)

#scipy.signal.lfilter(b, a, Pxx_den_aggr)



'''


