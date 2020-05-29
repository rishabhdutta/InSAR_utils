"""
Get non-nan values from the masked connected component output file
input - maskConnComp.h5
output is displayed if few, otherwise an output is saved
"""

import os
import numpy as np
import h5py
import scipy.io as sio

# work directory
proj_dir = os.path.expanduser('/data/not_backed_up/rdtta/Permafrost/Alaska/North_slope/AT94/Stack/timeseries')

# file
maskcompconn_file = os.path.join(proj_dir, 'maskConnComp.h5')

with h5py.File(maskcompconn_file, "r") as f:
    a_group_key = list(f.keys())[0]
    maskval = list(f[a_group_key])

maskval = np.array(maskval)
ind_nomask = np.where(maskval==True)
ind_nomask = np.array(ind_nomask)

varname1 = 'maskval.mat'
sio.savemat(varname1, {'maskval':maskval, 'ind_nomask':ind_nomask})



