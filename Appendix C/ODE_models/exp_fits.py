#!/usr/bin/env python

from scipy import optimize
from numpy import exp
from glob import glob

from matplotlib import pyplot as plot

def get_datapoints(path):
	f = open(path)
	X,Y = [],[]
	for l in f.readlines():
		a = l.split()
		X.append( float(a[0]) )
		Y.append( float(a[1]) )
	f.close()
	return X,Y

def fit_1exp( x, t, I ):
	ret = 0
	for i in xrange(len(t)):
		Ifit = x[1]*(1-exp(-1*x[0]*t[i]))
		ret += (I[i] - Ifit)**2
	return ret

def fit_2exp( x, t, I ):
	ret = 0
	for i in xrange(len(t)):
		Ifit = (x[2]*(1-exp(-1*x[0]*t[i]))) + (x[3]*(1-exp(-1*x[1]*t[i])))
		ret += (I[i] - Ifit)**2
	return ret

def fit_3exp( x, t, I ):
	ret = 0
	for i in xrange(len(t)):
		Ifit = (x[3]*(1-exp(-1*x[0]*t[i]))) + (x[4]*(1-exp(-1*x[1]*t[i]))) + (x[5]*(1-exp(-1*x[2]*t[i])))
		ret += (I[i] - Ifit)**2
	return ret

output = open("exp_fits.log","a")

#for file in glob('model_TAA_*.txt'):
for file in glob('model_TAT_*.txt'):

	time,intensity = get_datapoints(file)

#	x0_1 = (5,1)
	x0_2 = (5,1,1,1)

#	ret_1 = optimize.fmin_powell(fit_1exp,x0_1,args=(time,intensity),full_output=True)
	ret_2 = optimize.fmin_powell(fit_2exp,x0_2,args=(time,intensity),full_output=True)

#	plot.scatter(time,intensity)
#	plot.plot(time,[ret_1[0][1]*(1-exp(-1*ret_1[0][0]*t)) for t in time])
#	plot.show()

#	output.write("%s	1	%f	%s\n"%(file,ret_1[1],"\t".join(map(str,ret_1[0]))))
#	output.write("%s	2	%f	%s\n"%(file,ret_2[1],"\t".join(map(str,ret_2[0]))))

	output.write("%s	%f	%f\n"%(file,ret_2[0][0],ret_2[0][1]))

output.close()








