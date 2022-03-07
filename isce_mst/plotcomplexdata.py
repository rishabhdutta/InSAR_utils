#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 16:45:27 2021

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


parser = argparse.ArgumentParser(description='Utility to plot interferograms')
parser.add_argument('-f', '--GDALfilename', type=str, metavar='', required=True, help='Input file name')
parser.add_argument('-o', '--outfilename', type=str, metavar='', required=True, help='Output file name')
#parser.add_argument('-b', '--band', type=int, metavar='', required=True, help='Band number')
parser.add_argument('-t', '--title', type=str, metavar='', required=False, help='Input title')
parser.add_argument('-c', '--colormap', type=str, metavar='', required=False, help='Input colormap')
parser.add_argument('-a', '--aspect', type=str, metavar='', required=False, help='Input aspect')
parser.add_argument('-dmin', '--datamin', type=float, metavar='', required=False, help='Input minimum data value')
parser.add_argument('-dmax', '--datamax', type=float, metavar='', required=False, help='Input maximum data value')

args = parser.parse_args()

# name of the file
GDALfile = args.GDALfilename
outfile = args.outfilename
#bandval = args.band
titl = args.title
cmap = args.colormap
apect = args.aspect
dmin = args.datamin
dmax = args.datamax

def plotcomplexdata(GDALfilename, outfilename,title=None,aspect=1,datamin=None, datamax=None,draw_colorbar=None,colorbar_orientation="horizontal"):
    ds = gdal.Open(GDALfilename, gdal.GA_ReadOnly)
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

    
    fig = plt.figure(figsize=(18, 16))
    ax = fig.add_subplot(1,2,1)
    cax1=ax.imshow(np.abs(slc),vmin = datamin, vmax=datamax, cmap='gray',extent=[xmin,xmax,ymin,ymax])
    ax.set_title(title + " (amplitude)")
    if draw_colorbar is not None:
        cbar1 = fig.colorbar(cax1,orientation=colorbar_orientation)
    ax.set_aspect(aspect)

    ax = fig.add_subplot(1,2,2)
    cax2 =ax.imshow(np.angle(slc),cmap='rainbow',extent=[xmin,xmax,ymin,ymax])
    ax.set_title(title + " (phase [rad])")
    if draw_colorbar is not None:
        cbar2 = fig.colorbar(cax2,orientation=colorbar_orientation)
    ax.set_aspect(aspect)
    # plt.show()
    plt.savefig(outfilename)
    
    # clearing the data
    slc = None
    
      
if titl is None: 
    titl = None
    
if cmap is None:
    cmap = 'gray'
    
if apect is None: 
    apect = 1
    
if dmin is None: 
    dmin = None 
    
if dmax is None: 
    dmax = None
    
plotcomplexdata(GDALfile,outfile,titl,apect,dmin, dmax)
