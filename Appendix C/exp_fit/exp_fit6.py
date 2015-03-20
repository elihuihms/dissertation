#!/usr/bin/env python

from sys import argv
from scipy import interpolate
from scipy import logspace
from scipy import optimize
from numpy import exp,sqrt,mean,std
from glob import glob
from random import uniform,random

npoints = 1000

def get_datapoints(path):
	handles = [None]*5
	handles[0] = open(path)
	for i in xrange(1,5):
		handles[i] = open("%s.1"%path)
	X,Y,Z = [],[],[]

	data = [ h.readlines()[2:] for h in handles ]
	for lines in zip(*data):
		a = [ map(float,l.split()) for l in lines ]

		X.append( a[0][0] )
		Y.append( mean(zip(*a)[1]) )
		Z.append(  std(zip(*a)[1]) )

	for h in handles:
		h.close()

	return X,Y,Z

def make_phases( x, t, cutoff=2 ):
	i,j,n,ret = 0,0,len(x)/2,[0.0]*len(t)
	for i in xrange(len(t)):
		for j in xrange(n):
			ret[i] += x[j+n]*(1-exp(-1*(x[j])*t[i]))

	return ret

def fit_exp_dI( x, t, I, dI ):
	ret,fit = 0,make_phases( x, t )
	for i in xrange(len(t)):
		if dI[i] != 0:
			ret += (I[i] - fit[i])**2/dI[i]**2
	print x,ret/len(t)
	return ret/len(t)

def fit_exp( x, t, I ):
	ret,fit = 0,make_phases( x, t )
	for i in xrange(len(t)):
		if dI[i] != 0:
			ret += (I[i] - fit[i])**2
	return sqrt(ret)/len(t)

min_phases = 2
max_phases = 2

knone_11_starts = [
	( 0.08, 1428),
	( 0.34, 0.05, 515, 955),
	( 0.34, 0.05, 0.05, 515, 955, 38)]

koff_11_starts = [
	( 0.03, 4751 ),
	( 0.07, 0.001, 6006, -10757 ),
	( 0.55, 0.05, 0.05, 351, 66373, 62242  )]

kon_11_starts = [
	( 0.09, 4568 ),
	( 0.1, 0.01, 4385, 183 ),
	( 0.55, 0.05, 0.05, 351, 66373, 62242  )]

koff_51_starts = [
	( 0.10, 9388 ),
	( 0.11, 0.007, 8605, 2091 ),
	( 5.49, 0.11, 0.003, 63, 8667, 3327 )]

kon_51_starts = [
	( 0.19, 9170 ),
	( 0.22, 0.01, 8309, 2375 ),
	( 5.19, 1.01, 0.07, -4712, 12467, 28489  ),
	( 5.19, 1.01, 0.07, 0.22, -4712, 12467, 28489, 8309  )]

for i in xrange(min_phases,max_phases+1):

	x0 = knone_11_starts[i-1]

	for path in argv[1:]:
		T,I,dI = get_datapoints(path)

		f = interpolate.interp1d(T,I)
		d = interpolate.interp1d(T,dI)

		time = logspace(-1,2,200)
		intensity = f(time)

		ret = optimize.fmin(fit_exp,x0,args=(time,intensity),maxfun=1E6,maxiter=1E4,full_output=True)

		amp = [y for x, y in sorted(zip(ret[0][:i],ret[0][i:]),reverse=True)]
		tau = [x for x in sorted(ret[0][:i],reverse=True)]

		print "Opt: %s"%(tau + amp)
		output1 = open("exp_fit.log","a")
		output1.write("%s	%i	%f	%s	%s\n"%(path,i,ret[1],"\t".join(map(str,tau)),"\t".join(map(str,amp))))
		output1.close()

		output2 = open("%s_%i.fit"%(path.replace(".gdat",""),i),'w')
		fit = make_phases( ret[0], time )
		for j in xrange(len(time)):
			output2.write("%f	%f	%f\n"%(time[j],intensity[j],fit[j]))
		output2.close()

		x0 = ret[0]

	output1 = open("exp_fit.log","a")
	output1.write("\n")
	output1.close()




