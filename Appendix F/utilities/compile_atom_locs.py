#!/usr/bin/env python

import sys
import glob
import os
import numpy
import argparse

from pdb_lib import getAtomCoords,writeAtomToPDB

if(__name__ == '__main__'):

	parser = argparse.ArgumentParser()
	parser.add_argument('-dir',		metavar='<DIR>',	required=True,	help='Directory containing PDB files')
	parser.add_argument('-atom',	metavar='', nargs=3,required=True,	help='Residues specifying an atom: <chain> <residue> <atom>')
	parser.add_argument('-out',		metavar='<FILE>',	required=True,	help='File to save axis atoms to')
	args = parser.parse_args()

	# get the pdbs to put into the table
	path = "%s%s*.pdb" % (args.dir,os.sep)

	handle = open( args.out, 'w' )

	serial = 1
	for f in glob.glob( path ):
		name = os.path.basename(f)
		print name

		(c,r,a) = args.atom
		xyz = getAtomCoords(f, chainID=c, startRes=int(r), endRes=int(r), atomName=a)[0]

		if(len(xyz) == 0):
			print "No atoms found in chain \"%s\", %i:%i" % (c,s,e)
			exit()

		writeAtomToPDB( handle, serial, xyz[0],xyz[1],xyz[2], name=a, residue='COM' )
		serial+=1

	handle.write("END\n")
	handle.close()

