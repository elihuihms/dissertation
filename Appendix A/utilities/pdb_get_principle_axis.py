#!/usr/bin/env python

# last update: 20140812

import argparse
import numpy

from Bio.PDB.PDBParser import PDBParser
from Bio.PDB.Atom import Atom

from pdb_lib import getAtomCoords, getPrincipleAxes, writeAxisToPDB

if (__name__=='__main__'):
	parser = argparse.ArgumentParser()
	parser.add_argument('-pdb',		metavar='<PDB>',	required=True,	help='PDB file to parse')
#	parser.add_argument('-CA',		action='store_true',default=True,	help='Use only CA atoms.')
	parser.add_argument('-model',	metavar='<N>',		type=int,	default=None,	help='Restrict to specified model')
	parser.add_argument('-chain',	metavar='<ID>',		default=None,	help='Restrict to specifed chain')
	parser.add_argument('-startRes',metavar='<N>',		type=int,	default=None,	help='Include residues starting with the specified ID')
	parser.add_argument('-endRes',	metavar='<N>',		type=int,	default=None,	help='Include residues up to and including specified ID')
	parser.add_argument('-out',		metavar='<FILE>',	default=None,	help='Write principle axis atoms to <FILE> instead of original PDB file.')
	parser.add_argument('-unit',	action='store_true',default=False,	help='Normalize principle axes to unit vectors.')
	args = parser.parse_args()

	xyz = getAtomCoords( args.pdb,
		modelID = args.model,
		chainID = args.chain,
		startRes = args.startRes,
		endRes = args.endRes
		)

	(axis1,axis2,axis3) = getPrincipleAxes( xyz )

	center = numpy.mean(xyz, 0)

	if(args.unit):
		scale = (1.0,1.0,1.0)
	else:
		scale = (20.0,10.0,5.0)

	serial = 0
	if( args.out != None ):
		handle = open( args.out, 'w' )
		writeAxisToPDB( handle, center, axis1*scale[0], axis2*scale[1], axis3*scale[2], 1, 'A' )
		handle.write("END\n")
		handle.close()

		exit()

	else:
		handle = open( args.pdb, 'r+' )

		atoms = []
		atoms.append( ('QA',center) )
		atoms.append( ('QX',(axis1*scale[0]) + center) )
		atoms.append( ('QY',(axis2*scale[1]) + center) )
		atoms.append( ('QZ',(axis3*scale[2]) + center) )

		line = handle.readline()
		prev = handle.tell()
		while (line != ''):

			if( line[0:3] == 'END' ):
				handle.seek(prev)
				handle.write("TER\n")
				break

			if (line[0:7] == 'ATOM  ') or (line[0:7] == 'HETATOM'):
				serial = int(line[7:12])

			prev = handle.tell()
			line = handle.readline()

	serial += 1
	residue = 'AXI'
	seqid = 999
	segid = ''
	for (name,coord) in atoms:

		x = "%.3f" % coord[0]
		y = "%.3f" % coord[1]
		z = "%.3f" % coord[2]
		o = "%.2f" % 1
		b = "%.2f" % 0

		handle.write( 'ATOM'.ljust(6) )
		handle.write( "%5d" % serial )
		handle.write( "%1s" % " " )
		handle.write( name.center(4) )
		handle.write( "%1s" % " " )
		handle.write( "%3s" % residue )
		handle.write( "%1s" % " " )
		handle.write( "%1s" % " " )
		handle.write( "%4s" % seqid )
		handle.write( "%1s" % " " )
		handle.write( "%3s" % "   " )
		handle.write( x.rjust(8) )
		handle.write( y.rjust(8) )
		handle.write( z.rjust(8) )
		handle.write( o.rjust(6) )
		handle.write( b.rjust(6) )
		handle.write( "%6s" % "      " )
		handle.write( "%4s\n" % segid )

		serial +=1

	handle.write("END\n")
	handle.close()

