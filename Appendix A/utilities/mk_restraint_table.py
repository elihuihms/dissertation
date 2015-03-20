#!/usr/bin/env python

import argparse
import sys

from Bio.PDB.PDBParser import PDBParser

def readPDBAtoms(path,atom_names=[],quiet=False):
	parser=PDBParser(PERMISSIVE=True,QUIET=quiet)
	structure=parser.get_structure("temp", path )

	ret = []		
	for model in structure:
		for chain in model:
			for residue in chain:
				for atom in residue:
				
					if( len(atom_names)== 0):
						ret.append(atom)
					elif( atom.name in atom_names ):
						ret.append(atom) 
	return ret

def findNeighborAtoms(atoms,cutoff,quiet=False):

	n = len(atoms)	
	ret = [[]]*n
	
	if(not quiet):
		print "Linking PDB neighbors:"
	
	for i in range(0,n):
	
		if( not quiet) and (i % 100 == 0):
			print "%i / %i ATOMs linked" % (i,n)
	
		a1 = atoms[i]
		ret[i] = [a1]
		
		for j in range(i+1,n):
			a2 = atoms[j]
			
			if( a1-a2 < cutoff ):
				ret[i].append( a2 )
				
	return ret

def saveRestraintTable(neighbors,path,quiet=False):

	handle = open( path, 'w' )
	
	for i in range(len(neighbors)):
		a1 = neighbors[i][0]
		r1 = a1.get_parent()
		
		for j in range(1,len(neighbors[i])):
			a2 = neighbors[i][j]
			r2 = a2.get_parent()

			#Res_num	Res_name	Atom_name	Res_num2	Res_name2	Atom_name2	Distance
			handle.write( "%i\t%s\t%s\t%i\t%s\t%s\t%.3f\n" % (
				r1.get_id()[1],
				r1.get_resname(),
				a1.get_name(),
				r2.get_id()[1],
				r2.get_resname(),
				a2.get_name(),a1-a2)
			)
		
	handle.close()

if(__name__ == '__main__'):
	parser = argparse.ArgumentParser()
	parser.add_argument('-pdb', action='store', metavar='<PDB>', required=True, help='Coordinate file to parse')
	parser.add_argument('-out', action='store', metavar='<FILE>', required=True, help='Path to restraint table')
	parser.add_argument('-r', 	action='store', type=float, metavar='5.0', default=5.0, help='Inter-atomic cutoff distance for restraints')
	parser.add_argument('-atoms', 	nargs='*', metavar='C', default='', help='List of atom names to use. Omit to use all atoms.')
	parser.add_argument('-v', 	action='store_true', help='Enable verbose output.')
	args = parser.parse_args()
	
	print args.atoms
	
	atoms = readPDBAtoms( args.pdb, args.atoms, not args.v )
	neighbors = findNeighborAtoms( atoms, args.r )
	saveRestraintTable( neighbors, args.out )
	
	