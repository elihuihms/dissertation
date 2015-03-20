#!/usr/bin/python

import sys
import glob
import os.path
from scipy import recfromtxt

def getMu( y_exp, dy, y_fit):
	"""
	Determines the optimal scaling factor for y_fit within the y error band
	"""
	
	# From: Pelikan et. al., Gen. Physiol. Biophys. (2009)
	# doi: 10.4149/gbp_2009_02_174
	# Original: Bernado et al. J. Am. Chem. Soc. (2007)
	
	a = 1.0E-9
	b = 1.0E-9
	for i in range( len(y_exp) ):
		a += ( y_fit[i] * y_exp[i] )/( dy[i]**2 )
		b += ( y_fit[i] * y_fit[i] )/( dy[i]**2 )
	
	return a / b
pass

def chiSqReduced( y_exp, dy, y_fit, scale=1.0, offset=0.0 ):
	"""
	Returns a reduced chi-squared value between y_exp and y_fit within the error band dy
	"""
		
	nValues = len(y_exp)
	
	# now calculate the normalized sum of squares
	sum = 0.0
	for i in range( nValues ):
		sum += ( (((scale * y_fit[i]) + offset) - y_exp[i]) / dy[i] )**2
		
	return (1.0/(nValues -1))*sum
pass

def getChiSq(x,y,dy,file):
	(file_x,file_y) = recfromtxt( file, unpack=True, skip_header=6 )
	if( len(file_x) != len(x) ):
		print "File %s doesn't have same number of x values" % (file)
		sys.exit(0)
	if( file_x[0] != x[0] ):
		print "File %s doesn't start at same x value" % (file)
		sys.exit(0)
	
	scale = getMu( y, dy, file_y)
	return chiSqReduced( y, dy, file_y, scale )
pass

if(len(sys.argv) < 2):
	print "Usage: make_conf_chisq.py <target.mes> <conf_dir>"
	sys.exit(0)

(x,y,dy) = recfromtxt( sys.argv[1], unpack=True, skip_header=5 )

confs = glob.glob("%s/*.mes"%sys.argv[2])

if(len(confs)==0):
	print "No valid MESMER confs found.\n";
	sys.exit(0)
	
for conf in confs:
	print "%s\t%.3f" % (os.path.basename(conf),getChiSq(x,y,dy,conf))
	sys.stdout.flush()