# Module for removing spectral site amplification 

import numpy as np
from scipy.interpolate import interp1d

def deconvolve_SE(tr):

    """
    This function removes site effects from seismic signals.
    The spectral site amplification functions were estimated from 
    volcano-tectonic (VT) seismic signals. Station BON is used as reference
    stations. 
    The site effects are removed in the frequency domain:
    Deconvolution in time domain -> division in frequency domain

    Input parameters
    tr:  Seismic signal (Obspy Trace)
    
    """


    # Define frequency range within which site effects are removed
    fmin = 2.
    fmax = 20.
    freqs = np.fft.fftfreq(tr.stats.npts, tr.stats.delta)
    fidx_pos = [ii for ii,ff in enumerate(freqs) if ff>=fmin and ff<=fmax]
    fidx_neg = [ii for ii,ff in enumerate(freqs) if ff>=-fmax and ff<=-fmin]
    fourier_tr = np.fft.fft(tr.data)*tr.stats.delta
    
    # Load site effect amplification fuctions estimated by VTs
    if tr.stats.channel[-1] == 'Z':
        sta_comp = 'vertZ/'
    elif tr.stats.channel[-1] == 'E':
        sta_comp = 'horzE/'
    elif tr.stats.channel[-1] == 'N':
        sta_comp = 'horzN/'
    path_SiteEff = 'data/site_effects/'+sta_comp
    tf = np.loadtxt(path_SiteEff+'transfer_fct_'+tr.stats.station+'.txt')
    # Interpolate site effect functions on signal frequencies
    f_tf = interp1d(tf[:,0],tf[:,1])
    tf_interp = f_tf(freqs[fidx_pos])
    
    # FFT of signal
    tr_fft = np.fft.fft(tr.data)*tr.stats.delta

    # Removal of site effects:
    tr_fft[fidx_pos] = tr_fft[fidx_pos]/tf_interp         
    tr_fft[fidx_neg] = tr_fft[fidx_neg]/np.flip(tf_interp, axis=0)

    # Transform to time domain
    tr.data = np.fft.ifft(tr_fft/tr.stats.delta).real

    return(tr)

