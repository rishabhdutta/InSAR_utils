"""
Calculate the coseismic displacement from the InSAR timeseries
input data - geo_timeseries.h5 (mintpy result)

created by Rishabh Dutta
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import h5py
from datetime import datetime as dt

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
        out[k] = int(dstr[k][0])+ fracyr 

    return out

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

# convert dates from type 'bytes' to string 
numdates = np.size(dates)
datesn = np.empty([numdates, 1], dtype="<U10")
dates_int = np.zeros((numdates,1))
for i in range(numdates):
    datesn[i] = dates[i].decode("utf-8")
    dates_int[i] = int(dates[i].decode("utf-8"))

# access the dates pixel wise and estimate coseismic disp. 
ifglen = np.shape(longitude)[0]
ifgwid = np.shape(longitude)[1]
ts_data = np.array(ts_data)
eq_date = '20200318'

for i in range(ifglen):
    for j in range(ifgwid):
    # timeseries at pixel (i,j)
    ts_pix_ij = ts_data[:,i,j]
    
    # find dates before EQ and corresponding data 
    bef_dates = datesn[np.where(dates_int<int(eq_date))]
    ts_bef = ts_pix_ij[np.where(dates_int<int(eq_date))[0]]

    # fit a line and find intercept at EQ date 





