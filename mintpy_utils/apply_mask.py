"""
Apply mask to the coseismic displacement 
input data - geo_maskTempCoh.h5 (mintpy result)
             coseismic_disp.mat

created by Rishabh Dutta
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import h5py
import scipy.io as sio
import sys

# load the coseismic_disp.mat file 
mat_ts = sio.loadmat('coseismic_disp.mat')
coseismic_disp = mat_ts['coseismic_disp']

# load the mask 
proj_dir = os.path.expanduser('/data/not_backed_up/rdtta/earthquakes/Utah2020/Sentinel/AT20/Stack/timeseries')
maskfile = os.path.join(proj_dir, 'geo/geo_maskTempCoh.h5')

with h5py.File(maskfile, "r") as f:
    a_group_key = list(f.keys())[0]
    maskbool = list(f[a_group_key])

maskbool = np.array(maskbool)

for i in range(np.shape(maskbool)[0]):
    for j in range(np.shape(maskbool)[1]):
        if maskbool[i,j] == False:
            coseismic_disp[i,j] = np.nan

varname1 = 'coseismic_disp_mask.mat'
sio.savemat(varname1, {'coseismic_disp':coseismic_disp})


