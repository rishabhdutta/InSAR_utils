#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 09:58:50 2020

@author: duttar
Description: Solving the problem A = Bx 
A is the timeseries stack of InSAR pixel wise 
B is matrix including time and ADDT 
x is a vector containing seasonal and overall subsidence 

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




