# Rockfall localization

This repository contains an algorithm to localize rockfalls using seismic signals. 

A [Jupyter](https://jupyter.org/) notebook is used to present the localization method. You can explore yourself the method and the sensitivity of the results in respect to certain parameters. 

In case you don't have Jupyter installed or you want to run the notebook later, you can simply visualize the notebook using `nbviewer` following this [link](https://nbviewer.jupyter.org/github/Jubeku/RF_localization/blob/master/localize.ipynb).
    
The method is based on the comparison of observed and simulated seismic energy ratios between station pairs. In the following, the underlying numerical simulations of the seismic wave propagation are briefly introduced. 

## The simulated data used in the localization method

For simulating the seismic wave propagation, the Spectral Element Method (SEM) is used. In the following, the 




![Dolomieu map and Earth model](images/map_model.png)
![Simulation snapshots](images/snaps.png)
