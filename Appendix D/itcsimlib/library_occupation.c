//
//  main.c
//  itc_sim
//
//  Created by Elihu Ihms on 2/18/14.
//  Copyright (c) 2014 Elihu Ihms. All rights reserved.
//

#include "itc_model.h"
#include "itc_sim.h"
#include "energies_occupation.h"

struct mWorkspace model;
struct sWorkspace sim;

int n_params;
int b_energy[12];

int setup(int n, int* steps)
{
	model.size		= 11;
	n_params = n;

	// this is hideous, but I don't care
	int j=0;
	for(int i=0; i<n; i++)
	{
		while( j < steps[i] )
		{
			b_energy[j] = i-1;
			j++;
		}
	}
	b_energy[0] = 0;
	while( j < 12 )
	{
		b_energy[j] = n-1;
		j++;
	}
	// done with hideousness

	//for(int i=0;i<11;i++)
	//	printf("%i %i\n",i,b_energy[i]);

	if( setupModelWorkspace(&model) > 0 )
		return 0;
	if( setupSimWorkspace(&sim,model) > 0 )
		return 0;

	return 0;
}

int calc( int n, double* P, double* L, double* Q, double *params, double temp )
{
	int i;
	double G[12];
	double H[12];

	model.temp = temp;

	for(i=0; i<12; i++)
	{
		G[i] = params[ b_energy[i] ];
		H[i] = params[ b_energy[i]+n_params ];
	}

	assignEnergies(&model, &sim, G, H);

	for(i=0; i<n; i++)
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