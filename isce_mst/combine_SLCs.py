#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 16:07:12 2022
@author: duttar
"""

import os 
#import numpy as np
import argparse

parser = argparse.ArgumentParser(description='goes to SLC folder in merged and creates .slc.full files from .slc.full.vrt files')
parser.add_argument('-p', '--path', type=str, metavar='', required=True, help='enter path to merged folder')

args = parser.parse_args()

merged_dir = str(args.path)
sys_comm1 = 'cd ' + merged_dir + ' && mkdir trash'
os.system(sys_comm1)




