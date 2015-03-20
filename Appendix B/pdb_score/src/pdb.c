#ifndef _stdlib_h_
#include <stdlib.h>
#endif

#ifndef _pdb_h_
#include "pdb.h"
#endif

#include "misc.c"

/*

Some very basic PDB parsing functions

Author: E. Ihms

*/

int getPDBAtomCoords( char* file, double pos[][3], int max )
{
	FILE *pHandle;
	char string[10], line[60];
	int nAtoms=0;

	pHandle = fopen( file, "r");
	
	if (pHandle == NULL)
		return -1;

	while( fgets(line, sizeof(line), pHandle) != NULL )
	{	
		if (strncmp( "ATOM", line, 4) == 0)
		{
			substr( string, line, 30, 8);
			pos[nAtoms][0] = atof( string );

			substr( string, line, 38, 8);
			pos[nAtoms][1] = atof( string );

			substr( string, line, 46, 8);
			pos[nAtoms][2] = atof( string );				
			nAtoms++;
		}
		
		if(nAtoms > max)
			return -2;
	}
	
	return nAtoms;
}

int getNamedPDBAtomCoords( char* file, char* name, double pos[][3], int max )
{
	FILE *pHandle;
	char string[10], line[60];
	int nAtoms=0;

	trim( name );

	pHandle = fopen( file, "r");
	
	if (pHandle == NULL)
		return -1;

	while( fgets(line, sizeof(line), pHandle) != NULL )
	{
		strncpy( string, line+12, 4 );
		string[4] = 0;
		trim( string );
		
		if ((strncmp("ATOM", line, 4) == 0) && (strcmp(name, string) == 0))
		{
			substr( string, line, 30, 8);
			pos[nAtoms][0] = atof( string );

			substr( string, line, 38, 8);
			pos[nAtoms][1] = atof( string );

			substr( string, line, 46, 8);
			pos[nAtoms][2] = atof( string );
						
			nAtoms++;
		}
		
		if (nAtoms > max)
			return -2;
	}
	
	return nAtoms;
}

int getPDBNamesAndCoords( char* file, char names[][5], double pos[][3], int max )
{
	FILE *pHandle;
	char string[10], line[60];
	int nAtoms=0;

	pHandle = fopen( file, "r");
	
	if (pHandle == NULL)
		return -1;

	while( fgets(line, sizeof(line), pHandle) != NULL )
	{	
		if ( (strncmp( "ATOM", line, 4) == 0) || (strncmp( "HETATM", line, 6) == 0) )
		{
			// slice out the name of the atom
			strncpy( string, line+12, 4 );
			
			// if the name is well formed, add it to the list
			if (trim( string ) > 0)
			{
				strcpy( names[nAtoms], string);
			
				substr( string, line, 30, 8);
				pos[nAtoms][0] = atof( string );
	
				substr( string, line, 38, 8);
				pos[nAtoms][1] = atof( string );
	
				substr( string, line, 46, 8);
				pos[nAtoms][2] = atof( string );				
				nAtoms++;
			}
		}
		
		if(nAtoms > max)
			return -2;
	}
	
	return nAtoms;
}

double **mallocCoords(int m)
{
	int i;
	double **p;
	
	p = (double **) malloc( m * sizeof(double *) );
	
	if (p == NULL){
		printf( "Ran out of memory!" );
		return NULL;
	}
	
	for( i=0; i < m; i++ ){
		p[i] = (double *) malloc( 3 * sizeof(double) );
		if (p[i] == NULL){
			printf( "Ran out of memory!" );
			return NULL;
		}
	}
	
	return p;
}

double getDistance( double* coord1, double* coord2 )
{
	return sqrt( pow(coord1[0] - coord2[0],2.0) + pow(coord1[1] - coord2[1],2.0) + pow(coord1[2] - coord2[2],2.0) );	
}
