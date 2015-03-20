#!/usr/bin/python

from os.path import basename
from sys import argv
import glob
import re

def chiSq( col1, col2, err ):
	"""
	Returns a chi-squared value between col1 and col2 within the error band percentage
	"""
	
	nValues = len(col1)
	
	sum = 0.0
	for i in range( nValues ):
		sum += ( ((col1[i]) - col2[i]) / (col1[i]*err[i]) )**2
		
	return (1.0/(nValues -1))*sum

i=0
curves = []
names = []

# read error percentage curve
error = []
f = open('err.dat')
rows = f.readlines()
f.close

for r in rows[2:]:
	error.append( float(r) )

# read curves
for file in glob.glob( argv[1]+'/*.dat' ):

	curves.append([])
	names.append( basename(file) )
	
	f = open(file, 'r')	
	rows = f.readlines()
	f.close()
	
	for r in rows[2:]:
		curves[i].append( float(re.split('\s+', r)[1]) )
		
	i+=1
	
f = open('results.tbl', 'w')
f.write( "\t"+("\t".join( names ))+"\n")
for i in range( len(curves) ):
	for j in range( len(curves) ):
		if (j==0):
			f.write( names[i] )
		diff = chiSq( curves[i], curves[j], error )
		f.write( "\t%.3f" % (diff) )
	f.write("\n")
f.close()


	