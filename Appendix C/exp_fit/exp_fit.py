#!/usr/bin/env python

from sys import argv

from scipy import interpolate
from scipy import logspace
from scipy import optimize
from numpy import exp,sqrt
from glob import glob
from random import uniform

npoints = 1000

def get_datapoints(path):
	f = open(path)
	X,Y = [],[]
	for l in f.readlines()[1:]:
		a = l.split()
		X.append( float(a[0]) )
		Y.append( float(a[1]) )
	f.close()
	return X,Y

def make_phases( x, t ):
	i,j,n,ret = 0,0,len(x)/2,[0.0]*len(t)
	for i in xrange(len(t)):
		for j in xrange(n):
			ret[i] += x[j+n]*(1-exp(-1*x[j]*t[i]))

	return ret

def fit_exp( x, t, I ):
	ret,fit = 0,make_phases( x, t )
	for i in xrange(len(t)):
		ret += (I[i] - fit[i])**2
	return sqrt(ret)/len(t)

output1 = open("exp_fit.log","a")

min_phases = 1
max_phases = 4
max_starts = 10

if len(argv) == 0:
	files = glob("model_*.gdat")
	params = None
else:
	files = [argv[1]]
	params = map(float,argv[2:])

for path in files:

	time,intensity = get_datapoints(path)
	f = interpolate.interp1d(time,intensity)

	new_time = logspace(-1,2,1000)
	new_intensity = f(new_time)

	if params != None:
		assert(len(params)%2==0)
		max_phases = len(params)/2
		min_phases = max_phases
		max_starts = 1

	for z in xrange(min_phases,max_phases+1):
		best_score, best_conditions = 1E10, []

		for j in xrange(max_starts):

			if params != None:
				x0 = params
			else:
				x0 = [ uniform( 0, 1 ) for k in xrange(z) ]
				x0 += [ uniform( -1*new_intensity[-1], new_intensity[-1] ) for k in xrange(z) ]

			ret = optimize.fmin_powell(fit_exp,x0,args=(new_time,new_intensity),full_output=True)

			if ret[1] < best_score:
				best_conditions = ret[0]
				best_score = ret[1]

		if best_conditions == []:
			continue

		amp = [x for y, x in sorted(zip(best_conditions[:z],best_conditions[z:]),reverse=True)]
		tau = sorted(best_conditions[:z],reverse=True)

		print tau + amp
		output1.write("%s	%i	%f	%s	%s\n"%(path,z,best_score,"\t".join(map(str,tau)),"\t".join(map(str,amp))))

		output2 = open("%s_%i.fit"%(path.replace(".gdat",""),z),'w')
		fit = make_phases( best_conditions, new_time )
		for j in xrange(len(new_time)):
			output2.write("%f	%f	%f\n"%(new_time[j],new_intensity[j],fit[j]))
		output2.close()

	output1.write("\n")

output1.close()








