#ifndef _itc_energies_
#define _itc_energies_

int permute( int i, int n );
int checkFragment( int* config, int size, int index, char* fragment );

void assignEnergies(
						 struct mWorkspace *w,
						 struct sWorkspace *sim,
						 char*	Sa,	char*	Sb, char*	Sc,
						 double	Ga, double	Gb, double	Gc,
						 double	Ha, double	Hb, double	Hc);

#endif