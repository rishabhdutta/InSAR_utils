#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 09:58:50 2020

@author: duttar
Description: Solving the problem A = Bx 
A is the timeseries stack of InSAR pixel wise 
B is matrix including time and ADDT 
x is a vector containing seasonal and overall subsidence 

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

def datenum(d):
    '''
    Serial date number
    used for SBI_Year
    '''
    return 366 + d.toordinal() + (d - dt.fromordinal(d.toordinal())).total_seconds()/(24*60*60)

def SBI_Year(imd):
    '''
    A simple script that takes in numbers on the format '19990930'
    and changes to a number format 1999.7590
    imd - numpy (n,1) Vector with dates in strings
    out - numpy (n,1) Vector with dates in int
    created by Rishabh Dutta
    '''
    dstr = imd
    nd = imd.shape[0]
    out = np.zeros((nd,1))
    for k in range(nd):
        # get first day of year, minus 1/2 a day:
        d1 = dt.strptime(dstr[k][0][0:4]+'0101', '%Y%m%d')
        dn1 = datenum(d1) - 0.5 
        # get last day of year, plus 0.5
        d2 = dt.strptime(dstr[k][0][0:4]+'1231', '%Y%m%d')
        dne = datenum(d2) + 0.5
        # get number of days in that year:
        ndays = dne - dn1 
        # get day of year:
        d3 = dt.strptime(dstr[k][0], '%Y%m%d')
        doy = datenum(d3) - dn1 
        # get fractional year:
        fracyr = doy/ndays
        out[k] = int(dstr[k][0][0:4])+ fracyr 
    return out

# work directory
proj_dir = os.path.expanduser('/data/not_backed_up/rdtta/Permafrost/Alaska/North_slope/DT102/Stack/timeseries')

# file in geo coordinates
geom_file = os.path.join(proj_dir, 'geo/geo_geometryRadar.h5')
ts_file = os.path.join(proj_dir, 'geo/geo_timeseries_ramp_demErr.h5')
maskfile = os.path.join(proj_dir, 'geo/geo_maskTempCoh.h5')

with h5py.File(ts_file, "r") as f:
    # read the timeseries file
    a_group_key = list(f.keys())[2]
    ts_data = list(f[a_group_key])
    a_group_key = list(f.keys())[1]
    dates = list(f[a_group_key])

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

# convert dates from type 'bytes' to string 
numdates = np.size(dates)
datesn = np.empty([numdates, 1], dtype="<U10")
dates_int = np.zeros((numdates,1))
for i in range(numdates):
    datesn[i] = dates[i].decode("utf-8")
    dates_int[i] = int(dates[i].decode("utf-8"))

dates_frac = SBI_Year(datesn)

# select the dates to put in matrix A 
inddates = np.zeros((numdates,1))
for i in range(numdates):
    dates_i = dates_frac[i]
    frac_part = dates_i - np.floor(dates_i)
    if frac_part < .41506849 :
        inddates[i] = 0 
    elif frac_part > .81506849 : 
        inddates[i] = 0 
    else: 
        inddates[i] = 1 

include_dates = np.where(inddates == 1)[0]
print('included dates for estimation are: \n', datesn[include_dates]) 

dates_frac_included = dates_frac[include_dates]

# load the addt files 
dates_floor = np.floor(dates_frac_included)
for i in range(include_dates.shape[0]-1):
    if i == 0:
        years_incl = dates_floor[i]
    if dates_floor[i+1] != dates_floor[i]:
        years_incl = np.concatenate((years_incl, dates_floor[i+1]), axis=0)

for i in range(years_incl.shape[0]):
    varmat_load = 


# get the timeseries data attributes 
ifglen = np.shape(longitude)[0]
ifgwid = np.shape(longitude)[1]
ts_data = np.array(ts_data)
longitude = np.array(longitude)
latitude = np.array(latitude)

numpixels = ifglen*ifgwid

def x_est(arg_i):
    '''

    '''
    ind_len = np.mod(arg_i, ifglen) - 1
    if ind_len == 0 : 
        ind_len = ifglen - 1 
    ind_wid = np.int(np.floor(arg_i/ifglen)) - 1 
    # check if masked 
    if maskbool[ind_len, ind_wid] == False: 
        continue
    # get the matrix A 
    Amat = ts_data[include_dates, ind_len, ind_wid]
    Amat = np.reshape(Amat, (Amat.shape[0], 1))
    # get the matrix B 
    # first column is time in year (to get subsidence/year)
    




    
