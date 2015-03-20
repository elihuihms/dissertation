#include <stdio.h>
#include <string.h>
#include <math.h>

#include "pdb.c"

/*

Returns the number of interatomic C, CA, or N distances that are less than a provided cutoff

Author: Elihu Ihms

Last modified: 2012.01.13

*/

#define PDB_SIZE 500000

int main(int argc, char *argv[])
{
	FILE	*pHandle;
	char	string[5], line[60];
	int		nAtoms,i,j,clash;
	double	dist;
	
	char	names[ PDB_SIZE ][5];
	double	pdb[ PDB_SIZE ][3];
	
	/* do some basic argument checking */
	if (argc < 3)
	{
		printf("Usage: clash_count <dist> 'file.pdb'\n");
		return 0;
	}
	
	dist = atof( argv[1] );
	clash = 0;
	
	nAtoms = getPDBNamesAndCoords( argv[2], names, pdb, PDB_SIZE );
	if (nAtoms < 0){
		printf("Error reading PDB '%s'.\n", argv[2]);
		return 0;
	}

	for( i=0; i<nAtoms; i++){
		if ( \
		((strncmp( "C", names[ i ], 1) == 0) || \
		(strncmp( "CA", names[ i ], 2) == 0)) || \
		(strncmp( "N", names[ i ], 1) == 0) )
		{
		
			for ( j=i+1; j<nAtoms; j++){
				if ( \
				((strncmp( "C", names[ j ], 1) == 0) || \
				(strncmp( "CA", names[ j ], 2) == 0)) || \
				(strncmp( "N", names[ j ], 1) == 0) )
				{
			
					if( getDistance( pdb[i], pdb[j] ) < dist )
						clash++;
				}
			}
		}
	}
	
	printf("%s\t%.3f\t%i\n", argv[2], dist, clash);
	
	
	
	return 0;
}

