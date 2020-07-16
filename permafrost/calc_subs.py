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

a_dictionary = {}
mat_c1 = np.empty(())
for years in years_incl:
    varmat_load = 'data_temp_addt/ds633/addt' + str(np.int(years)) + '.mat'
    mat_c1 = sio.loadmat(varmat_load)
    lonlat = mat_c1['lonlat']
    var_addt = 'addt' + str(np.int(years))
    a_dictionary["addt_%s" %np.int(years)] = mat_c1[var_addt]
    a_dictionary["detailsaddt_%s" %np.int(years)] = mat_c1['details_addt']

# get the timeseries data attributes 
ifglen = np.shape(longitude)[0]
ifgwid = np.shape(longitude)[1]
ts_data = np.array(ts_data)
longitude = np.array(longitude)
latitude = np.array(latitude)

numpixels = ifglen*ifgwid

lonvals_addt = lonlat[:,0] - 360
latvals_addt = lonlat[:,1]

# normalize the addt values with the overall maximum value 
maxaddt = np.zeros((years_incl.shape[0], 1))
i = 0 
for years in years_incl:
    varaddt = "addt_" + str(np.int(years))
    maxaddt[i] = np.max(a_dictionary[varaddt])
    i = i+1
maxaddtall = np.max(maxaddt) # maximum addt value

addt_pixelwise = np.zeros((include_dates.shape[0], ifglen, ifgwid))
for i in range(numpixels):
    if np.mod(i, 50000) == 0:
        print('loops completed: ', i)
    ind_len = np.mod(i+1, ifglen) - 1 
    if np.mod(i+1, ifglen) == 0: 
        ind_len = ifglen -1 
    ind_wid = np.int(np.floor((i+1)/ifglen)) - 1
    if maskbool[ind_len, ind_wid] == False:
        continue 
    # get the latitude and longitude at the index 
    lon_valind = longitude[ind_len, ind_wid]
    lat_valind = latitude[ind_len, ind_wid]
    # find the closest lonlat of the addt values 
    abs_dist_lon = np.abs(lonvals_addt - lon_valind)
    abs_dist_lat = np.abs(latvals_addt - lat_valind)
    ind_close1 = np.where(abs_dist_lon == np.min(abs_dist_lon))
    ind_close2 = np.where(abs_dist_lat == np.min(abs_dist_lat))
    indcommon = np.intersect1d(ind_close1, ind_close2)
    if indcommon.shape[0] > 1: 
        indcommon = indcommon[0]
    ind_tsdate = 0 
    # go through the time series dates and find the corresponding addt values
    for day in dates_frac_included:
        if np.mod(np.floor(day),4) > 0:
            leapdays = 365 
        else: 
            leapdays = 366
        dayindex = (day - np.floor(day))* leapdays + .5
        varaddt1 = "detailsaddt_" + str(np.int(np.floor(day)[0]))
        firstday_addt = a_dictionary[varaddt1][indcommon, 1]
        varaddt2 = "addt_" + str(np.int(np.floor(day)[0]))
        if firstday_addt > dayindex: 
            addt_pixelwise[ind_tsdate, ind_len, ind_wid] = 1e-5 
        else: 
            day_diff = dayindex - firstday_addt 
            addt_pixelwise[ind_tsdate, ind_len, ind_wid] = a_dictionary[varaddt2][indcommon, np.int(np.round(day_diff[0]))]/maxaddtall
        ind_tsdate = ind_tsdate + 1

hf = h5py.File('data.h5', 'r')
addt_pixelwise = hf.get('addt_ts')
addt_pixelwise = np.array(addt_pixelwise)
hf.close()

def x_est(arg_i, ifglen, dates_frac_included, include_dates, ts_data, addt_pixelwise):
    '''
    Estimate the overall and seasonal subsidence 
    '''
    if np.int(np.mod(arg_i, 50000)) == 0: 
        print('in loop number : ', arg_i)
    ind_len = np.mod(arg_i, ifglen) - 1
    if np.mod(arg_i, ifglen) == 0: 
        ind_len = ifglen - 1 
    ind_wid = np.int(np.floor(arg_i/ifglen)) - 1 
    # check if masked 
    if maskbool[ind_len, ind_wid] == False:
        return np.array([[np.nan],[np.nan]])
    # get the matrix B 
    Bmat = ts_data[include_dates, ind_len, ind_wid]
    Bmat = np.reshape(Bmat, (Bmat.shape[0], 1))
    # get the matrix A 
    # first column is time in year (to get subsidence/year)
    fir_colm = dates_frac_included - dates_frac_included[0]
    sec_colm = addt_pixelwise[:, ind_len, ind_wid]
    sec_colm = np.reshape(sec_colm, (sec_colm.shape[0], 1))
    Amat = np.concatenate((fir_colm, sec_colm), axis = 1)
    # solution of Ax = B 
    AtA = np.matmul(Amat.conj().transpose(), Amat)
    AtB = np.matmul(Amat.conj().transpose(), Bmat)
    solx = np.linalg.solve(AtA, AtB)
    return solx

num_cores = multiprocessing.cpu_count()
x_est_ = partial(x_est, ifglen = ifglen, dates_frac_included = dates_frac_included, include_dates= include_dates, ts_data= ts_data, addt_pixelwise = addt_pixelwise)
output = Parallel(n_jobs=num_cores)(delayed(x_est_)(i) for i in range(numpixels))

subs_data = np.array(output)
hf = h5py.File('subs_data.h5', 'w')
hf.create_dataset('subs_data', data=subs_data)
hf.create_dataset('lon', data=longitude)
hf.create_dataset('lat', data=latitude)
hf.close()

    

