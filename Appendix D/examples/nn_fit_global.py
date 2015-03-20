#!/usr/bin/env python

from itcsimlib	import ITCSim,ITCFit
from itcsimlib.thermo		import *
from random		import random

sim = ITCSim(T_ref=275.15+40)
sim.setup_model( ['../itcsimlib/itc_sim_comprehensive.so',()] )

# obtained from single-mode fitting to all datasets
sim.set_params(
	dG	= [-3.5931E+04]*125,
	dH	= [-7.9152E+04]*125,
	dCp	= [-1.7712E+03]*125
)

dG,dH = [],[]
h = open('fmin_lastparams.txt')
for l in h.readlines():
	a = map(float,l.split())
	dG.append(a[0])
	dH.append(a[1])
h.close()
sim.set_params(dG,dH)

#sim.load_file( '../data/15C-01-TRAPstk-TrpA.txt',	T=275.15+15, V0=1416.6, M0=0.07500E-3/11, L0=0.61067E-3, skip=[0], 			dil_Q=1.491E+6 )
#sim.load_file( '../data/15C-02-TRAPG-TrpC.txt',		T=275.15+15, V0=1416.6, M0=0.02082E-3/11, L0=0.17962E-3, skip=[0] )
sim.load_file( '../data/20C-01-TRAPstk-TrpA.txt',	T=275.15+20, V0=1416.6, M0=0.07500E-3/11, L0=0.61067E-3, skip=[0],			dil_Q=8.524E+4 )
sim.load_file( '../data/20C-02-TRAPF-TrpC.txt',		T=275.15+20, V0=1416.6, M0=0.02120E-3/11, L0=0.17962E-3, skip=[0],			dil_Q=2.069E+6 )
sim.load_file( '../data/25C-02-TRAPE-TrpE.txt',		T=275.15+25, V0=1416.6, M0=0.03018E-3/11, L0=0.24900E-3, skip=[0],			dil_Q=9.838E+4 )
sim.load_file( '../data/25C-03-TRAPO-TrpG.txt',		T=275.15+25, V0=1416.6, M0=0.01496E-3/11, L0=0.15558E-3, skip=[0],			dil_Q=3.376E+5 )
sim.load_file( '../data/25C-04-TRAPP-TrpH.txt',		T=275.15+25, V0=1416.6, M0=0.02010E-3/11, L0=0.18772E-3, skip=[0,1,2,3],	dil_Q=6.846E+5 )
sim.load_file( '../data/30C-01-TRAPD-TrpD.txt',		T=275.15+30, V0=1416.6, M0=0.04013E-3/11, L0=0.34632E-3, skip=[0,1,2],		dil_Q=3.352E+5 )
sim.load_file( '../data/30C-02-TRAPP-TrpH.txt',		T=275.15+30, V0=1416.6, M0=0.02010E-3/11, L0=0.18772E-3, skip=[0],			dil_Q=1.620E+6 )
sim.load_file( '../data/35C-01-TRAPstk-TrpA.txt',	T=275.15+35, V0=1416.6, M0=0.07500E-3/11, L0=0.61067E-3, skip=[0],			dil_Q=2.174E+5 )
sim.load_file( '../data/35C-02-TRAPC-TrpC.txt',		T=275.15+35, V0=1416.6, M0=0.02190E-3/11, L0=0.17962E-3, skip=[0],			dil_Q=2.292E+6 )
sim.load_file( '../data/35C-03-TRAPM-TrpE.txt',		T=275.15+35, V0=1416.6, M0=0.03005E-3/11, L0=0.24900E-3, skip=[0],			dil_Q=1.071E+6 )
sim.load_file( '../data/40C-01-TRAPstk-TrpA.txt',	T=275.15+40, V0=1416.6, M0=0.07500E-3/11, L0=0.61067E-3, skip=[0,1],		dil_Q=6.521E+4 )
#sim.load_file( '../data/40C-02-TRAPF-TrpC.txt',		T=275.15+40, V0=1416.6, M0=0.02120E-3/11, L0=0.17962E-3, skip=[0]
sim.load_file( '../data/40C-03-TRAPH-TrpF.txt',		T=275.15+40, V0=1416.6, M0=0.02994E-3/11, L0=0.28418E-3, skip=[0],			dil_Q=8.567E+5 )
sim.load_file( '../data/45C-01-TRAPstk-TrpA.txt',	T=275.15+45, V0=1416.6, M0=0.07500E-3/11, L0=0.61067E-3, skip=[0],			dil_Q=3.057E+5 )
sim.load_file( '../data/45C-02-TRAPI-TrpF.txt',		T=275.15+45, V0=1416.6, M0=0.03011E-3/11, L0=0.28418E-3, skip=[0],			dil_Q=9.157E+5 )
sim.load_file( '../data/50C-02-TRAPQ-TrpI.txt',		T=275.15+50, V0=1416.6, M0=0.03004E-3/11, L0=0.32310E-3, skip=[0],			dil_Q=5.057E+5 )
sim.load_file( '../data/55C-01-TRAPstk-TrpB.txt',	T=275.15+55, V0=1416.6, M0=0.07500E-3/11, L0=0.76522E-3, skip=[0],			dil_Q=1.237E+5 )
sim.load_file( '../data/55C-02-TRAPJ-TrpF.txt',		T=275.15+55, V0=1416.6, M0=0.02464E-3/11, L0=0.28418E-3, skip=[0],			dil_Q=1.298E+6 )
sim.load_file( '../data/55C-03-TRAPK-TrpC.txt',		T=275.15+55, V0=1416.6, M0=0.01016E-3/11, L0=0.17962E-3, skip=[0],			dil_Q=1.008E+6 )
sim.load_file( '../data/55C-04-TRAPL-TrpD.txt',		T=275.15+55, V0=1416.6, M0=0.03501E-3/11, L0=0.34632E-3, skip=[0],			dil_Q=2.561E+6 )
sim.load_file( '../data/55C-05-TRAPN-TrpD.txt',		T=275.15+55, V0=1416.6, M0=0.02996E-3/11, L0=0.34632E-3, skip=[0],			dil_Q=1.526E+6 )
sim.load_file( '../data/55C-06-TRAPP-TrpE.txt',		T=275.15+55, V0=1416.6, M0=0.02010E-3/11, L0=0.24900E-3, skip=[0],			dil_Q=1.604E+5 )
#sim.load_file( '../data/65C-01-TRAPstk-TrpB.txt',	T=275.15+65, V0=1416.6, M0=0.07500E-3/11, L0=0.76522E-3, skip=[0],			dil_Q=3.673E+5 )
#sim.load_file( '../data/65C-02-TRAPQ-TrpJ.txt',		T=275.15+65, V0=1416.6, M0=0.03004E-3/11, L0=0.48671E-3, skip=[0],			dil_Q=3.140E+4 )

sim.update_fits()
sim.make_plots(hardcopy=True,hardcopyprefix='pre_')

fit = ITCFit(sim,maxfun=1E10,method='powell',verbose=True,ftol=1E-3)
dG,dH,dCp		= sim.dG,sim.dH,sim.dCp
#dG,dH,rmsd		= fit.fit_dGdH()
#dCp,rmsd		= fit.fit_dCp()
fit.set_bounds(dG=[ (None,0) ]*125)
dG,dH,dCp,rmsd	= fit.fit_dGdHdCp()
sim.set_params(dG=dG,dH=dH,dCp=dCp)

sim.update_fits()
sim.make_plots(hardcopy=True)
sim.close()

h = open('fit.log','a')
h.write("%s	%s	%s	%f"%(str(dG),str(dH),str(dCp),rmsd))
h.close()
