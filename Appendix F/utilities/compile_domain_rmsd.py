#!/usr/bin/env python

import sys
import glob
import os
import numpy
import argparse

from pdb_lib import *

parser = argparse.ArgumentParser()
parser.add_argument('-pdb',		metavar='<PDB>',	required=True,	help='Parent PDB to calculate RMSDs to')
parser.add_argument('-dir',		metavar='<DIR>',	required=True,	help='Directory containing PDB files')
parser.add_argument('-domain',	metavar='', action='append',	nargs='*',		help='Residues specifying a domain: [<chain>] <start res> <end res>')
parser.add_argument('-out',		metavar='<FILE>',	default='domain_rmsds.tbl',	help='File to save RMSD values in')
args = parser.parse_args()

if(not args.domain):
	print "Must specify at least one domain."
	exit()

# convert domain residues to integers
for i in range(len(args.domain)):
	if(len(args.domain[i]) == 2):
		args.domain[i] = (None,int(args.domain[i][0]),int(args.domain[i][1]))
	elif(len(args.domain[i]) == 3 ):
		args.domain[i] = (args.domain[i][0],int(args.domain[i][1]),int(args.domain[i][2]))
	else:
		print "-domain takes two or three arguments"
		exit()

parent_xyz = [None]*len(args.domain)
for i in range(len(args.domain)):
	parent_xyz[i] = getAtomCoords( args.pdb,
		chainID = args.domain[i][0],
		startRes = args.domain[i][1],
		endRes = args.domain[i][2])

# get the pdbs to put into the table
files = sorted( glob.glob("%s%s*.pdb" % (args.dir,os.sep)) )

rmsds=['rmsd']*len(args.domain)

handle = open( args.out, 'w' )
handle.write("#pdb\t%s\n" % "\t".join(rmsds) )
for f in files:
	print f

	for i in range(len(args.domain)):
		xyz = getAtomCoords( f,
			chainID = args.domain[i][0],
			startRes = args.domain[i][1],
			endRes = args.domain[i][2])
		rmsds[i] = "%.3f" % getRMSD(parent_xyz[i],xyz)

	handle.write("%s\t%s\n" % (os.path.basename(f),"\t".join(rmsds)) )

handle.close()

