#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 14:15:22 2021

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


parser = argparse.ArgumentParser(description='utility to plot a 2D array')
parser.add_argument('-f', '--GDALfilename', type=str, metavar='', required=True, help='Input file name')
parser.add_argument('-o', '--outfilename', type=str, metavar='', required=True, help='Output file name')
parser.add_argument('-b', '--band', type=int, metavar='', required=False, help='Band number')
parser.add_argument('-t', '--title', type=str, metavar='', required=False, help='Input title')
parser.add_argument('-c', '--colormap', type=str, metavar='', required=False, help='Input colormap')
parser.add_argument('-a', '--aspect', type=str, metavar='', required=False, help='Input aspect')
parser.add_argument('-dmin', '--datamin', type=float, metavar='', required=False, help='Input minimum data value')
parser.add_argument('-dmax', '--datamax', type=float, metavar='', required=False, help='Input maximum data value')
parser.add_argument('-bgnd', '--background', type=str, metavar='', required=False, help='background needed?')


args = parser.parse_args()

# name of the file
GDALfile = args.GDALfilename
outfile = args.outfilename
bandval = args.band
titl = args.title
cmap = args.colormap
apect = args.aspect
dmin = args.datamin
dmax = args.datamax
bgnd = args.background

def plotdata(GDALfilename,outfilename,band=1,title=None,colormap='gray',aspect=1, datamin=None, datamax=None, background=None, draw_colorbar=True,colorbar_orientation="horizontal"):
    ds = gdal.Open(GDALfilename, gdal.GA_ReadOnly)
    data = ds.GetRasterBand(band).ReadAsArray()
    transform = ds.GetGeoTransform()
    ds = None
    
    # getting the min max of the axes
    firstx = transform[0]
    firsty = transform[3]
    deltay = transform[5]
    deltax = transform[1]
    lastx = firstx+data.shape[1]*deltax
    lasty = firsty+data.shape[0]*deltay
    ymin = np.min([lasty,firsty])
    ymax = np.max([lasty,firsty])
    xmin = np.min([lastx,firstx])
    xmax = np.max([lastx,firstx])

    # put all zero values to nan and do not plot nan
    if background is None:
        try:
            data[data==0]=np.nan
        except:
            pass
    
    fig = plt.figure(figsize=(18, 16))
    ax = fig.add_subplot(111)
    cax = ax.imshow(data, vmin = datamin, vmax=datamax, cmap=colormap,extent=[xmin,xmax,ymin,ymax])
    ax.set_title(title)
    if draw_colorbar is not None:
        cbar = fig.colorbar(cax,orientation=colorbar_orientation)
    ax.set_aspect(aspect)    
    # plt.show()
    plt.savefig(outfilename)
    
    # clearing the data
    data = None

if bandval is None:
    bandval = 1
    
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

if bgnd is None: 
    bgnd = None
    
plotdata(GDALfile,outfile,bandval,titl,cmap,apect, dmin, dmax, bgnd)

