#include <stdio.h>
#include <string.h>
#include <math.h>

#include "pdb.c"

/*

Returns the minimum, average, and maximum distances from a pdb, provided the atom name (including spaces!)

Author: Elihu Ihms

Last modified: 2012.01.13

*/

#define PDB_SIZE 50000

int main(int argc, char *argv[])
{
	FILE	*pHandle;
	char	string[5], atom[5], line[60];
	int		nAtoms,i,j,nDist;
	double	dist,avg,max,min;
	
	double	pdb[ PDB_SIZE ][3];
	
	/* do some basic argument checking */
	if (argc < 3)
	{
		printf("Usage: pdb_dist 'atomname' 'file.pdb'\n");
		return 0;
	}
	if ((strlen(argv[1]) > 4) || (strlen(argv[1]) < 1))
	{
		printf("Atomname must be 1-4 characters long.\n");
		return 0;
	}
	
	nAtoms = getNamedPDBAtomCoords( argv[2], argv[1], pdb, PDB_SIZE );
	if (nAtoms == -1){
		printf("Error reading PDB '%s'.\n", argv[2]);
		return 0;
	}
	else if(nAtoms == -1){
		printf("Error reading PDB '%s' - too many (>50000) matching ATOMs.\n", argv[2]);
		return 0;
	}

	avg = 0;
	max = 0;
	min = 1000;
	nDist = 0;

	for( i=0; i<nAtoms; i++)
	{
		for ( j=i+1; j<nAtoms; j++)
		{
			dist = getDistance( pdb[i], pdb[j] );

			avg+=dist;
			if (dist > max)
				max = dist;
			if (dist < min)
				min = dist;
				
			nDist++;
		}
	}
	
	avg = avg / nDist;
	
	printf("%s\t%i\t%f\t%f\t%f\n", argv[2],nAtoms,min,avg,max);
		
	return 0;
}

