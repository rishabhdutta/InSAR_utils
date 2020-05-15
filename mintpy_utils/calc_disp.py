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
proj_dir = os.path.expanduser('/data/not_backed_up/rdtta/earthquakes/Utah2020/Sentinel/AT20/Stack/timeseries1')

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
eq_date_frac = SBI_Year(np.array([['20200318']])).flatten()

coseismic_disp = np.zeros((ifglen, ifgwid))
# find dates before EQ 
bef_dates = datesn[np.where(dates_int<int(eq_date))]
bef_dates_frac = SBI_Year(np.transpose(np.array([bef_dates])))
bef_dates_frac = bef_dates_frac.flatten()
# find dates after EQ
aft_dates = datesn[np.where(dates_int>int(eq_date))]
aft_dates_frac = SBI_Year(np.transpose(np.array([aft_dates])))
aft_dates_frac = aft_dates_frac.flatten()

def cos_slip(arg_j, arg_i):
    '''
    using multiprocessing and joblib for parallelization 
    '''
    # timeseries at pixel (i,j)
    ts_pix_ij = ts_data[:,arg_i,arg_j]
        
    if np.size(np.where(np.isnan(ts_pix_ij)==True)) == numdates :
        output = np.nan  
    else:
        # data before EQ 
        ts_bef = ts_pix_ij[np.where(dates_int<int(eq_date))[0]]

        # fit a line and find intercept at EQ date
        m, b = np.polyfit(bef_dates_frac, ts_bef, 1)
        c1 = m*eq_date_frac + b

        # data after EQ 
        ts_aft = ts_pix_ij[np.where(dates_int>int(eq_date))[0]]

        # fit a line and find intercept at EQ date
        m, b = np.polyfit(aft_dates_frac, ts_aft, 1)
        c2 = m*eq_date_frac +b

        output = c2 - c1 
    return output

num_cores = multiprocessing.cpu_count()
for i in range(ifglen):
    input = range(ifgwid)
    #num_cores = multiprocessing.cpu_count()
    #foo_ = partial(foo, arg2=arg2, arg3=arg3, arg4=arg4)
    cos_slip_ = partial(cos_slip, arg_i = i)
    output = Parallel(n_jobs=num_cores)(delayed(cos_slip_)(j) for j in input)
    coseismic_disp[i,:] = np.array(output)

#fig = plt.figure(figsize=(18, 16))
#ax = fig.add_subplot(111)
#im = ax.pcolormesh(longitude, latitude, coseismic_disp, cmap='jet')
#fig.colorbar(im, ax=ax)
#ax.set_title('AT20 coseismic disp.')
#fig.tight_layout()
#plt.savefig('AT20_coseismic_timeseries.png')

# save to .mat file for plotting
varname1 = 'coseismic_disp.mat'
sio.savemat(varname1, {'coseismic_disp':coseismic_disp, 'dem':height, \
        'lon':longitude, 'lat':latitude})

