#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

#include "pdb.c"
#include "rmsd.c"

/*

Calculates the RMSD between selected types of atoms in two PDBs

Author: E. Ihms

Last modified: 2012.01.13

*/

#define POS_SIZE 5000

int main(int argc, char *argv[])
{
	int	i,nAtoms1,nAtoms2;
	double rmsd;
	double pdb1[ POS_SIZE ][3], pdb2[ POS_SIZE ][3];
		
	/* do some basic argument checking */
	if (argc < 3){
		printf("Usage: rmsd_calc 'atom' file1.pdb file2.pdb\n");
		return 0;
	}
	
	/* read the two pdb files */
	nAtoms1 = getNamedPDBAtomCoords( argv[2], argv[1], pdb1, POS_SIZE );	
	if (nAtoms1 == -1){
		printf("Error reading file '%s'\n", argv[2]);
		return 0;
	}else if (nAtoms1 == -2){
		printf("File '%s' exceeds %i atoms named '%s'.\n", argv[2], POS_SIZE, argv[1]);
		return 0;
	}
	nAtoms2 = getNamedPDBAtomCoords( argv[3], argv[1], pdb2, POS_SIZE);
	if (nAtoms2 == -1){
		printf("Error reading file '%s'\n", argv[3]);
		return 0;
	}else if (nAtoms2 == -2){
		printf("File '%s' exceeds %i atoms named '%s'.\n", argv[2], POS_SIZE, argv[1]);
		return 0;
	}
	
	if (nAtoms1 != nAtoms2){
		printf("Atom number mismatch. Found %i matching atoms in first PDB, and %i in the second.\n", nAtoms1, nAtoms2);
		return 0;
	}
	if (nAtoms1 == 0){
		printf("Did not match any atoms with the provided name.\n", nAtoms1, nAtoms2);
		return 0;
	}
		
	/* calculate the RMSD */
	fast_rmsd( pdb1, pdb2, nAtoms1, &rmsd);
	
	if ( isnan(rmsd) )
		printf("%s\t%s\tNaN\n", argv[2], argv[3]);
	else
		printf("%s\t%s\t%f\n", argv[2], argv[3], rmsd);
		
	return 0;
}

