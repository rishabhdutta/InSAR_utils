"""
plot the interferogram for input master and slave
"""
import os
import argparse

parser = argparse.ArgumentParser(description='plot the interferogram for input master and slave')
parser.add_argument('-m', '--master', type=int, metavar='', required=True, help='Master date')
parser.add_argument('-s', '--slave', type=int, metavar='', required=True, help='Slave date')
args = parser.parse_args()

mas_input = args.master
sla_input = args.slave

mas_input = str(mas_input)
sla_input = str(sla_input)

sys_comm1 = 'echo '+mas_input+ '_'+sla_input+' > singleifg.txt'
os.system(sys_comm1)

from plotIFG_isce import plotcomplexdata
f = open("singleifg.txt", "r")
for x in f:
    filename = 'interferograms/' + x[0:17] + '/fine.int.vrt'
    outfile = 'figures/' + x[0:17] + '.png'
    plotcomplexdata(filename, outfile, title="MERGED IFG ",aspect=3,datamin=0, datamax=10000,draw_colorbar=True)
