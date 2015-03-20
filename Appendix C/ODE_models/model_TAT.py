#!/usr/bin/env python

import numpy
import matplotlib.pyplot as plot
import scipy.integrate as integrate
import scipy.optimize as optimize

"""
d[T]/dt	=	- k1f[T][A] + k1b[TA] - k2f[TA][T] + k2b[TAT]
d[A]/dt	=	- k1f[T][A] + k1b[TA]
d[TA]/dt	=	+ k1f[T][A] - k1b[TA] - k2f[TA][T] + k2b[TAT]
d[TAT]/dt	=	+ k2f[TA][T] - k2b[TAT]
"""

k1f = 0.01
k1b = 0.1
k2f = 0.1
k2b = 0.01

def f(y, t):

	T	= y[0]
	A	= y[1]
	TA	= y[2]
	TAT	= y[3]

	f0	=	-1*k1f*T*A + k1b*TA -1*k2f*TA*T + k2b*TAT
	f1	=	-1*k1f*T*A + k1b*TA
	f2	=	k1f*T*A -1*k1b*TA -1*k2f*TA*T + k2b*TAT
	f3	=	k2f*TA*T -1*k2b*TAT

	return (f0,f1,f2,f3)

def expfit(x, y, t, full_output=False):
	fit,n = [],len(t)
	for i in xrange(n):
		fit.append( x[1]*(1-numpy.exp(-1*t*x[0])) )
	if full_output:
		return fit
	else:
		return sum([ (y[i]-fit[i])**2 for i in xrange(n) ])

T0		= 1
A0		= 5
TA0		= 0
TAT0	= 0

y0 = [T0,A0,TA0,TAT0]

t = numpy.linspace(0,100,1000)
ode = integrate.odeint(f,y0,t)
TAT = ode[:,2]

if False:
	x0 = [1,0.5]
	opt = optimize.fmin(expfit,x0,args=([],[],[]))

	fit = expfit(opt,TAT,t,True)
	plot.plot(t,fit)

plot.scatter(t,TAT)
plot.show()