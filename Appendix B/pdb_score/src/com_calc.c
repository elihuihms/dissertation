#include <stdio.h>
#include <string.h>
#include <math.h>

#include "pdb.c"

/*

Returns the center of mass of a protein

Author: Elihu Ihms

Last modified: 2012.01.04

*/

#define PDB_SIZE 50000

int main(int argc, char *argv[])
{
	int		i,nAtoms;
	
	double	sum, center[3] = {0,0,0};
	double	pdb[ PDB_SIZE ][3];
	
	
	/* do some basic argument checking */
	if (argc < 2)
	{
		printf("Usage: com_calc 'file.pdb'\n");
		return 0;
	}
	
	nAtoms = getPDBAtomCoords( argv[1], pdb, PDB_SIZE );
	if (nAtoms < 0){
		printf("Error reading PDB '%s'.\n", argv[1]);
		return 0;
	}
	
	/* calculate the center of mass of the protein, assuming all atoms have equal mass */
	for( i=0; i<nAtoms; i++)
	{
		center[0] += pdb[i][0];
		center[1] += pdb[i][1];
		center[2] += pdb[i][2];
	}
	
	for( i=0; i<3; i++)
		center[i] = center[i] / nAtoms;
	
	printf("%s\t%f\t%f\t%f\n", argv[1], center[0],center[1],center[2] );
		
	return 0;
}

