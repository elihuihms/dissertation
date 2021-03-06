from math 	import exp,log,sqrt

R = 8.3144621 # J/(K*mol)

def dG_from_Kd( Kd, T ):
	return R*T*log(Kd)

def Kd_from_dG( dG, T ):
	return exp( dG/(R*T) )

def dS_from_dGdH( dG, dH, T ):
	return (dG-dH)/(-1.0*T)

def J_from_cal( cal ):
	return cal / 0.239005736

def cal_from_J( joules ):
	return joules * 0.239005736

def get_ratios( A, B ):
	"""
	Returns a list of ratios between the points in two lists
	"""
	n = len(A)
	assert( n == len(B) )
	ret = [0.0]*n
	for i in xrange(n):
		ret[i] = A[i] / B[i]
	return ret

def get_scale( A, B ):
	"""
	Returns the correct scaling factor between two lists of values
	"""
	n = len(A)
	assert( n == len(B) )
	return ( sum(A)/n )/( sum(B)/n )

def normalize( x, y ):
	"""
	Superimposes y on x
	"""
	n = len(x)
	assert( n == len(y) )

	# calculate root mean square for each dataset
	x_avg, y_avg = sum(x)/n, sum(y)/n
	x_rms, y_rms = 0.0, 0.0
	for i in xrange(n):
		x_rms += (x[i] - x_avg)**2
		y_rms += (y[i] - y_avg)**2
	x_rms, y_rms = sqrt(x_rms/n), sqrt(y_rms/n)

	# translate y data to origin, normalize scale, then transform back using data to be normalized to
	y_norm = [0.0]*n
	for i in xrange(n):
		y_norm[i] = (x_rms*(y[i] - y_avg)/y_rms) + x_avg

	return y_norm

def dK_Gibbs_Helmholtz( T, T0, K0, dH0, dCp ):
	"""
	Eqn. 19 from Winzor and Jackson (2006), also Naghibi et al., 1995
	"""

	return exp(
		log(K0) + ( ((dH0-(T0*dCp)) / R)*((1.0/T0)-(1.0/T)) ) + ((dCp/R)*log(T/T0))
		)

def dH_vant_Hoff( dH0, dCp, T, T0 ):
	"""
	Integrated van't Hoff equation 12a from Prabhu & Sharp, AR Reviews (2005)
	"""
	return dH0 + (dCp*(T-T0))


def dG_vant_Hoff( dG0, dH0, dCp, T, T0 ):
	"""
	Integrated van't Hoff equation 12c from Prabhu & Sharp, AR Reviews (2005)
	Assumes a constant dCp (i.e. linear dH w.r.t. T)
	"""
	dS0 = (dH0 - dG0) / T0
	return dH0 - (T*dS0) + (dCp*( (T-T0) - (T*log(T/T0)) ))

def dG_vant_Hoff_dH( dG0, dH, dCp, T, T0 ):
	"""
	Integrate van't Hoff equation, but using dH instead of dH0
	Assumes a constant dCp

	Start from eqn. 12c, the integrated van't Hoff equation, from Prabhu and Sharp (2005):
	dG = dH(T0) - T*dS(T0) + dCp[ (T-T0) - T*ln(T/T0) ]
	...
	Substitute definition for dS0 from Gibbs-Helmholtz eqn. (see Winzor and Jackson):
	dH(T0) = dG(T0) + T0*dS(T0)
	dS(T0) = ( dH(T0) - dG(T0) )/T0

	dG = dH(T0) - (T/T0)*[ dH(T0) - dG(T0) ] + dCp[ (T-T0) - T*ln(T/T0) ]
	...
	Substitute definition for dH0 from Prabhu and Sharp (2005);
	dH(T) = dH(T0) + dCp*(T-T0)
	dH(T0) = dH(T) - dCp*(T-T0)

	dG = dH(T) - dCp*(T-T0) - (T/T0)*[ dH(T) - dCp*(T-T0) - dG(T0) ] + dCp[ (T-T0) - T*ln(T/T0) ]
	"""

	return dH - dCp*(T-T0) - (T/T0)*( dH - dCp*(T-T0) - dG0 ) + dCp*( (T-T0) - T*log(T/T0) )

def dQ_calc( Q, V0, I_vol ):
	"""
	Eqn. 10 from Microcal's "ITC Data Analysis in Origin"
	"""
	dQ = [0.0]*len(Q)

	for i in xrange(0,len(Q)):
		if(i==0):
			dQ[i] = Q[i] + ( (I_vol[i]/V0)*((Q[i]-0.0000)/2) )
		else:
			dQ[i] = Q[i] + ( (I_vol[i]/V0)*((Q[i]+Q[i-1])/2) ) - Q[i-1]

	return dQ
