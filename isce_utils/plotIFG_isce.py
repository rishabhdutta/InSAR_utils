#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 11:19:54 2020

@author: duttar
use this script to plot complex, non-complex and stack images produced by ISCE2
Script plot_stack.py uses this

Edited from David Bekaert
"""

from shutil import copyfile
from osgeo import gdal            ## GDAL support for reading virtual files
import os                         ## To create and remove directories
import matplotlib.pyplot as plt   ## For plotting
import numpy as np                ## Matrix calculations
import glob                       ## Retrieving list of files


def plotdata(GDALfilename,band=1,title=None,colormap='gray',aspect=1, datamin=None, datamax=None,draw_colorbar=True,colorbar_orientation="horizontal",background=None):
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
    plt.savefig('plotdata.png')
    
    # clearing the data
    data = None
    
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
    
def plotstackdata(GDALfilename_wildcard,band=1,title=None,colormap='gray',aspect=1, datamin=None, datamax=None,draw_colorbar=True,colorbar_orientation="horizontal"):
    # get a list of all files matching the filename wildcard criteria
    GDALfilenames = glob.glob(os.path.abspath(GDALfilename_wildcard))
    
    # initialize empty numpy array
    for GDALfilename in GDALfilenames:
        ds = gdal.Open(GDALfilename, gdal.GA_ReadOnly)
        data_temp = ds.GetRasterBand(band).ReadAsArray()   
        ds = None
        
        try:
            data
        except NameError:
            data = data_temp
        else:
            data = np.vstack((data,data_temp))

    # put all zero values to nan and do not plot nan
    try:
        data[data==0]=np.nan
    except:
        pass            
            
    fig = plt.figure(figsize=(18, 16))
    ax = fig.add_subplot(111)
    cax = ax.imshow(data, vmin = datamin, vmax=datamax, cmap=colormap)
    ax.set_title(title)
    if draw_colorbar is not None:
        cbar = fig.colorbar(cax,orientation=colorbar_orientation)
    ax.set_aspect(aspect)    
    # plt.show() 
    plt.savefig('plotstackdata.png')
    
    # clearing the data
    data = None
    
def plotstackcomplexdata(GDALfilename_wildcard,title=None,aspect=1, datamin=None, datamax=None,draw_colorbar=True,colorbar_orientation="horizontal"):
    # get a list of all files matching the filename wildcard criteria
    GDALfilenames = glob.glob(os.path.abspath(GDALfilename_wildcard))
    
    # initialize empty numpy array
    for GDALfilename in GDALfilenames:
        ds = gdal.Open(GDALfilename, gdal.GA_ReadOnly)
        data_temp = ds.GetRasterBand(1).ReadAsArray()
        ds = None
        
        try:
            data
        except NameError:
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
    cax1=ax.imshow(np.abs(data),vmin = datamin, vmax=datamax, cmap='gray')
    ax.set_title(title + " (amplitude)")
    if draw_colorbar is not None:
        cbar1 = fig.colorbar(cax1,orientation=colorbar_orientation)
    ax.set_aspect(aspect)

    ax = fig.add_subplot(1,2,2)
    cax2 =ax.imshow(np.angle(data),cmap='rainbow')
    ax.set_title(title + " (phase [rad])")
    if draw_colorbar is not None:
        cbar2 = fig.colorbar(cax2,orientation=colorbar_orientation)
    ax.set_aspect(aspect)
    # plt.show() 
    plt.savefig('plotstackcomplexdata.png')
    
    # clearing the data
    data = None
