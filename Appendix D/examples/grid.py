#!/usr/bin/env python

import sys

from itcsimlib	import ITCSim, ITCFit
from itcsimlib.thermo import dG_from_Kd
from numpy		import linspace,logspace

for dGK in [dG_from_Kd(Kd, 275.15+40) for Kd in logspace(-9,-3,10)]:
	for dGA in linspace(-5,+5,10):
		for (i,dGB) in enumerate(linspace(-5,+5,10)):
			for (j,dGC) in enumerate(linspace(-5,+5,10)):

				if int(sys.argv[1]) != (i*10)+j :
					continue

				sim = ITCSim(T_ref=275.15+40,threads=1,verbose=True)
				sim.setup_model( ['./itcsimlib/itc_sim_nn.so',(11,1)] )
				sim.set_params(
					dG			= [dGK,dGA,dGB,dGC],
					dH			= [-8.0099E+04]+[0.0]*3,
					dCp			= [0.0]*4,
				)

				sim.load_file( '../data/40C-03-TRAPH-TrpF.txt',		T=275.15+40, V0=1416.6, M0=0.02994E-3/11, L0=0.28418E-3, skip=[0], dil_Q=1E6 )

				fit = ITCFit(sim,maxfun=1E5,method='powell',verbose=True)
				dH,rmsd = fit.fit_dH()

				sim.set_params(dH=dH)
				sim.update_fits()
				sim.make_plots(hardcopy=True,hardcopyprefix='post_%i-%i'%(i,j))

				handle = open('results.txt','w')
				handle.write("%s	%s	%f\n"%("\t".join(map(str,sim.dG[:])),"\t".join(map(str,dH[:])),rmsd))
				handle.close()

				sim.close()
