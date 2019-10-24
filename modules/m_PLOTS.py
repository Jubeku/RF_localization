# Plotting module

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib.dates import DateFormatter, MinuteLocator, SecondLocator
from modules.colormap2d import imshow2d

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


def plot_LOCA(loc_prob_time, t_rel, tstart, tend, swin):

    # Load DEM
    topo = np.loadtxt('data/DEM_PF_10m_cut.dat',skiprows=6)
    dx = 10
    dy = 10
    xx = np.arange(0.,2100.+dx,dx)
    yy = np.arange(0.,1800.+dy,dy)
    levels = np.arange(2190., 2650, 20)
    # Load station positions
    stas = np.loadtxt('data/stations.txt')
    stas_name = ['BON', 'BOR', 'DSO', 'SNE']
    xmin =  640.
    xmax = 1840.
    ymin =  400.
    ymax = 1400.

    fig, ax_im = plt.subplots( 1, 1, figsize=(12.,10.))
    im = imshow2d(loc_prob_time, ax=ax_im, cmap2d='brightwheel',
            huevmin=0., huevmax=t_rel+2*swin,
            lightvmin=0.25, lightvmax=0.55,
            extent=[xmin, xmax, ymin, ymax],
            )

    co = ax_im.contour(xx, yy, np.flipud(topo),levels, colors='C5', alpha=0.5,linewidths=0.5)

    bbox = dict(boxstyle='round', fc='1',alpha=0.7,lw=0)
    ax_im.scatter(stas[:,0], stas[:,1],
            marker='^', c='C2', s=240, edgecolor='k',linewidth=0.3)
    for iista, sta in enumerate(stas_name):
        if iista == 0:
            xanno = -300.
            yanno =   20.
        elif iista == 1:
            xanno = -140.
            yanno = -150.
        elif iista == 2:
            xanno =   70.
            yanno = -110.
        elif iista == 3:
            xanno = -300.
            yanno =  -30.
        anno = (stas_name[iista])
        ax_im.annotate(anno, xy=(stas[iista,0],stas[iista,1]),
                xytext=(stas[iista,0]+xanno,stas[iista,1]+yanno),
                size=16, color='C2')

    ax_im.set_xlim(xx[0]+400., xx[-1]-200.)
    ax_im.set_ylim(yy[0]+300., yy[-1]-250.)
    ax_im.set_xticks([]) 
    ax_im.set_yticks([]) 
    
    plt.show()
   

def plot_Tr_Cb(tr, t1, t2, t_rel, swin):
    
    rc('font', size=18.0)

    fig = plt.figure(figsize=(10, 2.5))
    ax = fig.add_axes([0.1,0.35,0.8,0.6])
    
    #fig = plt.figure(figsize=(15, 3))
    #ax = fig.add_axes([0.1,0.4,0.8,0.6])
    
    ax.grid(which='both')
    ax.plot(tr.times('matplotlib'), tr.normalize().data , label=tr.stats.station)
    ax.axvline(t1,color='k',linestyle='--')
    ax.axvline(t2,color='k',linestyle='--')
    ax.autoscale(enable=True, axis='x', tight=True)
    ax.legend()
    ax.axis('off')

    t1 = 0.
    t2 = t_rel
    
    times = np.arange(t1, t2+swin, swin)
    dp = 0.01
    prob  = np.arange(0., 1.+dp    , 0.01 )
    mesht = np.tile(times, (len(prob),1))
    meshp = np.tile(prob, (len(times),1))
    color = np.array([mesht, meshp.transpose()])
    
    ax_cb = fig.add_axes([0.1,0.1,0.8,0.15])
    #ax_cb = fig.add_axes([0.1,0.1,0.8,0.13])
    
    im = imshow2d(color, ax=ax_cb, cmap2d='brightwheel',
                    huevmin=t1, huevmax=t2+2*swin,
                    lightvmin=0., lightvmax=1.,
                    origin = 'lower',
                    extent=[t1, t2, 0., 1.],
                    #interpolation='spline16'
                    aspect='auto'
                    )

    ax_cb.set_xlabel('Time (s)') 
    ax_cb.set_ylabel('PDF') 
    
    plt.show()
