import matplotlib.pyplot as plt
from collections.abc import Iterable
import matplotlib as mpl 

mpl.rc('font', size=6)  # should be smaller so as others can see the computer 

class OnlineFigure():
    def __init__(self, x=None, y=None, pause=.5):
        def construct_lst(arr):
            if isinstance(arr, Iterable):
                ret = [_ for _ in arr]
            elif isinstance(arr, (float, int)):
                ret = [arr]
            elif isinstance(arr, type(None)):
                ret = []
            else:
                raise Exception('Unidentified data type')
            return ret

        self.x = construct_lst(x)
        self.y = construct_lst(y)
        self.pause = pause
        if len(self.x) != len(self.y):
            raise Exception('Unequal length in x and y arrays')

        self.fig, self.ax = plt.subplots(figsize=(4,3))  # smaller for other users' ease 


        self.line,  = self.ax.plot(self.x, self.y, '-')
        self.ax.set_yscale('log')

    def rescale_y(self):
        ymin = min(self.y)
        if ymin > 0:
            ymin *= .95
        else:
            ymin *= 1.05
        ymax = max(self.y)
        if ymax > 0:
            ymax *= 1.05
        else:
            ymax *= .95
        self.ax.set_ylim(ymin, ymax)
        plt.pause(self.pause)


    def display(self):
        self.line.set_data(self.x, self.y)
        plt.pause(self.pause)

    def append(self, new_x, new_y):
        self.x.append(new_x)
        self.y.append(new_y)

        _, xmax = self.ax.get_xlim()
        if new_x > xmax:
            xmax = 1.05 * new_x
            self.ax.set_xlim(right=xmax)

        ymin, ymax = self.ax.get_ylim()
        if new_y > ymax:
            if new_y > 0:
                ymax = 1.05 * new_y
            else:
                ymax = .95 * new_y
            self.ax.set_ylim(ymin, ymax)
        if new_y < ymin:
            if new_y < 0:
                ymin = 1.05 * new_y
            else:
                ymin = .95 * new_y
            self.ax.set_ylim(ymin, ymax)

        self.display()


    def appendln(self, new_xs, new_ys):
        self.x.extend(new_xs) 
        self.y.extend(new_ys) 
        _, xmax = self.ax.get_xlim()
        if new_xs[-1] > xmax:
            xmax = 1.05 * new_xs[-1]
            self.ax.set_xlim(right=xmax)

        self.rescale_y()

        self.display()

        
if __name__ == '__main__':
    of = OnlineFigure()
    from random import random
    from time import perf_counter, sleep
    for i in range(1000):
        of.append(perf_counter(), random()*2-1)
        sleep(.2)
