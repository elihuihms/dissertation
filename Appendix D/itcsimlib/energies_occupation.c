#include "itc_model.h"
#include "itc_sim.h"

void assignEnergies( struct mWorkspace *w, struct sWorkspace *sim, double G[12], double H[12] )
{
	//printf("%f %f %f %f %f %f %f %f %f %f %f %f\n",G[0],G[1],G[2],G[3],G[4],G[5],G[6],G[7],G[8],G[9],G[10],G[10]);
	for(int i=0; i<pow(2, w->size); i++)
	{
		w->energies[i]		= G[ w->bound[i] ]*w->bound[i];
		sim->enthalpies[i]	= H[ w->bound[i] ]*w->bound[i];
	}
}
