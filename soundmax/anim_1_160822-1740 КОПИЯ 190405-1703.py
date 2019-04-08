#-*- coding: utf-8 -*-

from __future__ import division
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

fig = plt.figure()
ax = plt.axes(xlim = (-.3, 1.3), ylim = (-.3, 1.3))
points = ax.plot([], [], 'ro')[0]  # Заготовка объекта

def animate(i):

    x = np.random.rand(i)
    y = np.random.rand(i)   
   
    points.set_data(x, y)

anim = animation.FuncAnimation(fig, animate, frames = 10000, interval = 1000/24)


'''
animation.FuncAnimation?

Init signature: animation.FuncAnimation(self, fig, func, frames=None, 
init_func=None, fargs=None, save_count=None, **kwargs)

Docstring:
Makes an animation by repeatedly calling a function *func*, passing in
(optional) arguments in *fargs*.
[ Создаёт анимацию постоянно вызывая функцию *func*, передавая нечто в 
опциональные аргументы через *fargs* ]


*frames* can be a generator, an iterable, or a number of frames.
[ Номера кадров, могут быть генератором, итерируемым объектом, или просто 
интеджером, из которого автомарически получится номер кадра (начиная с нуля).
иначе говоря, "frames = 10" эквивалентно "frames = xrange(10)" ]


*init_func* is a function used to draw a clear frame. If not given, the
results of drawing from the first item in the frames sequence will be
used. This function will be called once before the first frame.
[ Функция, которая нарисует первый кадр. Если не задана, первым кадром будет
первый кадр *func*. Что естесственно. ]


If blit=True, *func* and *init_func* should return an iterable of
drawables to clear.
[ Если True, от функции *func* и *init_func* ждём итератор или 
какую-то геометрию чтобы что-то очистить. 
Мутная настройка, нужно проверить что здесь к чему.]


*kwargs* include *repeat*, *repeat_delay*, and *interval*:
*interval* draws a new frame every *interval* milliseconds.
*repeat* controls whether the animation should repeat when the sequence
of frames is completed.
*repeat_delay* optionally adds a delay in milliseconds before repeating
the animation.
[ *interval* -- интервал между кадрами, в милисекундах
*repeat* -- повторять или не повторять анимацию когда кадры кончатся, лупы
*repeat_delay* -- пауза между лупами]
'''





plt.show()