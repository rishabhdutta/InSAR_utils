#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 20:36:20 2020

@author: duttar

Description : Reads the daily temperature data from DS633 catalog 
Calculates the Accumulated Degree Days of Thawing from the temperature data
"""

import numpy as np
from netCDF4 import Dataset  # http://code.google.com/p/netcdf4-python/
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import scipy.io as sio

# 
# Opening a file 
file = open("allind.txt","r") 
Counter = 0
  
# Reading from file 
Content = file.read() 
CoList = Content.split("\n") 
  
for i in CoList: 
    if i: 
        Counter += 1
file.close()

# read the monthly file
for i in range(Counter):
    f = open("allind.txt")
    lines_variable = f.readlines()
    line_var = lines_variable[i]
    nc_file = line_var[0:-1]
    f.close()
    
    fh = Dataset(nc_file, mode='r')
    VAR_2T = fh.variables['VAR_2T'][:]
    VAR_2T = np.array(VAR_2T)
    VAR_2T_domain = VAR_2T[:,4:12,57:88]
    
    longitude1 = fh.variables['longitude'][:]
    longitude1 = np.array(longitude1)
    lons = longitude1[57:88]     # selected longitude
    
    latitude1 = fh.variables['latitude'][:]
    latitude1 = np.array(latitude1)
    lats = latitude1[4:12]       # selected latitude
    
    fh.close()
    
    
    # calculate the daily average temperature
    numdays = np.int(VAR_2T.shape[0]/24)
    
    var_2T_avgday = np.zeros((numdays, 8, 31))
    for latind in range(lats.shape[0]):
        for lonind in range(lons.shape[0]):
            varval = VAR_2T_domain[:,latind,lonind]
            avg_2T = np.zeros((numdays,1))
            for j in range(numdays):
                ind = j*24 + np.arange(0,24, dtype=int)
                avgday = (np.max(varval[ind]) + np.min(varval[ind]))/2 
                avg_2T[j] = avgday
                
            var_2T_avgday[:, latind, lonind] = avg_2T.flatten(order='F') 
            
    var_name = line_var[48:69] + '.mat'
    # save the file in matlab format 
    sio.savemat(var_name, {'var_2T_avgday':var_2T_avgday, 'latitude':lats, 'longitude':lons})
    print_var = 'saved the matlab file: ' + var_name + '\n'
    print(print_var)

##############################################################################       
# plot the addt for the year 2016 
    
lon, lat = np.meshgrid(lons, lats)
locnum = lon.shape[0]*lon.shape[1]

locall = np.concatenate((lon.reshape(locnum,1, order = 'F'), lat.reshape(locnum,1, order = 'F')), axis=1)

temp2016 = np.zeros((locnum, 366))
prevdays = 0

f = open("2016.txt")
lines_variable = f.readlines()
for i in range(12):
    line_var = lines_variable[i]
    matfile = line_var[0:-1]
    mat_c1 = sio.loadmat(matfile)
    var_2Tmat = mat_c1['var_2T_avgday']
    lonmat = mat_c1['longitude']
    latmat = mat_c1['latitude']
    
    numdays = var_2Tmat.shape[0]
    ind_days = prevdays + np.arange(numdays)
    for j in range(locnum):
        lon_pr = locall[j,0]
        lat_pr = locall[j,1]
        
        indlon = np.where(lonmat == lon_pr)
        indlat = np.where(latmat == lat_pr)   
        indlon1 = indlon[1]
        indlat1 = indlat[1]
        
        temp2016[j, ind_days] = var_2Tmat[:, indlat1, indlon1].flatten(order='F')
        
    prevdays = prevdays + numdays

var_name = 'temp2016.mat'
sio.savemat(var_name, {'temp2016':temp2016})
f.close()
        
# calculate ADDT (accumulated degree days of thawing)

details_addt = np.zeros((locnum, 3)) # contains detail of addt 
# first column is number of days over 273.15 
# second column - first day of above 273.15
# third column - last day of above 273.15
addt2016 = np.zeros((locnum, 365))

for i in range(locnum): 
    temp_i = temp2016[i, :] 
    ind_mtzero = np.where(temp_i > 273.15)
    ind_mtzero = np.array(ind_mtzero)
    first_day = ind_mtzero[0][0] + 1
    last_day = ind_mtzero[0][-1] + 1
    num_zeroday = last_day - first_day
    addt_prev = 0
    for days in range(num_zeroday):
        if temp2016[i, first_day -1 + days] > 273.15:
            addt_day = temp2016[i, first_day-1+days] - 273.15
        else:
            addt_day = 0 
            
        addt2016[i, days] = addt_prev + addt_day
        addt_prev = addt_prev + addt_day
        
    details_addt[i, 0] = num_zeroday
    details_addt[i, 1] = first_day
    details_addt[i, 2] = last_day
    print(i)
    
var_name = 'addt2016.mat'
sio.savemat(var_name, {'addt2016':addt2016, 'details_addt':details_addt, \
                       'lonlat':locall})             
    
##############################################################################  
# plot the addt for the year 2017 
    
lon, lat = np.meshgrid(lons, lats)
locnum = lon.shape[0]*lon.shape[1]

locall = np.concatenate((lon.reshape(locnum,1, order = 'F'), lat.reshape(locnum,1, order = 'F')), axis=1)

temp2017 = np.zeros((locnum, 365))
prevdays = 0

f = open("2017.txt")
lines_variable = f.readlines()
for i in range(12):
    line_var = lines_variable[i]
    matfile = line_var[0:-1]
    print(matfile)
    mat_c1 = sio.loadmat(matfile)
    var_2Tmat = mat_c1['var_2T_avgday']
    lonmat = mat_c1['longitude']
    latmat = mat_c1['latitude']
    
    numdays = var_2Tmat.shape[0]
    ind_days = prevdays + np.arange(numdays)
    for j in range(locnum):
        lon_pr = locall[j,0]
        lat_pr = locall[j,1]
        
        indlon = np.where(lonmat == lon_pr)
        indlat = np.where(latmat == lat_pr)   
        indlon1 = indlon[1]
        indlat1 = indlat[1]
        
        temp2017[j, ind_days] = var_2Tmat[:, indlat1, indlon1].flatten(order='F')
        
    prevdays = prevdays + numdays

var_name = 'temp2017.mat'
sio.savemat(var_name, {'temp2017':temp2017})
f.close()

# calculate ADDT (accumulated degree days of thawing)

details_addt = np.zeros((locnum, 3)) # contains detail of addt 
# first column is number of days over 273.15 
# second column - first day of above 273.15
# third column - last day of above 273.15
addt2017 = np.zeros((locnum, 365))

for i in range(locnum): 
    temp_i = temp2017[i, :] 
    ind_mtzero = np.where(temp_i > 273.15)
    ind_mtzero = np.array(ind_mtzero)
    first_day = ind_mtzero[0][0] + 1
    last_day = ind_mtzero[0][-1] + 1
    num_zeroday = last_day - first_day
    addt_prev = 0
    for days in range(num_zeroday):
        if temp2017[i, first_day -1 + days] > 273.15:
            addt_day = temp2017[i, first_day-1+days] - 273.15
        else:
            addt_day = 0 
            
        addt2017[i, days] = addt_prev + addt_day
        addt_prev = addt_prev + addt_day
        
    details_addt[i, 0] = num_zeroday
    details_addt[i, 1] = first_day
    details_addt[i, 2] = last_day
    print(i)
    
var_name = 'addt2017.mat'
sio.savemat(var_name, {'addt2017':addt2017, 'details_addt':details_addt, \
                       'lonlat':locall})           
   
##############################################################################      
# plot the addt for the year 2018 
    
lon, lat = np.meshgrid(lons, lats)
locnum = lon.shape[0]*lon.shape[1]

locall = np.concatenate((lon.reshape(locnum,1, order = 'F'), lat.reshape(locnum,1, order = 'F')), axis=1)

temp2018 = np.zeros((locnum, 365))
prevdays = 0

f = open("2018.txt")
lines_variable = f.readlines()
for i in range(12):
    line_var = lines_variable[i]
    matfile = line_var[0:-1]
    print(matfile)
    mat_c1 = sio.loadmat(matfile)
    var_2Tmat = mat_c1['var_2T_avgday']
    lonmat = mat_c1['longitude']
    latmat = mat_c1['latitude']
    
    numdays = var_2Tmat.shape[0]
    ind_days = prevdays + np.arange(numdays)
    for j in range(locnum):
        lon_pr = locall[j,0]
        lat_pr = locall[j,1]
        
        indlon = np.where(lonmat == lon_pr)
        indlat = np.where(latmat == lat_pr)   
        indlon1 = indlon[1]
        indlat1 = indlat[1]
        
        temp2018[j, ind_days] = var_2Tmat[:, indlat1, indlon1].flatten(order='F')
        
    prevdays = prevdays + numdays

var_name = 'temp2018.mat'
sio.savemat(var_name, {'temp2018':temp2018})
f.close()

# calculate ADDT (accumulated degree days of thawing)

details_addt = np.zeros((locnum, 3)) # contains detail of addt 
# first column is number of days over 273.15 
# second column - first day of above 273.15
# third column - last day of above 273.15
addt2018 = np.zeros((locnum, 365))

for i in range(locnum): 
    temp_i = temp2018[i, :] 
    ind_mtzero = np.where(temp_i > 273.15)
    ind_mtzero = np.array(ind_mtzero)
    first_day = ind_mtzero[0][0] + 1
    last_day = ind_mtzero[0][-1] + 1
    num_zeroday = last_day - first_day
    addt_prev = 0
    for days in range(num_zeroday):
        if temp2018[i, first_day -1 + days] > 273.15:
            addt_day = temp2018[i, first_day-1+days] - 273.15
        else:
            addt_day = 0 
            
        addt2018[i, days] = addt_prev + addt_day
        addt_prev = addt_prev + addt_day
        
    details_addt[i, 0] = num_zeroday
    details_addt[i, 1] = first_day
    details_addt[i, 2] = last_day
    print(i)
    
var_name = 'addt2018.mat'
sio.savemat(var_name, {'addt2018':addt2018, 'details_addt':details_addt, \
                       'lonlat':locall})  
    
##############################################################################      
# plot the addt for the year 2019 

lon, lat = np.meshgrid(lons, lats)
locnum = lon.shape[0]*lon.shape[1]

locall = np.concatenate((lon.reshape(locnum,1, order = 'F'), lat.reshape(locnum,1, order = 'F')), axis=1)

temp2019 = np.zeros((locnum, 365))
prevdays = 0

f = open("2019.txt")
lines_variable = f.readlines()
for i in range(12):
    line_var = lines_variable[i]
    matfile = line_var[0:-1]
    print(matfile)
    mat_c1 = sio.loadmat(matfile)
    var_2Tmat = mat_c1['var_2T_avgday']
    lonmat = mat_c1['longitude']
    latmat = mat_c1['latitude']
    
    numdays = var_2Tmat.shape[0]
    ind_days = prevdays + np.arange(numdays)
    for j in range(locnum):
        lon_pr = locall[j,0]
        lat_pr = locall[j,1]
        
        indlon = np.where(lonmat == lon_pr)
        indlat = np.where(latmat == lat_pr)   
        indlon1 = indlon[1]
        indlat1 = indlat[1]
        
        temp2019[j, ind_days] = var_2Tmat[:, indlat1, indlon1].flatten(order='F')
        
    prevdays = prevdays + numdays

var_name = 'temp2019.mat'
sio.savemat(var_name, {'temp2019':temp2019})
f.close()

# calculate ADDT (accumulated degree days of thawing)

details_addt = np.zeros((locnum, 3)) # contains detail of addt 
# first column is number of days over 273.15 
# second column - first day of above 273.15
# third column - last day of above 273.15
addt2019 = np.zeros((locnum, 365))

for i in range(locnum): 
    temp_i = temp2019[i, :] 
    ind_mtzero = np.where(temp_i > 273.15)
    ind_mtzero = np.array(ind_mtzero)
    first_day = ind_mtzero[0][0] + 1
    last_day = ind_mtzero[0][-1] + 1
    num_zeroday = last_day - first_day
    addt_prev = 0
    for days in range(num_zeroday):
        if temp2019[i, first_day -1 + days] > 273.15:
            addt_day = temp2019[i, first_day-1+days] - 273.15
        else:
            addt_day = 0 
            
        addt2019[i, days] = addt_prev + addt_day
        addt_prev = addt_prev + addt_day
        
    details_addt[i, 0] = num_zeroday
    details_addt[i, 1] = first_day
    details_addt[i, 2] = last_day
    print(i)
    
var_name = 'addt2019.mat'
sio.savemat(var_name, {'addt2019':addt2019, 'details_addt':details_addt, \
                       'lonlat':locall})  
    

