//
//  main.c
//  itc_sim
//
//  Created by Elihu Ihms on 2/18/14.
//  Copyright (c) 2014 Elihu Ihms. All rights reserved.
//

#include <string.h>

#include "itc_model.h"
#include "itc_sim.h"
#include "energies_fragment.h"

struct mWorkspace model;
struct sWorkspace sim;

int n_params;
int exclusive; // do we stop applying additional fragment dG,dHs if we've already found a match?
char** fragments;

int setup( int size, int x, int n, char** f )
{
	model.size	= size;
	exclusive	= x;
	n_params	= n;

	fragments = malloc(n_params * sizeof(char*) );
	for(int i=0; i<n_params; i++)
	{
		fragments[i] = (char*)malloc( (size+1) * sizeof(char) );
		strcpy(fragments[i], f[i]); // f better be null terminated
	}

	if( setupModelWorkspace(&model) > 0 )
		return 0;
	if( setupSimWorkspace(&sim,model) > 0 )
		return 0;

	return 0;
}

int calc( int n, double* P, double* L, double* Q, double *params, double temp )
{
	model.temp = temp;

	assignEnergies(&model, &sim, n_params, exclusive, fragments, params);

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
	for(int i=0; i<n_params; i++)
		free( fragments[i] );
	free( fragments );

	freeSimWorkspace(sim,model);
	freeModelWorkspace(model);

	return 0;
}