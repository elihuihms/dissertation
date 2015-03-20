#!/usr/bin/env python

import argparse
import numpy

from pdb_lib import parseAtomLine,writeAtomLine,rmsd,kabsch

def getAtomCoords(arr,atomName=None,chainID=None,startRes=0,endRes=99999):
	# uses an array instead of reading from a file like the normal pdb_lib gAC
	ret = []
	for line in arr:
		a = parseAtomLine(line)
		if(a):
			if (a['chain']==chainID) or (chainID==None):
				if (a['resnum']>=startRes) and (a['resnum']<=endRes):
					if (a['name'] == atomName) or (atomName==None):
						ret.append( a['coords'] )

	return ret

def getResidueNums( arr, chainID=None ):

	start = None
	for line in arr:
		a = parseAtomLine(line)
		if(a):
			if (a['chain']==chainID) or (chainID==None):
				if(start==None):
					start = a['resnum']
				end = a['resnum']

	return (start,end)

if (__name__=='__main__'):
	parser = argparse.ArgumentParser()
	parser.add_argument('-pdb',		metavar='<PDB>',	required=True,				help='Parent PDB file')
	parser.add_argument('-domain',	action='append',	metavar='<PDB>',			help='PDBs of domains present in parent PDB file')
	parser.add_argument('-out',		metavar='<FILE>',	required=True,				help='Path to PDB to save the aligned domains')
	args = parser.parse_args()

	# read parent atom records
	f = open( args.pdb, 'r' )
	parent = f.readlines()
	f.close()

	serial=1
	out = open( args.out, 'w' )
	for d in args.domain:

		# get the chain ID, start and end residues for the domain
		f = open( d, 'r' )
		domain = f.readlines()
		f.close()

		# scan the PDB till a valid ATOM with chain is encountered
		for i in range(len(domain)):
			a = parseAtomLine( domain[i] )
			if( a != None ):
				break
		if(a==None):
			print "Error: could not find a valid chain in the domain %s" % (d)

		(start,end) = getResidueNums( domain, a['chain'] )

		# get the domain CA coordinates
		domain_coords = getAtomCoords(domain, 'CA', a['chain'], start, end )

		# get the corresponding parent CA coordinates
		parent_coords = getAtomCoords(parent, 'CA', a['chain'], start, end)

		if( len(domain_coords) != len(parent_coords) ):
			print "Error:"
			print "Found %i CA records for parent %s using %s %i:%i" % (len(parent_coords),args.pdb,a['chain'],start,end)
			print "Found %i CA records for domain %s using %s %i:%i" % (len(domain_coords),d,a['chain'],start,end)
			exit()

		# obtain the centers of mass and the transformation matrix
		(Da,Pa,M) = kabsch( domain_coords, parent_coords )

		# write the transformed domain atoms
		for l in domain:
			a = parseAtomLine(l)
			if(a):
				a['coords'] = numpy.dot( a['coords']-Da, M )+Pa
				writeAtomLine(out,a)
				serial+=1

	out.close()












