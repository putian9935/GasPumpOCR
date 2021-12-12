import numpy as np
from online_multi_figure import OnlineMultiFigure
import os.path
import os
import matplotlib.dates as md
from datetime import datetime, timedelta


def get_latest_file(path='.'):
    return sorted(
        [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))
         if f.startswith('log@')],
        key=lambda f: ''.join(f[4:-4].split('-'))
    )[-1]


def get_latest_temp_file(path='.'):
    return sorted(
        [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))
         if f.startswith('temp_log_1_')],
        key=lambda f: ''.join(f[11:-4])
    )[-1]


def sci2tex(sci_str):
    r"""Convert a sci string into tex style

    E.g.
    1.21e-7 to 1.21\times10^{-7}
    """
    splitted = tuple(sci_str.split('e'))
    if len(splitted) == 1:
        return splitted[0]
    else:
        return splitted[0] + r"\times10^{%d}" % int(splitted[1])


class LocalMultiPlotter():
    def __init__(self, fname, tempfname, main=(0,), twin=(1, 2, 3, 4,), pause=1):
        self.fname = fname
        self.fname_temp = tempfname
        self.last_line = 0
        self.last_line_temp = 0
        self.main = main
        self.twin = twin

        self.initial_time = datetime.strptime(
            os.path.split(fname)[-1][4:-4], "%Y-%m-%d-%H%M%S")

        self.fig = OnlineMultiFigure(
            len(main)+len(twin), main, twin, pause=pause, cast_time=True)

        self.fig.ax_main.set_title(r'Enclosure pressure')
        self.fig.ax_main.set_ylabel(r'Pressure $p\,/\,\mathrm{mbar}$')
        self.fig.ax_twin.set_ylabel(r'Temperature $T\,/\,^\circ\mathrm{C}$')

        self.update()
        self.update_tmp()
        self.fig.show()

    def update(self):
        try:
            data = np.genfromtxt(self.fname, delimiter=',', usecols=[0, 1])
        except PermissionError:  # possibly writing this file
            return

        if self.last_line == len(data):  # nothing to update
            return

        time, obs = data[self.last_line:].T
        time = [self.initial_time + timedelta(seconds=td) for td in time]
        self.fig.appendln(time, obs, 0)

        self.fig.ax_main.set_title(
            r'Enclosure pressure $%s\,\mathrm{mbar}$' % sci2tex("%.2e" % data[-1, 1]))
        self.last_line = len(data)

    def update_tmp(self):
        try:
            data = np.genfromtxt(self.fname_temp, delimiter=',',
                             usecols=[0, 2, 3, 4, 5])
        except PermissionError:  # possibly writing this file
            return

        if self.last_line_temp == len(data):  # nothing to update
            return

        time, *obs = data[self.last_line_temp:].T
        time = [datetime.utcfromtimestamp(
            ts)+timedelta(hours=8) for ts in time]

        for ob, twin_idx in zip(obs, self.twin):
            self.fig.appendln(time, ob, twin_idx)

        self.last_line_temp = len(data)


path = './'
fname = get_latest_file()
print("Pressure file: ", fname)

temppath = r'Q:\strontium\data\2021\20211207_enclosure_bake\bake-out-data'
tempname = get_latest_temp_file(path=temppath)
print("Temperature file:", tempname)

lmp = LocalMultiPlotter(os.path.join(path, fname),
                        os.path.join(temppath, tempname), pause=5)
while True:
    lmp.update()
    lmp.update_tmp()
    lmp.fig.show()
