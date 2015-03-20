#! /usr/bin/env python

# Based on code from Pierre Poulain, Justine Guegan, and Edithe Selwa
# last update: 20110414

import argparse
import numpy
import glob
import os
import sys

from Bio.PDB.PDBParser import PDBParser
from Bio.PDB.Atom import Atom

from pdb_lib import getAtomCoords,writeAtomToPDB

if (__name__=='__main__'):
	parser = argparse.ArgumentParser()
	parser.add_argument('-dir',		metavar='<DIR>',	required=True,	help='Directory containing pdb files')
	parser.add_argument('-out',		metavar='<FILE>',	required=True,	help='File to write collected center of mass points to')
	parser.add_argument('-model',	metavar='<N>',		type=int,	default=None,	help='Restrict to specified model')
	parser.add_argument('-chain',	metavar='<ID>',		default=None,	help='Restrict to specifed chain')
	parser.add_argument('-startRes',metavar='<N>',		type=int,	default=None,	help='Include residues starting with the specified ID')
	parser.add_argument('-endRes',	metavar='<N>',		type=int,	default=None,	help='Include residues up to and including specified ID')
	args = parser.parse_args()

	files = glob.glob("%s%s*.pdb" % (args.dir,os.sep) )
	files.sort()
	
	handle = open( args.out, 'w' )

	serial = 1
	for f in files:

		handle.write("REMARK %s\n" % f)

		# get all desired CA atom coordinates
		xyz = getAtomCoords( f,
			modelID = args.model,
			chainID = args.chain,
			startRes = args.startRes,
			endRes = args.endRes,
			CAonly=True )
	 
		#create coordinates array
		coord = numpy.array(xyz, float)
	 
		# compute geometric center
		center = numpy.mean(coord, 0)
	
		writeAtomToPDB( handle, serial, center[0], center[1], center[2], name='QA', residue='COM' ):		
		serial +=1
	
	handle.write("END\n")
	handle.close()
	
	
