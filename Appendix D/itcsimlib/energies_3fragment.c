#include <string.h>

#include "itc_model.h"
#include "itc_sim.h"

int permute( int i, int n )
{
	if( i < 0 )
		return i + n;
	else if( i >= n )
		return i % n;
	else
		return i;
}

int checkFragment( int* config, int size, int index, char* fragment )
{
	int f = 1; //forward
	int b = 1; //backward (mirror image)
	int l = strlen(fragment);

	for(int i=0; i<l; i++)
	{
		if( (fragment[i]-'0') != config[ permute( index -(l/2) +i, size) ] )
			f = 0;
		if( (fragment[i]-'0') != config[ permute( index +(l/2) -i, size) ] )
			b = 0;
	}

	return f+b;
}

void assignEnergies( struct mWorkspace *w, struct sWorkspace *sim,
					char*	Sa, char*	Sb, char*	Sc,
					double	Ga, double	Gb, double	Gc,
					double	Ha, double	Hb, double	Hc )
{

	/* assign energies for each configuration */
	for(int i=0; i<pow(2, w->size); i++)
	{
		w->energies[i]=0;
		sim->enthalpies[i]=0;

		for(int j=0; j<w->size; j++)
		{
			if( w->configs[i][j] > 0 )
			{
				if( checkFragment( w->configs[i], w->size, j, Sa) > 0 ){
					w->energies[i]			+= Ga;
					sim->enthalpies[i]		+= Ha;
				}

				if( checkFragment( w->configs[i], w->size, j, Sb) > 0 ){
					w->energies[i]			+= Gb;
					sim->enthalpies[i]		+= Hb;
				}

				if( checkFragment( w->configs[i], w->size, j, Sc) > 0 ){
					w->energies[i]			+= Gc;
					sim->enthalpies[i]		+= Hc;
				}
			}
		}
	}

	return;
}
