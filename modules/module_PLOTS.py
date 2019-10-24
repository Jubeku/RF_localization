# Plotting module

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, MinuteLocator, SecondLocator


def plot_traces(st,title):
    fig, ax = plt.subplots(st.count(), 1, sharex=True, sharey=True,figsize=(8,10))
    ax[0].set_title(title)
    for itr, tr in enumerate(st):
        label = tr.stats.network+'.'+tr.stats.station+'.' \
                +tr.stats.location+'.'+tr.stats.channel
        ax[itr].grid(which='both')
        ax[itr].plot(tr.times('matplotlib'), tr.data,label=label)
        ax[itr].ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        if itr is not 0:
            ax[itr].yaxis.get_offset_text().set_visible(False)
        ax[itr].set(ylabel='$v_Z$ (m/s)')
        ax[itr].legend()

    ax[itr].set(xlabel='Time (s)')
    ### Bring subplots close to each other.
    fig.subplots_adjust(hspace=0.1)
    ### Hide x labels and tick labels for all but bottom plot.
    for axi in ax:
        axi.label_outer()
    ### Format time axis
    if st[0].stats.npts*st[0].stats.delta > 80 :
        plt.gca().xaxis.set_minor_locator( SecondLocator(bysecond=range(10,60,10)) )
    else:
        plt.gca().xaxis.set_minor_locator( SecondLocator(bysecond=range( 5,60, 5)) )
    plt.gca().xaxis.set_minor_formatter( DateFormatter("%S''") )
    plt.gca().xaxis.set_major_locator( MinuteLocator(byminute=range( 0,60, 1)) )
    plt.gca().xaxis.set_major_formatter( DateFormatter('%H:%M:%S') )
    
    plt.show()
