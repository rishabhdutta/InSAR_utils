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

trash_dir = merged_dir + '/trash'
SLC_dir = merged_dir + '/SLC'
filename = trash_dir + '/dates.txt'

# get list of dates in SLC and put that in trash folder
sys_comm2 = 'ls ' + SLC_dir + ' > ' + filename
os.system(sys_comm2)

# read the file dates.txt
file = open(filename,"r")

Counter = 0
# Reading from file
Content = file.read()
CoList = Content.split("\n")
for i in CoList:
    if i:
        Counter += 1
# Counter is the number of lines in the file 
file.close()

file = open(filename,"r")
Lines = file.readlines()
count = 0
# Strips the newline character
for line in Lines:
    count += 1
    print("Moving SLC {}".format(line.strip()))
    sys_comm3 = 'gdal_translate -of ENVI '+ line.strip() + '.slc.full.vrt ' + line.strip() + '.slc.full'
    print(sys_comm3)

file.close()


