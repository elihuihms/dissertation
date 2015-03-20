#!/usr/bin/env python

from sys import argv

from scipy import interpolate
from scipy import logspace
from scipy import optimize
from numpy import exp,sqrt,mean,log10
from glob import glob
from random import uniform

npoints = 1000

def get_datapoints(path):
	f1 = open(path)
	f2 = open("%s.1"%path)
	f3 = open("%s.2"%path)
	X,Y = [],[]

	l1 = f1.readlines()[2:]
	l2 = f2.readlines()[2:]
	l3 = f3.readlines()[2:]

	assert( len(l1) == len(l2) )
	assert( len(l1) == len(l3) )

	for i in xrange(len(l1)):
		a1 = map(float,l1[i].split())
		a2 = map(float,l2[i].split())
		a3 = map(float,l3[i].split())

		assert( a1[0] == a2[0] )
		assert( a1[0] == a3[0] )

		X.append( a1[0] )
		Y.append( mean([a1[1],a2[1],a3[1]]) )

	f1.close()

	return X,Y

def make_phases( x, t ):
	i,j,n,ret = 0,0,len(x)/2,[0.0]*len(t)
	for i in xrange(len(t)):
		for j in xrange(n):
			if x[j] > 2:
				ret[i] += x[j+n]*(1-exp(-1*(10**2)*t[i])) + 10**x[j]
			ret[i] += x[j+n]*(1-exp(-1*(10**x[j])*t[i]))

	return ret

def fit_exp( x, t, I ):
	ret,fit = 0,make_phases( x, t )
	for i in xrange(len(t)):
		ret += (I[i] - fit[i])**2
	return sqrt(ret)/len(t)

fix_phases = False
min_phases = 1
max_phases = 3
max_starts = 10

if len(argv) == 1:
	files = glob("model_*.gdat")
	params = None
elif argv[-1] == '.':
	files = [argv[1]]
	params = map(float,argv[2:len(argv)-1])
	fix_phases = True
else:
	files = [argv[1]]
	params = map(float,argv[2:])

for path in [files[-1]]:

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
				x0 = [ log10(params[k]) for k in xrange(len(params)/2) ]
				x0 += [ params[k] for k in xrange(len(params)/2,len(params)) ]
			else:
				x0 = [ uniform( -3, 0 ) for k in xrange(z) ]
				x0 += [ uniform( -1*new_intensity[-1], new_intensity[-1] ) for k in xrange(z) ]

			if fix_phases:
				best_conditions = x0
				best_score = fit_exp(x0,new_time,new_intensity)
				continue

			ret = optimize.fmin_powell(fit_exp,x0,args=(new_time,new_intensity),full_output=True)

			if ret[1] < best_score:
				best_conditions = ret[0]
				best_score = ret[1]

		if best_conditions == []:
			continue

		amp = [x for y, x in sorted(zip(best_conditions[:z],best_conditions[z:]),reverse=True)]
		tau = [10**x for x in sorted(best_conditions[:z],reverse=True)]

		print tau + amp
		output1 = open("exp_fit.log","a")
		output1.write("%s	%i	%f	%s	%s\n"%(path,z,best_score,"\t".join(map(str,tau)),"\t".join(map(str,amp))))
		output1.close()

		output2 = open("%s_%i.fit"%(path.replace(".gdat",""),z),'w')
		fit = make_phases( best_conditions, new_time )
		for j in xrange(len(new_time)):
			output2.write("%f	%f	%f\n"%(new_time[j],new_intensity[j],fit[j]))
		output2.close()






