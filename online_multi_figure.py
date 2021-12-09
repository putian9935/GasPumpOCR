
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.dates as md

mpl.rc('font', size=6)  # should be smaller so as others can see the computer


class OnlineMultiFigure():
    def __init__(self, ncols, main, twin=None, pause=.5, cast_time=False):
        self.ncols = ncols
        self.x = [[] for _ in range(ncols)]
        self.y = [[] for _ in range(ncols)]

        self.pause = pause
        self.cast_time = cast_time
        if len(self.x) != len(self.y):
            raise Exception('Unequal length in x and y arrays')

        # smaller for other users' ease
        self.fig, self.ax_main = plt.subplots(figsize=(4, 3))
        if twin:
            self.ax_twin = self.ax_main.twinx()

        self.ax = dict()
        self.line = []
        for _ in range(ncols):
            if _ in main:
                self.line.append(self.ax_main.plot(self.x[_], self.y[_], '-')[0])
                self.ax[_] = self.ax_main
            else:
                self.line.append(self.ax_twin.plot(self.x[_], self.y[_], '-')[0])
                self.ax[_] = self.ax_twin

        self.ax_main.set_yscale('log')

    def rescale_y(self):
        cur_main_max = float("-inf")
        cur_main_min = float("inf")
        cur_twin_max = float("-inf")
        cur_twin_min = float("inf")
        for idx in range(self.ncols):
            if self.ax[idx] == self.ax_main:
                cur_main_max = max(cur_main_max, max(self.y[idx]))
                cur_main_min = min(cur_main_min, min(self.y[idx]))
            else: 
                cur_twin_max = max(cur_twin_max, max(self.y[idx]))
                cur_twin_min = min(cur_twin_min, min(self.y[idx]))
                
        self.ax_main.set_ylim(cur_main_min * .95, cur_main_max * 1.05)
        self.ax_twin.set_ylim(cur_twin_min * .95, cur_twin_max * 1.05)

    def display(self, idx):
        self.line[idx].set_data(self.x[idx], self.y[idx])
        if self.cast_time:
            td = self.x[0][-1] - self.x[0][0]
            self.ax_main.set_xlim(self.x[0][0], self.x[0][0] + td * 1.05)
            self.ax_main.xaxis.set_major_formatter(md.DateFormatter('%m-%d %H:%M'))
            plt.setp(self.ax_main.get_xticklabels(), rotation=45)

    def show(self):
        plt.tight_layout()
        plt.pause(self.pause)

    def appendln(self, new_xs, new_ys, idx):
        self.x[idx].extend(new_xs)
        self.y[idx].extend(new_ys)

        if not self.cast_time:
            _, xmax = self.ax[idx].get_xlim()
            if new_xs[-1] > xmax:
                xmax = 1.05 * new_xs[-1]
                self.ax[idx].set_xlim(right=xmax)
                
        self.display(idx)


if __name__ == '__main__':
    of = OnlineMultiFigure(3, (0, 1 ,2 ))
    of.appendln([1,2,3],[2,3,4],1)
    # from random import random
    # from time import perf_counter, sleep
    # for i in range(1000):
    #     of.append(perf_counter(), random()*2-1)
    #     sleep(.2)
