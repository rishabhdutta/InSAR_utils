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

with h5py.File(maskfile, "r") as f:
    a_group_key = list(f.keys())[0]
    maskbool = list(f[a_group_key])

maskbool = np.array(maskbool)

mat_c1 = sio.loadmat('subsdata.mat')
longitude = mat_c1['lon']
latitude = mat_c1['lat']
subs_data = mat_c1['subs_data']

seasonal_subs = subs_data[:,1]
ifglen = np.shape(longitude)[0]
ifgwid = np.shape(longitude)[1]

def get_ALT(arg_i, ifglen, seasonal_subs):
    '''
    Estimate ALT from seasonal subsidence value
    '''
    if np.int(np.mod(arg_i, 50000)) == 0:
        print('in loop number : ', arg_i)
    ind_len = np.mod(arg_i, ifglen) - 1
    if np.mod(arg_i, ifglen) == 0:
        ind_len = ifglen - 1
    ind_wid = np.int(np.floor(arg_i/ifglen)) - 1
    # check if masked
    if maskbool[ind_len, ind_wid] == False:
        return np.nan
    seasubs = seasonal_subs[arg_i] 
    # mask if seasonal subsidence is negative 
    if seasubs < 0 :
        return np.nan 
    # check if subsidence is too small --> porosity 0.9 
    if seasubs <= 0.0028 :
        return seasubs*23/(2*0.9)
    elif seasubs >= 0.0353 :
        return .7+ (seasubs - 0.0353)*23/(2*0.44)
    else: 





