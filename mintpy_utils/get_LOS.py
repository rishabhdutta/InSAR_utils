"""
Get the Line-of-sight parameters: Azimuth and Incidence angle 
Input: geo_timeseries.h5
Output as a matlab file
"""
import os
import h5py
import scipy.io as sio

# work directory
proj_dir = os.path.expanduser('/data/not_backed_up/rdtta/earthquakes/Utah2020/Sentinel/AT20/Stack/timeseries')

# file in geo coordinates
geom_file = os.path.join(proj_dir, 'geo/geo_geometryRadar.h5')

with h5py.File(geom_file, "r") as f:
    a_group_key = list(f.keys())[0]
    azim_angle = list(f[a_group_key])
    a_group_key = list(f.keys())[2]
    inc_angle = list(f[a_group_key])

varname1 = 'los_AT20'
sio.savemat(varname1, {'azim_angle':azim_angle, 'inc_angle':inc_angle})

