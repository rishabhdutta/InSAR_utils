#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 26 11:00:12 2020

@author: duttar
"""

import os 
#import numpy as np

conf_dir = '/data/not_backed_up/rdtta/Permafrost/Alaska/North_slope/DT102/Stack/configs'
copyfile = '/data/not_backed_up/rdtta/Permafrost/Alaska/North_slope/DT102/Stack/configs/config_igram_20200407_20200513'
pres_dir = '/data/not_backed_up/rdtta/Permafrost/Alaska/North_slope/DT102/Stack/run_files'

sys_comm1 = 'cp '+copyfile + ' '+ pres_dir + '/.'
os.system(sys_comm1)

mas_input = 20200715
sla_input = 20200730

mas_input = str(mas_input)
sla_input = str(sla_input)

sys_comm2 = 'mv '+ pres_dir + '/config_igram_20200407_20200513 '+ \
    pres_dir+'/config_igram_'+mas_input+'_'+sla_input
os.system(sys_comm2)

stack_dir = '/data/not_backed_up/rdtta/Permafrost/Alaska/North_slope/DT102/Stack'

filename= pres_dir+'/config_igram_'+mas_input+'_'+sla_input
a_file = open(filename, "r")
list_of_lines = a_file.readlines()
list_of_lines[5] = 'master : '+stack_dir + '/coreg_slaves/'+mas_input+'\n'
list_of_lines[6] = 'slave : '+stack_dir + '/coreg_slaves/'+sla_input+'\n'
list_of_lines[7] = 'interferogram : '+stack_dir + '/interferograms/'+ \
    mas_input+'_'+sla_input+'\n'
list_of_lines[16] = 'inp_master : '+stack_dir + '/interferograms/' + \
    mas_input+'_'+sla_input+'\n'
list_of_lines[17] = 'dirname : '+stack_dir + '/interferograms/' + \
    mas_input+'_'+sla_input+'\n'
list_of_lines[19] = 'outfile : '+stack_dir + '/merged/interferograms/' + \
    mas_input+'_'+sla_input + '/fine.int'+'\n'

a_file = open(filename, "w")
a_file.writelines(list_of_lines)
a_file.close()    
    
