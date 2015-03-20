#!/usr/bin/env python

import os
import glob
import argparse

from DEERSimLib import *
from scipy import recfromtxt

# parser block
parser = argparse.ArgumentParser()
parser.add_argument('-dir', metavar="<DIR>", default=False, help="A directory containing PDBs with varying label positions...")
parser.add_argument('-mmm', metavar="<FILE>", default=False, nargs=2, help="...or 2 files in MMM pseudo-PDB format, labels are seriaized by residue number...")
parser.add_argument('-pdb', metavar="<FILE>", default=False, help="...or a single PDB with varying label positions.")
parser.add_argument('-label', metavar='', action='append', nargs='*', help='Label specifier. Format is [chainID] [resnum] atomname')
parser.add_argument('-resolution', metavar='1', type=float, default=1.0, help='The distribution precision (angstroms)')
parser.add_argument('-out', metavar='<FILE>', required=True, help="File path to write the distribution to")
args = parser.parse_args()

if (args.dir==None) and (args.pdb==None):
	print "Must specify either a directory of PDBs via -dir or a single pdb via -pdb"
	exit()

if(len(args.label) != 2):
	print "Must specify two label positions."
	exit()

# assemble label location specifier
spec = []
for l in args.label:

	 if( len(l) == 1):
	 	spec.append((None,None,l[0]))
	 elif( len(l) == 2):
	 	spec.append((None,int(l[0]),l[1]))
	 elif( len(l) == 3):
	 	spec.append((l[0],int(l[1]),l[2]))
	 else:
	 	print "Mangled label specifier. Check help via -h"
	 	exit()

# get list of coordinates for the label positions
if(args.pdb):

	coords_1 = getAtomCoords(args.pdb,chainID=spec[0][0],resNum=spec[0][1],atomName=spec[0][2])
	coords_2 = getAtomCoords(args.pdb,chainID=spec[1][0],resNum=spec[1][1],atomName=spec[1][2])

elif(args.mmm):

	coords_1 = getAtomCoords(args.mmm[0],atomName=spec[0][2])
	coords_2 = getAtomCoords(args.mmm[1],atomName=spec[0][2])

elif(args.dir):
	files = glob.glob("%s%s*.pdb" % (args.dir,os.sep))
	print "Found %i files to analyze." % len(files)

	coords_1,coords_2 = ([],[])
	for (i,f) in enumerate(files):
		print f

		tmp1 = getAtomCoords(f,chainID=spec[0][0],resNum=spec[0][1],atomName=spec[0][2])
		tmp2 = getAtomCoords(f,chainID=spec[1][0],resNum=spec[1][1],atomName=spec[1][2])

		if (len(tmp1)!=1) or (len(tmp2)!=1):
			print "Error on PDB \"%s\": Invalid label specification." % f
			exit()

		coords_1.append( tmp1[0] )
		coords_2.append( tmp2[0] )

else:
	print "Must specify a file or a directory to obtain label coordinates!"
	exit()

# histogram of distances
histogram = {}

for i in range( len(coords_1) ):
	for j in range( len(coords_2) ):
		# add the inter-label distance to the distribution
		r = getDistance(coords_1[i],coords_2[j])
		addToDistribution( histogram, r, args.resolution )

f = open( args.out, 'w' )

# normalization sum
sum = 0.0
tmp = 0.0
for n in histogram:
	sum += histogram[n]*args.resolution
	if(histogram[n]>tmp):
		tmp = histogram[n]

print ("\nHistogram:")

n = min(histogram.keys())
while( n <= max(histogram.keys()) ):

	# keys of the histogram are in units of resolution, so convert to distance
	r = args.resolution * n

	if( n in histogram ):
		print "%.3f\t%s" % (r,"#"*int(40*histogram[n]/tmp))
		f.write("%.3f\t%.3E\n" % (r,float(histogram[n])/sum))
	else:
		print "%.3f\t" % (r)
		f.write("%.3f\t%.3E\n" % (r,0))

	n+=1

f.close()