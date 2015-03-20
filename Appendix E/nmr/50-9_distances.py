#!/usr/bin/env python

from pdb_lib import *
from glob import glob

def get_minimums(f):
	G1 = getAtomCoords(f,startRes=9,endRes=9,atomName='OE1')
	G2 = getAtomCoords(f,startRes=9,endRes=9,atomName='OE2')
	H1 = getAtomCoords(f,startRes=50,endRes=50,atomName='ND1')
	H2 = getAtomCoords(f,startRes=50,endRes=50,atomName='NE2')

	min_distances = []
	for i in xrange(len(G1)):

		d1,d2,d3,d4 = [],[],[],[]
		for j in xrange(len(H1)):

			d1.append( getDistance(G1[i],H1[j]) )
			d2.append( getDistance(G1[i],H2[j]) )
			d3.append( getDistance(G2[i],H1[j]) )
			d4.append( getDistance(G2[i],H2[j]) )

		m1,m2,m3,m4 = min(d1),min(d2),min(d3),min(d4)

		min_distances.append( min([m1,m2,m3,m4]) )
	return min_distances

h = open('saxs_100.dat', 'w')
for f in glob("./lowE_100/*.pdb"):
	for m in get_minimums(f):
		h.write("%f\n"%m)
h.close()

h = open('saxs_40.dat', 'w')
for f in glob("./lowE_40/*.pdb"):
	for m in get_minimums(f):
		h.write("%f\n"%m)
h.close()

h = open('2BX9.dat', 'w')
for m in get_minimums('2BX9.pdb'):
	h.write("%f\n"%m)
h.close()

h = open('2ZP8.dat', 'w')
for m in get_minimums('2ZP8_bio.pdb'):
	h.write("%f\n"%m)
h.close()
