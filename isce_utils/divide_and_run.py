"""divide the script to multiple scripts and run them
"""

import os 
import argparse 
import multiprocessing
from joblib import Parallel, delayed
import numpy as np

parser = argparse.ArgumentParser(description='divide the input script to multiple scripts and then run them')
parser.add_argument('-f', '--filename', type=str, metavar='', required=True, help='Input file name')
args = parser.parse_args()

# name of the file
filename = args.filename 

# Opening a file
file = open(filename,"r")
Counter = 0

# Reading from file
Content = file.read()
CoList = Content.split("\n")
for i in CoList:
    if i:
        Counter += 1
# Counter is the number of lines in the file 

# number of cores available 
num_cores = multiprocessing.cpu_count()

# number of files made 
if Counter > num_cores:
    num_files = num_cores 
else: 
    num_files = Counter


numfile_runs = np.zeros((num_files,1))
for i in range(num_files):
    if Counter > num_cores: 
        minval = np.int(np.floor(Counter/num_files))
        if np.mod(Counter, num_files) >= i+1: 
            valnow = minval + 1 
            numfile_runs[i] = valnow
        else:
            numfile_runs[i] = minval
    else:
        numfile_runs[i] = 1

fileidx = np.zeros((num_files,1))
for i in range(num_files):
    fileidx[i] = np.int(np.sum(numfile_runs[0:i+1]))

def run_file_divided(numcurrent, fileid_run, filename):
    '''
    function that divides the scripnumcurrent in python format 0,1,2,...
    '''
    a_file = open(filename, "r")
    linelist = a_file.readlines()
    if numcurrent == 0 :
        firstidx = 0 
    else:
        firstidx = np.int(fileid_run[numcurrent-1][0])
    lastidx = np.int(fileid_run[numcurrent][0])  
    copylines = linelist[firstidx:lastidx]
    filename_current = filename + '_num' + str(numcurrent)
    a_file.close()
    a_file = open(filename_current, "w")
    a_file.writelines(copylines)
    a_file.close()












