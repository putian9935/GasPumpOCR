import numpy as np
from online_figure import OnlineFigure
from time import sleep 
import os.path 
import os 


def get_latest_file():
    return sorted([f for f in os.listdir('.') if os.path.isfile(f) if f.startswith('log@')], 
                  key=lambda f:''.join(f[4:-4].split('-'))
           )[-1]

class LocalPlotter():
    def __init__(self, fname):
        self.fname = fname 
        self.last_line = 0 

        self.fig = OnlineFigure(pause=1)
        self.fig.ax.set_title(r'Enclosure pressure')
        self.fig.ax.set_xlabel(r'Time elapsed $t\,/\,\mathrm{s}$')
        self.fig.ax.set_ylabel(r'Pressure $p\,/\,\mathrm{mbar}$')
        
        self.update()
        self.fig.rescale_y()


    def update(self):
        data = np.genfromtxt(self.fname, delimiter=',', usecols=[0,1])
        if self.last_line == len(data):  # nothing to update 
            return 
        self.fig.appendln(*(data[self.last_line:].T))
        self.last_line = len(data) 
    
    
path = './'

fname = input('Enter file name (or press enter if use latest): \n').strip()
if not fname: 
    fname = get_latest_file()
    print(fname)
lp = LocalPlotter(os.path.join(path, fname))
while True:
    lp.update()
    sleep(1)
