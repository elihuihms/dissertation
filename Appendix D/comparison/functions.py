#!/usr/bin/env python

import math
import scipy
import matplotlib.pyplot as plt

def SK(L,K,a1,a2):
	return (1
	+( 11*K*L*a1**2 )
	+( K**2 * L**2 * ( 44*a1**4        +  11*a1**2*a2) )
	+( K**3 * L**3 * ( 77*a1**6        +  77*a1**4*a2    +  11*a1**2*a2**2) )
	+( K**4 * L**4 * ( 55*a1**8        + 165*a1**6*a2    +  99*a1**4*a2**2 +  11*a1**2*a2**3) )
	+( K**5 * L**5 * ( 11*a1**10       + 110*a1**8*a2    + 220*a1**6*a2**2 + 110*a1**4*a2**3 + 11*a1**2*a2**4) )
	+( K**6 * L**6 * ( 11*a1**10*a2    + 110*a1**8*a2**2 + 220*a1**6*a2**3 + 110*a1**4*a2**4 + 11*a1**2*a2**5) )
	+( K**7 * L**7 * ( 55*a1**8 *a2**3 + 165*a1**6*a2**4 +  99*a1**4*a2**5 +  11*a1**2*a2**6) )
	+( K**8 * L**8 * ( 77*a1**6 *a2**5 +  77*a1**4*a2**6 +  11*a1**2*a2**7) )
	+( K**9 * L**9 * ( 44*a1**4 *a2**7 +  11*a1**2*a2**8) )
	+( K**10* L**10* ( 11*a1**2 *a1**9) )
	+( K**11* L**11* a2**11 )
	)

def IAN(L,K,X,Y):
	return (1
	+( K**1 * L**1 * (11) )
	+( K**2 * L**2 * (44 + 11*X**2) )
	+( K**3 * L**3 * (77 + 77*X**2      + 11*X**2*Y) )
	+( K**4 * L**4 * (55 +165*X**2      + 66*X**2*Y    +11*X**2*Y**2 +33*X**4) )
	+( K**5 * L**5 * (11 +110*X**2      +110*X**2*Y    +55*X**2*Y**2 +11*X**2*Y**3 +110*X**4      +55*X**4*Y) )
	+( K**6 * L**6 * ( 0 + 11*X**2      + 44*X**2*Y    +66*X**2*Y**2 +44*X**2*Y**3 + 11*X**2*Y**4 +66*X**4      +132*X**4*Y    +66*X**4*Y**2 +22*X**6) )
	+( K**7 * L**7 * ( 0 + 11*X**2*Y**2 + 33*X**2*Y**3 +33*X**2*Y**4 +11*X**2*Y**5 + 33*X**4*Y    +99*X**4*Y**2 + 66*X**4*Y**3 +11*X**6      +33*X**6*Y) )
	+( K**8 * L**8 * ( 0 + 11*X**2*Y**4 + 22*X**2*Y**5 +11*X**2*Y**6 +44*X**4*Y**3 + 55*X**4*Y**4 +22*X**6*Y**2) )
	+( K**9 * L**9 * ( 0 + 11*X**2*Y**6 + 11*X**2*Y**7 +33*X**4*Y**5) )
	+( K**10* L**10* ( 0 + 11*X**2*Y**8) )
	+( K**11* L**11* (Y**11) )
	)

def theta(func,L,K,A,B,tol=1E-10):
	dF = [math.log(func(K,L-(tol/2),A,B)),math.log(func(K,L+(tol/2),A,B))]
	dC = math.log(L-(tol/2)),math.log(L+(tol/2))
	return (dF[1]-dF[0])/(dC[1]-dC[0])

def obj( x, func, concs, data ):
	assert len(concs) == len(data)
	K,A,B = [10**f for f in x]
	return sum([(data[i]-theta(func,concs[i],K,A,B))**2 for i in xrange(len(concs))])

def leastsq( x, func, concs, data ):
	assert len(concs) == len(data)
	k,A,B = x
	f = [(data[i]-theta(func,concs[i],k,A,B))**2 for i in xrange(len(concs))]
	return f

def plot(X,Y,Z=None,title=None):
	plt.xscale('log')
	plt.xlim([min(X),max(X)])
	plt.scatter(X,Y)
	if Z!= None: plt.plot(X,Z,c='r')
	if title!= None: plt.title(title)
	plt.show()

def opt_range( func, K, A, B, pts=100, min=-9, max=1, high=10.9, low=0.1 ):

	L,R = max,min
	while( L > min ):
		L -=1
		if theta(func,10**L,K,A,B) < low: break

	while( R < max ):
		R +=1
		if theta(func,10**R,K,A,B) > high: break

	return scipy.logspace(L,R,pts)




