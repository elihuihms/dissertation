#!/usr/bin/env python

from math import sqrt

R0 = 56

def get_atoms(file, atomname):
	ret = []
	h = open(file)
	for l in h.readlines():
		a = l.split()
		#ATOM      0  QT  LYS A  71     -23.810  16.870   5.390
		if a[0] == "ATOM" and atomname==a[2]:
			ret.append( [float(a[6]),float(a[7]),float(a[8])] )
	h.close()
	return ret

def dist( A, B ):
	return sqrt( (A[0]-B[0])**2 + (A[1]-B[1])**2 + (A[2]-B[2])**2 )

ctr,ret = 0,0
for A in get_atoms('1TRAP_1AT/00000.pdb','QT'):
	for B in get_atoms('1TRAP_1AT/00000.pdb','QA'):
		D = dist(A,B)
		if D == 0:
			continue
		print D
		ctr += 1
		ret += 1/(1 + (D/R0)**6 )

print "TRAP-AT : %f"%(ret/ctr)


ctr,ret = 0,0
for A in get_atoms('2TRAP_1AT/00000.pdb','QT'):
	for B in get_atoms('2TRAP_1AT/00000.pdb','QU'):
		D = dist(A,B)
		if D == 0:
			continue
		print D
		ctr += 1
		ret += 1/(1 + (D/R0)**6 )

print "TRAP-TRAP : %f" %(ret/ctr)


