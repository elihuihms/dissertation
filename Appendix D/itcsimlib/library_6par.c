//
//  main.c
//  itc_sim
//
//  Created by Elihu Ihms on 2/18/14.
//  Copyright (c) 2014 Elihu Ihms. All rights reserved.
//

#include "itc_model.h"
#include "itc_sim.h"
#include "energies_6par.h"

struct mWorkspace model;
struct sWorkspace sim;

int setup( int size, int cyclic )
{
	model.size		= size;
	model.cyclic	= cyclic;
	
	if( setupModelWorkspace(&model) > 0 )
		return 0;
	if( setupSimWorkspace(&sim,model) > 0 )
		return 0;

	return 0;
}

int calc( int n, double* P, double* L, double* Q, double *params, double temp )
{
	model.temp = temp;
	assignEnergies(&model, &sim,
		params[0], params[1], params[2],
		params[3], params[4], params[5]);

	for(int i=0; i<n; i++)
	{
		model.Ptot = P[i];
		model.Ltot = L[i];
		setFree( &model );

		Q[i] = getQ( sim, model );
	}

    return 0;
}

int close()
{
	freeSimWorkspace(sim,model);
	freeModelWorkspace(model);

	return 0;
}