#!/usr/bin/env python

import argparse

from DEERSimLib import *

parser = argparse.ArgumentParser()
parser.add_argument('-pdb',		metavar='<FILE>',	required=True,				help="PDB to extract N-O midpoints from")
parser.add_argument('-atoms',	action='append',	required=True,	nargs='*',	help='Chain name, residue number, atom names for N and O spin probe atoms: [[chainid] resnum] atom1 atom2')
parser.add_argument('-pseudo', 	metavar='QZ',		default='QZ',				help="Name of pseudo atom to write as N-O midpoints")
parser.add_argument('-out', 	metavar='<FILE>',	required=True,				help="File path to write the pseudo atoms to")
args = parser.parse_args()

# assemble atom specifiers
spec = []
for tmp in args.atoms:
	if( len(tmp) == 2):
		spec.append( (None,None,tmp[0],tmp[1]) )
	elif( len(tmp) == 3):
		spec.append( (None,int(tmp[0]),tmp[1],tmp[2]) )
	elif( len(tmp) == 4):
		spec.append( (tmp[0],int(tmp[1]),tmp[2],tmp[3]) )
	else:
		print "Mangled label specifier (%s). Check help via -h" % tmp
		exit()

f = open( args.out, 'w' )
for s in spec:
	
	coords_1 = getAtomCoords(args.pdb,chainID=s[0],resNum=s[1],atomName=s[2])
	coords_2 = getAtomCoords(args.pdb,chainID=s[0],resNum=s[1],atomName=s[3])
	
	if( len(coords_1) != len(coords_2) ):
		print "Found atom number mismatch: (%i of atom %s vs. %i of atom %s)" % (len(coords_1),s[2],len(coords_2,s[3]))
		exit()
	
	# build the atom dict prototype
	a = {
		'serial':0,
		'name':args.pseudo,
		'resname':"AVG",
		'chain':s[0],
		'resnum':s[1],
		'coords':[0,0,0],
		'occupancy':1.0,
		'bfactor':0.0,
		'segment':'    ',
		'element': ''
	}
	
	for (A,B) in zip(coords_1,coords_2):
		a['serial'] +=1
		a['coords'] = getAverage(A,B)
		writeAtomLine( f, a )
		
f.close()	