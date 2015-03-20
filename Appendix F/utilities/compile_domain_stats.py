#!/usr/bin/env python

import sys
import glob
import os
import numpy
import argparse

from pdb_lib import *

parser = argparse.ArgumentParser()
parser.add_argument('-dir',		metavar='<DIR>',	required=True,	help='Directory containing PDB files')
parser.add_argument('-domain',	metavar='', action='append',	nargs='+',		help='Residues specifying a domain: [<chain>] <start res> <end res>')
parser.add_argument('-out',		metavar='<FILE>',	default='domain_stats.tbl',	help='File to save statistics to')
args = parser.parse_args()

if( len(args.domain) != 2 ):
	print "Specify two domains via -domain"
	exit()

# convert domain residues to integers
for i in range(2):
	if(len(args.domain[i]) == 2):
		args.domain[i] = (None,int(args.domain[i][0]),int(args.domain[i][1]))
	elif(len(args.domain[i]) == 3 ):
		args.domain[i] = (args.domain[i][0],int(args.domain[i][1]),int(args.domain[i][2]))
	else:
		print "-domain takes two or three arguments"
		exit()

# get the pdbs to put into the table
files = sorted( glob.glob("%s%s*.pdb" % (args.dir,os.sep)) )

handle = open( args.out, 'w' )
handle.write("#pdb\tr\tdot1\tdot2\tdot3\n")
for f in files:
	print f

	A = getAtomCoords( f,
		chainID = args.domain[0][0],
		startRes = args.domain[0][1],
		endRes = args.domain[0][2])
	B = getAtomCoords( f,
		chainID = args.domain[1][0],
		startRes = args.domain[1][1],
		endRes = args.domain[1][2])

	A_CoM = getCenter( A )
	B_CoM = getCenter( B )

	if (len(A)<4) and (len(B)<4) :
		handle.write( "%s\t%.3f\n" % (os.path.basename(f),getDistance(A_CoM,B_CoM)) )
		continue

	(A1,A2,A3) = getPrincipleAxes( A )
	(B1,B2,B3) = getPrincipleAxes( B )

	r = numpy.linalg.norm(A_CoM - B_CoM)
	dot1 = numpy.dot(A1,B1)
	dot2 = numpy.dot(A2,B2)
	dot3 = numpy.dot(A3,B3)

	handle.write( "%s\t%.3f\t%.3f\t%.3f\t%.3f\n" % (os.path.basename(f),r,dot1,dot2,dot3) )

handle.close()

