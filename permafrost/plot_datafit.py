#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 09:58:50 2020
@author: duttar
Description: Plotting the data fit of seasonal + overall subsidence result
to the time-series data 

"""
import numpy as np
import matplotlib.pyplot as plt
import h5py
from datetime import datetime as dt
import os
import scipy.io as sio
import argparse

parser = argparse.ArgumentParser(description='plot the timeseries and the data fit with the stefan model')
parser.add_argument('-y', '--yindex', type=str, metavar='', required=True, help='input y index value')
parser.add_argument('-x', '--xindex', type=str, metavar='', required=True, help='input x index value')

args = parser.parse_args()

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

dates_frac_included = dates_frac[include_dates]

ts_data = np.array(ts_data)
valy = np.int(args.yindex)
valx = np.int(args.xindex)

# make the forward model - get matrix B 
# matrix A 
fir_colm = dates_frac_included - dates_frac_included[0]

hf = h5py.File('data.h5', 'r')
addt_pixelwise = hf.get('addt_ts')
addt_pixelwise = np.array(addt_pixelwise)
hf.close()

sec_colm = addt_pixelwise[:, valx, valy]
sec_colm = np.reshape(sec_colm, (sec_colm.shape[0], 1))
thi_colm = np.ones((sec_colm.shape[0], 1))
Amat_1 = np.concatenate((fir_colm, sec_colm), axis = 1)
Amat = np.concatenate((Amat_1, thi_colm), axis = 1)

# x values 
mat_c1 = sio.loadmat('subsdata.mat')
subs_data = mat_c1['subs_data']
subs_data1 = subs_data[:, 0, 0]
ifglen = np.shape(longitude)[0]
ifgwid = np.shape(longitude)[1]
subs_data1 = np.reshape(subs_data1, (ifglen, ifgwid), order='F')  

subs_data2 = subs_data[:, 1, 0]
subs_data2 = np.reshape(subs_data2, (ifglen, ifgwid), order='F')
subs_data3 = subs_data[:, 2, 0]
subs_data3 = np.reshape(subs_data3, (ifglen, ifgwid), order='F')

sol_x = np.array([[subs_data1[valy-1,valx-1]], [subs_data2[valy-1,valx-1]], [subs_data3[valy-1,valx-1]]])
Bmat = np.matmul(Amat, sol_x)

fig, ax = plt.subplots()
ax.plot(dates_frac_included, ts_data[include_dates, valy-1, valx-1], 'bs', label="time series data")
ax.plot(dates_frac_included, Bmat, label="Stefan model")
ax.legend()
ax.set_xlabel('Year')
ax.set_ylabel('Displacements [m]')
title_var = 'Y: '+str(valy) + ', X: '+str(valx)
ax.set_title(title_var)
save_var = 'Y' + str(valy) + 'X' + str(valx) + '.png'
plt.savefig(save_var, dpi=150)


