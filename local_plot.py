import numpy as np
from online_figure import OnlineFigure
import os.path
import os
from datetime import datetime, timedelta

def get_latest_file(path='.'):
    return sorted(
        [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))
         if f.startswith('log@')],
        key=lambda f: ''.join(f[4:-4].split('-'))
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
        return splitted[0] + r"\times10^{%d}"%int(splitted[1])

class LocalPlotter():
    def __init__(self, fname, pause=1, cast_time=False):
        self.fname = fname
        self.last_line = 0
           
        self.initial_time = datetime.strptime(os.path.split(fname)[-1][4:-4], "%Y-%m-%d-%H%M%S")
        if cast_time:
            self.fig = OnlineFigure(pause=pause, cast_time=True)
            # self.fig.ax.xaxis.set_major_formatter()
        else: 
            self.fig = OnlineFigure(pause=pause)
            self.fig.ax.set_xlabel(r'Time elapsed $t\,/\,\mathrm{s}$')
        
        self.fig.ax.set_title(r'Enclosure pressure')
        self.fig.ax.set_ylabel(r'Pressure $p\,/\,\mathrm{mbar}$')
        self.cast_time = cast_time
        
        self.update()
        self.fig.rescale_y()

    def update(self):
        data = np.genfromtxt(self.fname, delimiter=',', usecols=[0, 1])
        if self.last_line == len(data):  # nothing to update
            self.fig.display()  # just make it sleep a while
            return
        if self.cast_time: 
            time, obs = data[self.last_line:].T
            time = [self.initial_time + timedelta(seconds=td) for td in time]
            self.fig.appendln(time, obs)
        else:
            self.fig.appendln(*(data[self.last_line:].T))
        self.fig.ax.set_title(r'Enclosure pressure $%s\,\mathrm{mbar}$' % sci2tex("%.2e"%data[-1,1]))
        self.last_line = len(data)


path = './'

fname = input('Enter file name (or press enter if use latest): \n').strip()
if not fname: 
    fname = get_latest_file()
    print(fname)
lp = LocalPlotter(os.path.join(path, fname), 5, True)
while True:
    lp.update()
    