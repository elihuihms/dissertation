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
#include "energies_3fragment.h"

struct mWorkspace model;
struct sWorkspace sim;

char stepA[6],stepB[6],stepC[6];

int setup( int size, char* A, char* B, char *C )
{
	model.size	= size;

	strcpy(stepA, A);
	strcpy(stepB, B);
	strcpy(stepC, C);

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
		stepA,		stepB,		stepC,
		params[0],	params[1],	params[2],
		params[3],	params[4],	params[5]);

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