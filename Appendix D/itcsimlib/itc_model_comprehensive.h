#ifndef _itc_model_h_
#define _itc_model_h_
#include <gsl/gsl_errno.h>
#include <gsl/gsl_math.h>
#include <gsl/gsl_roots.h>

struct mWorkspace
{
	int		size;
	double	temp;
	double	Ptot;
	double	Ltot;
	double	Pfree;
	double	Lfree;
	int		bound[126];
	double	weight[126];
	double	dG[126];
	double	probs[126];
	gsl_root_fsolver*		fsolver_s;
	gsl_function			fsolver_F;
} mWorkspace;

int		setupModelWorkspace( struct mWorkspace *w );
int 	freeModelWorkspace( struct mWorkspace w );
void	setProbabilities( struct mWorkspace *w );
double	getFree( double Lfree, void *params );
int		setFree( struct mWorkspace *w );

#endif