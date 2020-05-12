"""
Calculate the coseismic displacement from the InSAR timeseries
input data - geo_timeseries.h5 (mintpy result)

created by Rishabh Dutta
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import h5py

# work directory
proj_dir = os.path.expanduser('/data/not_backed_up/rdtta/earthquakes/Utah2020/Sentinel/AT20/Stack/timeseries')

# file in geo coordinates
geom_file = os.path.join(proj_dir, 'geo/geo_geometryRadar.h5')
ts_file = os.path.join(proj_dir, 'geo/geo_timeseries_ramp_demErr.h5')

with h5py.File(ts_file, "r") as f:
    # read the timeseries file
    a_group_key = list(f.keys())[2]
    ts_data = list(f[a_group_key])
    a_group_key = list(f.keys())[1]
    dates = list(f[a_group_key])




