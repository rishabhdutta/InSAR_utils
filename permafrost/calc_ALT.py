#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 09:58:50 2020

@author: duttar
Description: Inverting for ALT from the seasonal subsidence results
Using mixed soil conditions: 
    a) .9 porosity for top organic layer
    b) exponential decay of porosity below organic layer
    c) .44 porosity for pure mineral

"""

import os
import numpy as np
import matplotlib.pyplot as plt
import h5py
from datetime import datetime as dt
import multiprocessing
from joblib import Parallel, delayed
from functools import partial
import scipy.io as sio


# work directory
proj_dir = os.path.expanduser('/data/not_backed_up/rdtta/Permafrost/Alaska/North_slope/DT102/Stack/timeseries')

# file in geo coordinates
geom_file = os.path.join(proj_dir, 'geo/geo_geometryRadar.h5')
ts_file = os.path.join(proj_dir, 'geo/geo_timeseries_ramp_demErr.h5')
maskfile = os.path.join(proj_dir, 'geo/geo_maskTempCoh.h5')

with h5py.File(geom_file, "r") as f:
    # read the geometry file
    a_group_key = list(f.keys())[0]
    azim_angle = list(f[a_group_key])
    a_group_key = list(f.keys())[1]
    height = list(f[a_group_key])
    a_group_key = list(f.keys())[2]
    inc_angle = list(f[a_group_key])
    a_group_key = list(f.keys())[3]
    latitude = list(f[a_group_key])
    a_group_key = list(f.keys())[4]
    longitude = list(f[a_group_key])

with h5py.File(maskfile, "r") as f:
    a_group_key = list(f.keys())[0]
    maskbool = list(f[a_group_key])

maskbool = np.array(maskbool)




