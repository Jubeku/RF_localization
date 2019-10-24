# Module for calculating error between simulations and observations

import numpy as np


def calc_prob(windowed_st, channels, ydim, xdim, freqID):
  
    ref = 'BON'
    dt = windowed_st[0].stats.delta
    
    probs_tw = np.zeros((ydim,xdim))
    for ch in channels:                
        if ch == 'Z':
            stas_name = ['BOR','DSO','SNE']
        else:
            stas_name = ['BOR','SNE']

        nRatios = len(stas_name)
        ratio_obs = np.zeros(nRatios)
        ### ENERGY RATIOS FROM DATA
        energy_curr_ref = np.trapz( 
                windowed_st.select(station=ref,channel='*'+ch)[0].data**2, 
                dx=dt )
        for idxSta, sta in enumerate(stas_name):
            energy_curr = np.trapz(
                    windowed_st.select(station=sta,channel='*'+ch)[0].data**2, 
                    dx=dt )
            ratio_obs[idxSta] = energy_curr/energy_curr_ref

        ### ENERGY RATIOS FROM SIMULATIONS
        if ch == 'Z':
            direc_comp = 'data/simu/vertZ/'
        elif ch == 'E':
            direc_comp = 'data/simu/horzX/'
        elif ch == 'N':
            direc_comp = 'data/simu/horzY/'
        path_simu_ref = direc_comp + ref + '/' 
        energy_simu_ref = np.loadtxt(path_simu_ref + freqID + '/energy_vz.txt')
        energy_simu_ref = np.reshape(energy_simu_ref,(ydim,xdim))

        ratios_simu = np.zeros((ydim,xdim,nRatios)) 
        for idxSrc, sta in enumerate(stas_name):
            path_simu = direc_comp  + sta + '/' 
            # Energy
            energy_simu = np.loadtxt(path_simu + freqID + '/energy_vz.txt')
            energy_simu = np.reshape(energy_simu,(ydim,xdim))
            ratios_simu[:,:,idxSrc] = energy_simu/energy_simu_ref
                    

        for ii in range(ydim):
            for jj in range(xdim):
                for kk in range(nRatios):
                    probs_tw[ii,jj] += 1./nRatios * (
                        np.abs(np.log10(ratios_simu[ii,jj,kk]/ratio_obs[kk])))

    return(probs_tw)
