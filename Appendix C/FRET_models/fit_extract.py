#!/usr/bin/env python

from scipy import interpolate
from scipy import logspace
from scipy import optimize
from numpy import exp

file_sets = [
	('./raw/Run8783.dat','uAT_1.fit', (7.79444009319,0.346472520156,0.002069147563,0.1119321903780,0.123633038262,0.184046569727,0.107320093906)),
	('./raw/Run8787.dat','uAT_2.fit', (7.83921591894,0.468945369101,0.171470581619,0.0236762839406,0.219514034109,0.158049459857,0.087760986516)),
	('./raw/Run8795.dat','uAT_3.fit', (7.81288305142,0.614616667216,0.171985949952,0.0250586379685,0.321761500293,0.215419671279,0.102728883164)),
	('./raw/Run8760.dat','wtAT_1.fit',(9.41419019241,0.349093923557,0.040697114579,0.0307783644224,0.195792878453,0.208334677880,0.103522228182)),
	('./raw/Run8769.dat','wtAT_2.fit',(7.17938110172,0.661061189507,0.029746125470,0.1140880825920,0.266222167666,0.208534105399,0.264314369925)),
	('./raw/Run8775.dat','wtAT_3.fit',(7.51255224419,0.214506775755,1.048311596250,0.0354973649567,0.349494587970,0.298481114453,0.309256629695))]

npoints = 1000

def get_datapoints(path):
	f = open(path)
	X,Y = [],[]
	for l in f.readlines():
		a = l.split()
		X.append( float(a[0]) )
		Y.append( float(a[1]) )
	f.close()
	return X,Y

def exp1( x, t ):
	return [x[0] + (x[2]*exp(-1*x[1]*t[i])) for i in xrange(len(t))]

def exp2( x, t):
	return [x[0] + (x[3]*exp(-1*x[1]*t[i])) + (x[4]*exp(-1*x[2]*t[i])) for i in xrange(len(t))]

def exp3( x, t):
	return [x[0] + (x[4]*exp(-1*x[1]*t[i])) + (x[5]*exp(-1*x[2]*t[i])) + (x[6]*exp(-1*x[3]*t[i])) for i in xrange(len(t))]

for inpath,outpath,params in file_sets:
	time,intensity = get_datapoints(inpath)
	f = interpolate.interp1d(time,intensity)

	# determine if dataset goes to 50 or 100s
	if time[-1] > 95:
		end_exp = 1.98
	elif time [-1] > 48:
		end_exp = 1.68

	new_time = logspace(-1,end_exp,1000)
	new_intensity = f(new_time)

	if len(params) == 3:
		fit_intensity = exp1( params, new_time )
	elif len(params) == 5:
		fit_intensity = exp2( params, new_time )
	elif len(params) == 7:
		fit_intensity = exp3( params, new_time )

	output = open(outpath,'w')
	for i in xrange(len(new_time)):
		output.write("%f	%f	%f\n"%(new_time[i],new_intensity[i],fit_intensity[i]))
	output.close()








