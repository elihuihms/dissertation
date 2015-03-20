#include <stdio.h>
#include <string.h>
#include <math.h>

#include "pdb.c"

/*

Returns the radius of gyration for a protein (standard deviation of atom distances from the center of mass)

Author: Elihu Ihms

Last modified: 2012.1.04

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
		printf("Usage: rg_calc 'file.pdb'\n");
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

	/* start calculating the standard deviation
	Rg = stddev = sqrt( (1/n) * sum( D_i ) )
	
	D_i = distance from center for atom i
	n = # atoms
	*/
	
	for( i=0; i<nAtoms; i++)
		sum += pow( getDistance( pdb[i], center ), 2);
	
	printf("%s\t%f\n", argv[1], sqrt( sum / nAtoms ));
		
	return 0;
}

