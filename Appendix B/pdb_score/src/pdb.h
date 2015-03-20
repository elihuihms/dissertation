#ifndef _pdb_h_
#define _pdb_h_

/*
	malloc's memory for an array of cartesian coordinates of specified size
*/
double **mallocCoords( int m );

/*
	Provides all ATOM cartesian coordinates from a pdb file
	returns the number of atoms on success, -1 on file read failure, and -2 on exceeding max number of atoms
*/
int getPDBAtomCoords( char* file, double pos[][3], int max );

/*
	Given an exact name of four characters (including spaces!), provides all matching ATOM cartesian coordinates from a pdb file
	returns the number of matching atoms on success, -1 on file read failure, and -2 on exceeding max number of atoms
*/
int getNamedPDBAtomCoords( char* file, char* name, double pos[][3], int max );

/*
	gets all ATOM and HETATM records, along with their names
*/
int getPDBNamesAndCoords( char* file, char names[][5], double pos[][3], int max );

/*
	returns the euclidian distance between two cartesian coordinates
*/
double getDistance( double* coord1, double* coord2 );



#endif