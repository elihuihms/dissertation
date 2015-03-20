#!/usr/bin/python2.6

#
# This program iterates over a set of passed files and removes all entries that have an RMSD for ALL marker atoms less than the cutoff distance.
#
# Based on a protein superposition script by Peter Cock, his original info is reproduced below:

# Copyright 2007 Peter Cock, all rights reserved.
# Licenced under the GPL v2 (or later at your choice)
#
# Please see this website for details:
# http://www.warwick.ac.uk/go/peter_cock/python/protein_superposition/
#

import sys
import Bio.PDB
from Bio.PDB import Selection
import numpy
from sys import argv,exit

if (len(argv) < 2):
	print "Usage: uniquify_CA <*pdb>"
	exit(0)
	
pdb_files = argv[1:]

for i in range( len(pdb_files) ):

	ref_file = pdb_files[ i ]
	ref_structure = Bio.PDB.PDBParser(PERMISSIVE=True, QUIET=True).get_structure('ref', ref_file)
	
	ref_atoms = []
	all_atoms = Selection.unfold_entities(ref_structure,'A')
	for a in all_atoms:
		if( a.name == 'CA' ):
			ref_atoms.append( a )
	
	for j in range( i+1, len(pdb_files) ):
	
		chk_file = pdb_files[ j ]
		chk_structure = Bio.PDB.PDBParser(PERMISSIVE=True, QUIET=True).get_structure('chk', chk_file)
		
		chk_atoms = []
		all_atoms = Selection.unfold_entities(chk_structure,'A')
		for a in all_atoms:
			if( a.name == 'CA' ):
				chk_atoms.append( a )

		if( len(ref_atoms) == len(chk_atoms) ):	
			superimposer = Bio.PDB.Superimposer()
			superimposer.set_atoms( ref_atoms, chk_atoms )
			print "RMS (%s vs. %s): %0.2f" % (ref_file,chk_file, superimposer.rms)
		else:
			break
