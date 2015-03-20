#include <math.h>

/* binding polynomial from Microcal's "ITC Data Analysis In Origin, Rev. F-4, p.g. 106, eq. 9".
Note that normalization to cell volume (V0) and macromolecule concentration is taken into account in itc_calc.py
*/

double n_sites;
int setup( double n )
{
	n_sites	= n;
	return 0;
}

int calc( int n, double* P, double* L, double* Q, double *params, double temp )
{
	// R = J/(K*mol)
	double Ka = 1.0/exp(params[0]/(8.3144621*temp));
	for(int i=0; i<n; i++)
	{
		Q[i] = ((n_sites*params[1])/2.0)*(1.0 +(L[i]/(n_sites*P[i])) +(1.0/(n_sites*Ka*P[i])) -sqrt( pow(1 +(L[i]/(n_sites*P[i])) +(1.0/(n_sites*Ka*P[i])), 2.0) -((4.0*L[i])/(n_sites*P[i]))));
	}
    return 0;
}

int close()
{
	return 0;
}