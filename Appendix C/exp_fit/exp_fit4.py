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
	for lines in zip(*data)
		a = [ map(float,l.split()) for l in lines ]

		print a
		exit()

		X.append( a[0][0] )
		Y.append( mean(zip(*a)[1]) )
		Z.append(  std(zip(*a)[1]) )

	f1.close()

	return X,Y,Z

def make_phases( x, t ):
	i,j,n,ret = 0,0,len(x)/2,[0.0]*len(t)
	for i in xrange(len(t)):
		for j in xrange(n):
			ret[i] += x[j+n]*(1-exp(-1*(10**x[j])*t[i]))

	return ret

def fit_exp( x, t, I, dI ):
	ret,fit = 0,make_phases( x, t )
	for i in xrange(len(t)):
		if dI[i] != 0:
			ret += (I[i] - fit[i])**2/dI[i]**2
	return ret/len(t)

fix_phases = False
min_phases = 1
max_phases = 4
num_starts = 1

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

if params != None:
	assert(len(params)%2==0)
	max_phases = len(params)/2
	min_phases = max_phases

for z in xrange(min_phases,max_phases+1):

	if params != None:
		starts = 1
	else:
		starts = z**2 * num_starts

	for path in files[1:]:
		time,intensity,sigma = get_datapoints(path)
		best_score, best_conditions = 1E10, []

		for j in xrange(starts):

			if params != None:
				x0 = [ log10(params[k]) for k in xrange(len(params)/2) ]
				x0 += [ params[k] for k in xrange(len(params)/2,len(params)) ]
			else:
				x0 = [ uniform( -3, 0 ) for k in xrange(z) ]
				x0 += [ intensity[-1] * random() for k in xrange(z) ]

			if fix_phases:
				best_conditions = x0
				best_score = fit_exp(x0,time,intensity)
				continue
			print "x0: %s"%(x0)
			ret = optimize.fmin_powell(fit_exp,x0,args=(time,intensity,sigma),full_output=True)

			if ret[1] < best_score:
				best_conditions = ret[0]
				best_score = ret[1]

		if best_conditions == []:
			continue

		amp = [x for y, x in sorted(zip(best_conditions[:z],best_conditions[z:]),reverse=True)]
		tau = [10**x for x in sorted(best_conditions[:z],reverse=True)]

		print "Opt: %s"%(tau + amp)
		output1 = open("exp_fit.log","a")
		output1.write("%s	%i	%f	%s	%s\n"%(path,z,best_score,"\t".join(map(str,tau)),"\t".join(map(str,amp))))
		output1.close()

		output2 = open("%s_%i.fit"%(path.replace(".gdat",""),z),'w')
		fit = make_phases( best_conditions, time )
		for j in xrange(len(time)):
			output2.write("%f	%f	%f\n"%(time[j],intensity[j],fit[j]))
		output2.close()

	output1 = open("exp_fit.log","a")
	output1.write("\n")
	output1.close()




