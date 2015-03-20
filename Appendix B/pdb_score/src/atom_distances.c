#include <stdio.h>
#include <string.h>
#include <math.h>

#include "pdb.c"

/*

Returns a tab-delimited table of distances between two provided atom names

Author: Elihu Ihms

Last modified: 2012.08.20

*/

#define PDB_SIZE 50000

int main(int argc, char *argv[])
{
	FILE	*pHandle;
	char	string[5], atom1[5], atom2[5], line[60];
	int		nAtoms1, nAtoms2,i,j;
	double	dist;
	
	double	pdb1[ PDB_SIZE ][3];
	double	pdb2[ PDB_SIZE ][3];
	
	/* do some basic argument checking */
	if (argc < 4)
	{
		printf("Usage: pdb_dist 'atomname1' 'atomname2' 'file.pdb'\n");
		return 0;
	}
	if ((strlen(argv[1]) > 4) || (strlen(argv[1]) < 1))
	{
		printf("First atomname must be 1-4 characters long.\n");
		return 0;
	}
	if ((strlen(argv[2]) > 4) || (strlen(argv[2]) < 1))
	{
		printf("Second atomname must be 1-4 characters long.\n");
		return 0;
	}
		
	nAtoms1 = getNamedPDBAtomCoords( argv[3], argv[1], pdb1, PDB_SIZE );
	if (nAtoms1 < 0){
		printf("Error reading PDB '%s'.\n", argv[3]);
		return 0;
	}
	nAtoms2 = getNamedPDBAtomCoords( argv[3], argv[2], pdb2, PDB_SIZE );
	if (nAtoms2 < 0){
		printf("Error reading PDB '%s'.\n", argv[3]);
		return 0;
	}

	for( i=0; i<nAtoms1; i++){
		for ( j=0; j<nAtoms2; j++){
			
			dist = getDistance( pdb1[i], pdb2[j] );
			printf("%s\t%s\t%i\t%i\t%f\n", argv[1],argv[2],i,j,dist);
		}
	}	
		
	return 0;
}

