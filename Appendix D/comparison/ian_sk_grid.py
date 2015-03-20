#!/usr/bin/env python

from sys		import argv
from scipy		import optimize
from functions	import *

mode = int(argv[1])

if mode == 0:
	fname = "ian_fit_sk_powell.txt"
	f1 = SK
	f2 = IAN
elif mode == 1:
	fname = "ian_fit_sk_fmin.txt"
	f1 = SK
	f2 = IAN
elif mode == 2:
	fname = "sk_fit_ian_powell.txt"
	f1 = IAN
	f2 = SK
elif mode == 3:
	fname = "sk_fit_ian_fmin.txt"
	f1 = IAN
	f2 = SK

h = open(fname, 'w')
h.write( "K\tA\tB\tK\tA\tB\tSSE\n")

for K in scipy.logspace(3,9,20):
	for A in scipy.logspace(-3,3,20):
		for B in scipy.logspace(-3,3,20):

			X, Y = [],[]
			for L in opt_range(f1,K,A,B): #scipy.logspace(-7,1,100):
				X.append( L )
				Y.append( theta(f1,L,K,A,B) )
			if Y[0] > 10.9:
				h.write( "%.3E\t%.3F\t%.3F\tFAIL_MIN\n" % (K,A,B) )
				continue
			if Y[-1] < 0.1:
				h.write( "%.3E\t%.3F\t%.3F\tFAIL_MAX\n" % (K,A,B) )
				continue

			try:
				if mode == 0 or mode == 2:
					ret = optimize.fmin_powell( obj, x0=[math.log10(K),0,0], args=(f2,X,Y), disp=0 )
				else:
					ret = optimize.fmin( obj, x0=[math.log10(K),0,0], args=(f2,X,Y), disp=0 )

				fit = [10**x for x in ret]
			except ValueError:
				h.write( "%.3E\t%.3F\t%.3F\tFAIL_MATH\n" % (K,A,B) )
			else:
				h.write( "%.3E\t%.3F\t%.3F\t%.3E\t%.3F\t%.3F\t%.5F\n" % (K,A,B,fit[0],fit[1],fit[2],obj((ret[0],ret[1],ret[2]),f2,X,Y)) )

h.close()
