## Read/plot displacement time-series of one pixel from timeseries HDF5 file
"""
created by Rishabh Dutta 
addpath this directory and then 
from plot_ts_pixelwise import pixel_ts

plots the timeseries of each pixel from geocoded mintpy results (geo_timeseries.h5)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from mintpy.utils import utils as ut, plot as pp
from mintpy.defaults.plot import *

# work directory
proj_dir = os.path.expanduser('/data/not_backed_up/rdtta/earthquakes/Utah2020/Sentinel/DT100/Stack/timeseries1')

# file in geo coordinates
geom_file = None
ts_file = os.path.join(proj_dir, 'geo/geo_timeseries_ramp_demErr.h5')

def pixel_ts(lat, lon, font_size, fig_dpi):
    '''
    format : pixel_ts(lat, lon, font_size, fig_dpi)
    plots the time-series at a pixel
    '''
    dates, dis = ut.read_timeseries_lalo(lat, lon, ts_file=ts_file, lookup_file=geom_file)
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=[6, 3])
    ax.scatter(dates, dis, marker='^', s=6**2, facecolors='none', edgecolors='k', linewidth=1.)

    # axis format
    pp.auto_adjust_xaxis_date(ax, dates, fontsize=font_size)
    ax.tick_params(which='both', direction='in', labelsize=font_size, bottom=True, top=True, left=True, right=True)
    ax.set_xlabel('Time [yr]', fontsize=font_size)
    ax.set_ylabel('LOS displacement [m]', fontsize=font_size)

    # output
    out_file = proj_dir+ '/pic/lat' + str(lat) + 'lon' + str(lon) + '.png'
    plt.savefig(out_file, bbox_inches='tight', dpi=fig_dpi)

    print('save to file: '+out_file)


