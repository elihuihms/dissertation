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

void assignEnergies( struct mWorkspace* w, struct sWorkspace* sim, int n_params, int exclusive, char** fragments, double* params )
{
	int i,j,k; //counter vars
	int assigned; // boolean flag to set if we've assigned an energy to

	/* assign energies for each configuration */
	for(i=0; i<pow(2, w->size); i++)
	{
		w->energies[i] = 0;
		sim->enthalpies[i] = 0;

		/* iterate through each position in the ring */
		for(j=0; j<w->size; j++)
		{
			/* if this site is occupied, continue */
			if( w->configs[i][j] > 0 )
			{

				/* look for a fragment to apply dG, dH */
				for (k=0; k<n_params; k++)
				{
					if( checkFragment( w->configs[i], w->size, j, fragments[k] ) > 0 )
					{
						w->energies[i]		+= params[k];				//dG
						sim->enthalpies[i]	+= params[k +n_params];		//dH

						/* if we've assigned an energy for this position, break */
						if( exclusive > 0 )
							break;

					}
				}
			}
		}
	}

	return;
}
