#include "itc_model_comprehensive.h"

struct mWorkspace model;

int setup()
{
	if( setupModelWorkspace(&model) > 0 )
		return 1;

	return 0;
}

int calc( int n, double* P, double* L, double* Q, double *params, double temp )
{
	int i=0;
	model.temp = temp;

	for(i=1; i<126; i++)
		model.dG[i] = params[i-1];

	/* set the protein and ligand concentrations at each injection point, and determine the enthalpic heat present for each */
	for(i=0; i<n; i++)
	{
		model.Ptot = P[i];
		model.Ltot = L[i];
		setFree( &model );

		Q[i] = 0;
		for(int j=1; j<126; j++)
			Q[i] += model.probs[j] * params[j+124] * model.bound[j];

	}

    return 0;
}

int close()
{
	freeModelWorkspace(model);
	return 0;
}