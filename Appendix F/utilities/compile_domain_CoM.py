#!/usr/bin/env python

import sys
import glob
import os
import numpy
import argparse

from pdb_lib import *

parser = argparse.ArgumentParser()
parser.add_argument('-dir',		metavar='<DIR>',	required=True,	help='Directory containing PDB files')
parser.add_argument('-domain',	metavar='', action='append',	nargs='*',		help='Residues specifying a domain: [<chain>] <start res> <end res>')
parser.add_argument('-out',		metavar='<FILE>',	default='domain_CoMs.pdb',	help='File to save CoM atoms to')
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

# get the pdbs to put into the table
files = sorted( glob.glob("%s%s*.pdb" % (args.dir,os.sep)) )

chainIDs=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

serial = 1
handle = open( args.out, 'w' )
for f in files:
	print f

	for (c,s,e) in args.domain:

		xyz = getAtomCoords(f,
				chainID=c,
				startRes=s,
				endRes=e)

		if(len(xyz) == 0):
			print "No atoms found in chain \"%s\", %i:%i" % (c,s,e)
			exit()

		CoM = getCenter( xyz )
		writeAtomToPDB( handle, serial, CoM[0], CoM[1], CoM[2], 'CA', residue='', segid=c )
		serial += 1

handle.close()

