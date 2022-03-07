#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 17:12:36 2021

@author: duttar

Edited from David Bekaert
"""
from shutil import copyfile
from osgeo import gdal            ## GDAL support for reading virtual files
import os                         ## To create and remove directories
import matplotlib.pyplot as plt   ## For plotting
import numpy as np                ## Matrix calculations
import glob                       ## Retrieving list of files
import argparse 


parser = argparse.ArgumentParser(description='Utility to plot multiple simple complex arrays')
parser.add_argument('-f', '--GDALfilename_wildcard', type=str, metavar='', required=True, help='Input file name')
parser.add_argument('-o', '--outfilename', type=str, metavar='', required=True, help='Output file name')
#parser.add_argument('-b', '--band', type=int, metavar='', required=True, help='Band number')
parser.add_argument('-t', '--title', type=str, metavar='', required=False, help='Input title')
#parser.add_argument('-c', '--colormap', type=str, metavar='', required=True, help='Input colormap')
parser.add_argument('-a', '--aspect', type=str, metavar='', required=False, help='Input aspect')
parser.add_argument('-dmin', '--datamin', type=float, metavar='', required=False, help='Input minimum data value')
parser.add_argument('-dmax', '--datamax', type=float, metavar='', required=False, help='Input maximum data value')
parser.add_argument('-i', '--interpolation', type=str, metavar='', required=False, help='interpolation technique')

args = parser.parse_args()

# name of the file
GDALfile = args.GDALfilename_wildcard
outfile = args.outfilename
#band = args.band
titl = args.title
#colormap = args.colormap
apect = args.aspect
dmin = args.datamin
dmax = args.datamax
interp = args.interpolation


def plotstackcomplexdata(GDALfilename_wildcard, outfilename,
                         title=None, aspect=1,
                         datamin=None, datamax=None,
                         interpolation='nearest',
                         draw_colorbar=True, colorbar_orientation="horizontal"):
    # get a list of all files matching the filename wildcard criteria
    GDALfilenames = glob.glob(GDALfilename_wildcard)
    print(GDALfilenames)
    # initialize empty numpy array
    data = None
    for GDALfilename in GDALfilenames:
        ds = gdal.Open(GDALfilename, gdal.GA_ReadOnly)
        data_temp = ds.GetRasterBand(1).ReadAsArray()
        ds = None
        
        if data is None:
            data = data_temp
        else:
            data = np.vstack((data,data_temp))

    # put all zero values to nan and do not plot nan
    try:
        data[data==0]=np.nan
    except:
        pass              
            
    fig = plt.figure(figsize=(18, 16))
    ax = fig.add_subplot(1,2,1)
    cax1=ax.imshow(np.abs(data), vmin=datamin, vmax=datamax,
                   cmap='gray', interpolation='nearest')
    ax.set_title(title + " (amplitude)")
    if draw_colorbar is not None:
        cbar1 = fig.colorbar(cax1,orientation=colorbar_orientation)
    ax.set_aspect(aspect)

    ax = fig.add_subplot(1,2,2)
    cax2 =ax.imshow(np.angle(data), cmap='rainbow',
                            interpolation='nearest')
    ax.set_title(title + " (phase [rad])")
    if draw_colorbar is not None:
        cbar2 = fig.colorbar(cax2,orientation=colorbar_orientation)
    ax.set_aspect(aspect)
    #plt.show() 
    plt.savefig(outfilename)
    
    # clearing the data
    data = None
    
if titl is None: 
    titl = None
    
    
if apect is None: 
    apect = 1
    
if dmin is None: 
    dmin = None 
    
if dmax is None: 
    dmax = None
    
if interp is None: 
    interp = 'nearest'
    
plotstackcomplexdata(GDALfile, outfile,titl, apect,dmin, dmax, interp)
                        