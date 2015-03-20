#!/usr/bin/python

import sys

#
# Script to thin MESMER input files
# This is achieved by iterating over a file containing descriptive parameters (Rg, average interprotomer distance, etc.) and randomly selecting only a single representative of the group that has all such parameters within a given percentage
#

# parameters table creation
#tread -col 0 pdb_dist_QA.tbl > compiled.tbl
#tread -col 1 pdb_mw.tbl | twrite -col 1 compiled.tbl
#tread -col 1 pdb_rg.tbl | twrite -col 2 compiled.tbl
#tread -col 1 pdb_dmax.tbl | twrite -col 3 compiled.tbl
#tread -col 3 pdb_dist_QT.tbl | twrite -col 4 compiled.tbl
#tread -col 3 pdb_dist_QA.tbl | twrite -col 5 compiled.tbl
#tread -col 4 pdb_dist_QTQA.tbl | twrite -col 6 compiled.tbl

# parameters table path
param_table = sys.argv[1]

# uniqueness percentage
cutoff = 0.05

# file to contain unique representatives
output_file = 'unique.tbl'

#
# Done with options
#

import sys
import random

from scipy import recfromtxt

pdbs = list(recfromtxt( param_table ))

def PDBs_similar( cutoff, pdb1, pdb2 ):
	
	for i in range(1,len(pdb1)):
		avg = (pdb1[i]+pdb2[i])/2
		
		if (pdb1[i] > avg+(avg*cutoff)) or (pdb1[i] < avg-(avg*cutoff)):
			return False
	
	return True
pass

file = open( output_file, 'w' )

for i in range(len(pdbs)):
	
	if (pdbs[i] == None):
		continue
	
	group = [pdbs[i][0]]
	for j in range(i+1,len(pdbs)):
		
		if (pdbs[j] == None):
			continue
			
		if PDBs_similar(cutoff,pdbs[i],pdbs[j]):
			group.append(pdbs[j][0])
			pdbs[j] = None

	if(len(group)>0):
		for pdb in group:
			print "%s\t" % (pdb),
		print ""
		sys.stdout.flush()
	
	file.write( "%s\n" % (random.choice(group)) )

file.close()
