#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 11:19:54 2020

@author: duttar

Plots all the results of ISCE filterred wrapped interfrograms from Sentinel stack
processing. 
output - stack1.pdf ... in figures folder
Edit it according to number of IFGs

Also plots single unfiltered wrapped ifgs to the figures folder 
"""

from shutil import copyfile
from osgeo import gdal            ## GDAL support for reading virtual files
import os                         ## To create and remove directories
import matplotlib.pyplot as plt   ## For plotting
import numpy as np                ## Matrix calculations
import glob                       ## Retrieving list of files


fig, axs = plt.subplots(7, 6, sharex='col', sharey='row',
                        gridspec_kw={ 'wspace': 0})
f = open("all_igrams.txt")
lines_variable = f.readlines()
print(lines_variable[0])
i = 1
for ax in axs.flat:
    #ax.plot(x, y**2, 'tab:orange')
    line_var = lines_variable[i-1]
    filename = 'interferograms/' + line_var[0:17] + '/filt_fine.int.vrt'
    
    ds = gdal.Open(filename, gdal.GA_ReadOnly)
    slc = ds.GetRasterBand(1).ReadAsArray()
    transform = ds.GetGeoTransform()
    ds = None
    
    # getting the min max of the axes
    firstx = transform[0]
    firsty = transform[3]
    deltay = transform[5]
    deltax = transform[1]
    lastx = firstx+slc.shape[1]*deltax
    lasty = firsty+slc.shape[0]*deltay
    ymin = np.min([lasty,firsty])
    ymax = np.max([lasty,firsty])
    xmin = np.min([lastx,firstx])
    xmax = np.max([lastx,firstx])

    # put all zero values to nan and do not plot nan
    try:
        slc[slc==0]=np.nan
    except:
        pass
    
    ax.imshow(np.angle(slc),cmap='rainbow',extent=[xmin,xmax,ymin,ymax])
    ax.text(.6,.92, line_var[0:17], fontsize=3)
    ax.get_yaxis().set_ticks([])
    ax.get_xaxis().set_ticks([])
    ax.axis('off')
    i = i + 1
    ax.label_outer()
       
plt.savefig('figures/stack1.pdf')


#fig, axs = plt.subplots(3, 6, sharex='col', sharey='row',
#                        gridspec_kw={ 'wspace': 0})
#f = open("all_igrams.txt")
#lines_variable = f.readlines()
#print(lines_variable[0])
#i = 61
#for ax in axs.flat:
    #ax.plot(x, y**2, 'tab:orange')
#    line_var = lines_variable[i-1]
#    filename = 'interferograms/' + line_var[0:17] + '/filt_fine.int.vrt'

#    ds = gdal.Open(filename, gdal.GA_ReadOnly)
#    slc = ds.GetRasterBand(1).ReadAsArray()
#    transform = ds.GetGeoTransform()
#    ds = None

    # getting the min max of the axes
#    firstx = transform[0]
#    firsty = transform[3]
#    deltay = transform[5]
#    deltax = transform[1]
#    lastx = firstx+slc.shape[1]*deltax
#    lasty = firsty+slc.shape[0]*deltay
#    ymin = np.min([lasty,firsty])
#    ymax = np.max([lasty,firsty])
#    xmin = np.min([lastx,firstx])
#    xmax = np.max([lastx,firstx])

    # put all zero values to nan and do not plot nan
#    try:
#        slc[slc==0]=np.nan
#    except:
#        pass

#    ax.imshow(np.angle(slc),cmap='rainbow',extent=[xmin,xmax,ymin,ymax])
#    ax.text(.6,.92, line_var[0:17], fontsize=3)
#    ax.get_yaxis().set_ticks([])
#    ax.get_xaxis().set_ticks([])
#    ax.axis('off')
#    i = i + 1
#    ax.label_outer()

#plt.savefig('figures/stack2.pdf')


from plotIFG_isce import plotcomplexdata
f = open("all_igrams.txt", "r")
for x in f:
    filename = 'interferograms/' + x[0:17] + '/fine.int.vrt'
    outfile = 'figures/' + x[0:17] + '.png'
    plotcomplexdata(filename, outfile, title="MERGED IFG ",aspect=3,datamin=0, datamax=10000,draw_colorbar=True)


