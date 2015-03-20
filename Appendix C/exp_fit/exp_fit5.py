#!/usr/bin/env python

from sys import argv
from scipy import interpolate
from scipy import logspace
from scipy import optimize
from numpy import exp,sqrt,mean,std,log10
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
			ret[i] += 10**x[j+n]*(1-exp(-1*(10**x[j])*t[i]))

	return ret

def fit_exp( x, t, I, dI ):
	ret,fit = 0,make_phases( x, t )
	for i in xrange(len(t)):
		if dI[i] != 0:
			ret += (I[i] - fit[i])**2/dI[i]**2
	print x,ret/len(t)
	return ret/len(t)

min_phases = 1
max_phases = 4

for i in xrange(min_phases,max_phases+1):

	for path in argv[1:]:
		T,I,dI = get_datapoints(path)

#		f = interpolate.interp1d(T,I)
#		d = interpolate.interp1d(T,dI)
#
#		time = logspace(-1,2,200)
#		intensity = f(time)
#		sigma = d(time)

		points,j = [],0
		while j**2/5 < len(T):
			points.append( int(j**2/5) )
			j+=1
		points = sorted(set( points ))

		time		= [T[j] for j in points]
		intensity	= [I[j] for j in points]
		sigma		= [dI[j] for j in points]

		x0 =  [ -1 * k for k in xrange(i) ]
		x0 += [ log10( intensity[-1] / i ) for j in xrange(i) ]
		print "x0: %s"%(x0)

		ret = optimize.fmin_powell(fit_exp,x0,args=(time,intensity,sigma),full_output=True)

		tau = [10**x for y, x in sorted(zip(ret[0][i:],ret[0][:i]),reverse=True)]
		amp = [10**x for x in sorted(ret[0][i:],reverse=True)]

		print "Opt: %s"%(amp + tau)
		output1 = open("exp_fit.log","a")
		output1.write("%s	%i	%f	%s	%s\n"%(path,i,ret[1],"\t".join(map(str,tau)),"\t".join(map(str,amp))))
		output1.close()

		output2 = open("%s_%i.fit"%(path.replace(".gdat",""),i),'w')
		fit = make_phases( ret[0], time )
		for j in xrange(len(time)):
			output2.write("%f	%f	%f	%f\n"%(time[j],intensity[j],sigma[j],fit[j]))
		output2.close()

	output1 = open("exp_fit.log","a")
	output1.write("\n")
	output1.close()




