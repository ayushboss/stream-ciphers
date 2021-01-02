import math
import pandas as pd
from gamma_functions import *
import argparse

parser = argparse.ArgumentParser(description='Provide file locations.')
parser.add_argument('-R','--readfile', type=str,
                    help='file to read from')
parser.add_argument('-O','--outfile',type=str,
                    help='file to save to')

args = parser.parse_args()

readfile=args.readfile

data = pd.read_csv(readfile)


n=1029000

# Monobit
data['Frequency Within Blocks'] = [gammaincc((99/2.0),float(s)/2.0) for s in data['Frequency Within Blocks'] ]

excess = [s*(n**0.5) for s in data['Monobit']]
vs = [(n-x)/2 for x in excess]

# print(vs)
# for i in range(10):
# 	print(' ')
# print(excess)

prop = []
for i in range(len(excess)):
	prop.append((excess[i]+vs[i])/n)
data['Runs']= [math.erfc(abs(data['Runs'].iloc[i] - (2.0*n*prop[i]*(1.0-prop[i])))/(2.0*math.sqrt(2.0*n)*prop[i]*(1-prop[i]))) for i in range(len(data['Runs']))]
data['Monobit'] = [math.erfc(float(s)/math.sqrt(2.0)) for s in data['Monobit']]
data['Longest Run in Ones'] = [gammaincc(6/2.0, s/2.0) for s in data['Longest Run in Ones']]
data['Binary Matrix Rank'] = [math.e **(-s/2.0) for s in data['Binary Matrix Rank']]
data['Nonoverlapping Template'] = [gammaincc(8/2.0, s/2.0) for s in data['Nonoverlapping Template']]
data['Overlapping Template'] = [gammaincc(5.0/2.0, s/2.0) for s in data['Overlapping Template']]
L=7
ev_table =  [0,0.73264948,1.5374383,2.40160681,3.31122472,
             4.25342659,5.2177052,6.1962507,7.1836656,
             8.1764248,9.1723243,10.170032,11.168765,
             12.168070,13.167693,14.167488,15.167379]
var_table = [0,0.690,1.338,1.901,2.358,2.705,2.954,3.125,
             3.238,3.311,3.356,3.384,3.401,3.410,3.416,
             3.419,3.421]
mag = [abs((fn - ev_table[L])/((math.sqrt(var_table[L]))*math.sqrt(2))) for fn in data['Maurer\'s Universal']]
data['Maurer\'s Universal'] = [math.erfc(s) for s in mag]
data['Linear Complexity'] = [gammaincc((6/2.0),(s/2.0)) for s in data['Linear Complexity']]

# print(data['Nonoverlapping Template'])
print((data > 1).sum())

outfile = args.outfile
data.to_csv(outfile)