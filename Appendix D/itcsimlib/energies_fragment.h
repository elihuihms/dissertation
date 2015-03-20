#ifndef _itc_energies_
#define _itc_energies_

int permute( int i, int n );
int checkFragment( int* config, int size, int index, char* fragment );
void assignEnergies( struct mWorkspace* w, struct sWorkspace* sim, int n_params, int exclusive, char** fragments, double* params );

#endif