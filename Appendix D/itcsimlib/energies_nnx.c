

#include "itc_model.h"
#include "itc_sim.h"

int permute( int i, int n );
int permute( int i, int n )
{
	if( i < 0 )
		return i + n;
	else if( i >= n )
		return i % n;
	else
		return i;
}

void assignEnergies( struct mWorkspace *w, struct sWorkspace *sim,
					double Ga, double Gb, double Gc,
					double Ha, double Hb, double Hc )
{
	/*

	Configurations:
	010				(a)
	011 or 110		(b)
	111				(c)
	*/

	/* assign energies for each configuration */
	for(int i=0; i<pow(2, w->size); i++)
	{
		w->energies[i]=0;
		sim->enthalpies[i]=0;

		for(int j=0; j<w->size; j++)
		{
			if( w->configs[i][j] > 0 )
			{
				if( (w->configs[i][ permute(j-1,w->size) ] == 0) && (w->configs[i][ permute(j+1,w->size) ] == 0) ){
					w->energies[i]		+= Ga; /* 010 */
					sim->enthalpies[i]	+= Ha;
				}else if( (w->configs[i][ permute(j-1,w->size) ] == 1) && (w->configs[i][ permute(j+1,w->size) ] == 0) ){
					w->energies[i]		+= Gb; /* 110 */
					sim->enthalpies[i]	+= Hb;
				}else if( (w->configs[i][ permute(j-1,w->size) ] == 0) && (w->configs[i][ permute(j+1,w->size) ] == 1) ){
					w->energies[i]		+= Gb; /* 011 */
					sim->enthalpies[i]	+= Hb;
				}else if( (w->configs[i][ permute(j-1,w->size) ] == 1) && (w->configs[i][ permute(j+1,w->size) ] == 1) ){
					w->energies[i]		+= Gc; /* 111 */
					sim->enthalpies[i]	+= Hc;
				}
			}
		}
	}

	return;
}
