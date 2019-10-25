# Module for removing spectral site amplification 

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib.dates import DateFormatter, MinuteLocator, SecondLocator
import os

class cd:

    """
    Class for changing the current working directory
    
    """
    
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


def onclick(event):
    
    
    if event.button == 3 :
        print('button=%d, xdata=%f' %(event.button, event.xdata))
        with open("pickedTW.txt", "a") as f:
            f.write('%.6f  ' % (event.xdata))
        event.inaxes.axvline(event.xdata,color='C3',linestyle='--')
        print(event.inaxes)
        event.canvas.draw()
        event.canvas.flush_events()
    
    return()


def pickTW(tr, path_event):
    
    """

    """
    
    rc('font', size=12.0)
    
    fig = plt.figure(figsize=(10,4))
    ax  = fig.add_subplot(111)
    title = ('Click middle mouse button to select start of signal,\n' +
            ' click right mouse button to select end of signal.')
    label = tr.stats.station+'.'+tr.stats.channel[2]
    ax.set_title(title)
    ax.grid()
    ax.plot(tr.times('matplotlib'), tr.data,label=label)
    ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    ax.legend(loc=1)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('$v_Z$ (m/s)')
    # Format time axis
    if tr.stats.npts*tr.stats.delta > 80 :
        plt.gca().xaxis.set_minor_locator(
                SecondLocator(bysecond=range(10,60,10)) )
    else:
        plt.gca().xaxis.set_minor_locator(
                SecondLocator(bysecond=range( 5,60, 5)) )
    plt.gca().xaxis.set_minor_formatter( DateFormatter("%S''") )
    plt.gca().xaxis.set_major_locator( MinuteLocator(byminute=range( 0,60, 1)) )
    plt.gca().xaxis.set_major_formatter( DateFormatter('%H:%M:%S') )
    
    # Start the picking
    cid = fig.canvas.mpl_connect('button_press_event', onclick)

    plt.show()

    return()
