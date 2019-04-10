
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure()
ax = plt.axes(xlim = (0, 150), ylim = (-6000, 6000))

points = ax.plot([], [])[0]

def animate(i):

    x_tek = x.reshape(-1, 150)[i]
    x_numbers =  np.linspace(0, x_tek.shape[0], x_tek.shape[0], endpoint=False)
    points.set_data(x_numbers, x_tek)

anim = animation.FuncAnimation(fig, animate, frames=147, interval=1000/20)


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
