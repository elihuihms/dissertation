#!/usr/bin/env python

import argparse

from DEERSimLib import *
from scipy import recfromtxt,optimize

# parser block
parser = argparse.ArgumentParser()
parser.add_argument('-dist', metavar='<FILE>', required=True, help='Integrate over a distribution of inter-label distances (in *angstroms* !).')
parser.add_argument('-out', metavar='<FILE>', required=True, help="The file to write the DEER curve to")
parser.add_argument('-Dip', metavar='52.04', type=float, default=52.04, help='Dipolar susceptibility (MHz/nm^3)')
parser.add_argument('-T', metavar='2.5', default=2.5, type=float, help='Final t (us)')
parser.add_argument('-dW', metavar='(Inf)', type=float, default=None, help='Effective excitation bandWith (MHz)')
parser.add_argument('-Tstep', metavar='0.025', default=None, type=float, help='Time resolution (us)')
parser.add_argument('-fit', metavar='<FILE>', default=None, help='Experimental data to fit.')
parser.add_argument('-fitdW', action='store_true', default=None, help='Improve fitting to experimental data by optimizing the effective excitation bandwidth')
args = parser.parse_args()

# default to 100 steps
if(args.Tstep == None):
	args.Tstep = args.T / 100

# convert dipolar coupling to MHz/A**3
args.Dip = args.Dip*1000.0

# read distribution of distances from file
distances = recfromtxt( args.dist )
if( len(distances[0]) != 2 ):
	print "Distribution file must be of the format: \"r w\""
	exit()

if(args.fit):

	exp = recfromtxt( args.fit, unpack=True )
	if( len(exp) != 3 ):
		print "Experimental data file must contain t, Vt, and dVt columns"
		exit()

	n = len(exp[0])
	def f2( x ):
		norm = DEER_Vt( args.Dip, distances, 0.0, x[1] ) + x[0]
		tmp = [0.0]*n
		for i in range(n):
			tmp[i] = (DEER_Vt( args.Dip, distances, exp[0][i], x[1] ) + x[0]) / norm
		ret = reducedChisq( exp[1], exp[2], tmp )
		print "Current dW: %f, ChiSq = %f" % (x[1],ret)
		return ret

	if(args.fitdW):
		print "Optimizing excitation bandwith:"
		(offset,args.dW) = optimize.fmin_tnc( f2, x0=(0,1), bounds=((0,None),(0,None)), approx_grad=True, messages=False)[0]
		print "Optimized excitation bandwith: %.2fMHz" % args.dW
	else:
		fit = [0.0]*n
		for i in range(n):
			fit[i] = DEER_Vt( args.Dip, distances, exp[0][i], args.dW )

		def f1( x ):
			norm = DEER_Vt( args.Dip, distances, 0.0, args.dW ) + x
			tmp = [0.0]*n
			for i in range(n):
				tmp[i] = (fit[i] + x) / norm
			return reducedChisq( exp[1], exp[2], tmp )

		offset = optimize.fminbound( f1, 0.0, 1E9 )
		print offset

	f = open( args.out, 'w')
	norm = DEER_Vt( args.Dip, distances, 0.0, args.dW ) + offset
	for i in range(n):
		fit = DEER_Vt( args.Dip, distances, exp[0][i], args.dW ) + offset
		f.write("%.3f\t%.3f\t%.3f\t%.3f\n" % (
			exp[0][i],
			exp[1][i],
			fit/norm,
			exp[1][i] - (fit/norm)) )

	f.close()
	exit()

t = 0.0
Vt = {}
while( t < args.T ):
	Vt[t] = DEER_Vt( args.Dip, distances, t, args.dW )
	t += args.Tstep

f = open( args.out, 'w')
t = 0.0
while( t < args.T ):
	f.write("%.3f\t%.3f\n" % (t,Vt[t]/Vt[0.0]))
	t += args.Tstep
f.close()