#!/usr/bin/env python

from itcsimlib import ITCSim,ITCFit
from os.path import isfile

files = []
#files.append( ('15C-01-TRAPstk-TrpA',	275.15+15, 1416.6, 0.07500E-3, 0.61067E-3, [0] ))
files.append( ('15C-02-TRAPG-TrpC',		275.15+15, 1416.6, 0.02082E-3, 0.17962E-3, [0] ))
files.append( ('20C-01-TRAPstk-TrpA',	275.15+20, 1416.6, 0.07500E-3, 0.61067E-3, [0] ))
files.append( ('20C-02-TRAPF-TrpC',		275.15+20, 1416.6, 0.02120E-3, 0.17962E-3, [0] ))
#files.append( ('25C-02-TRAPE-TrpE',		275.15+25, 1416.6, 0.03018E-3, 0.24900E-3, [0] ))
files.append( ('25C-03-TRAPO-TrpG',		275.15+25, 1416.6, 0.01496E-3, 0.15558E-3, [0] ))
files.append( ('25C-04-TRAPP-TrpH',		275.15+25, 1416.6, 0.02010E-3, 0.18772E-3, [0,1,2,3] ))
files.append( ('30C-01-TRAPD-TrpD',		275.15+30, 1416.6, 0.04013E-3, 0.34632E-3, [0,1,2] ))
files.append( ('30C-02-TRAPP-TrpH',		275.15+30, 1416.6, 0.02010E-3, 0.18772E-3, [0] ))
files.append( ('35C-01-TRAPstk-TrpA',	275.15+35, 1416.6, 0.07500E-3, 0.61067E-3, [0] ))
files.append( ('35C-02-TRAPC-TrpC',		275.15+35, 1416.6, 0.02190E-3, 0.17962E-3, [0] ))
files.append( ('35C-03-TRAPM-TrpE',		275.15+35, 1416.6, 0.03005E-3, 0.24900E-3, [0] ))
files.append( ('40C-01-TRAPstk-TrpA',	275.15+40, 1416.6, 0.07500E-3, 0.61067E-3, [0,1] ))
#files.append( ('40C-02-TRAPF-TrpC',		275.15+40, 1416.6, 0.02120E-3, 0.17962E-3, [0] ))
files.append( ('40C-03-TRAPH-TrpF',		275.15+40, 1416.6, 0.02994E-3, 0.28418E-3, [0] ))
files.append( ('45C-01-TRAPstk-TrpA',	275.15+45, 1416.6, 0.07500E-3, 0.61067E-3, [0] ))
files.append( ('45C-02-TRAPI-TrpF',		275.15+45, 1416.6, 0.03011E-3, 0.28418E-3, [0] ))
files.append( ('50C-02-TRAPQ-TrpI',		275.15+50, 1416.6, 0.03004E-3, 0.32310E-3, [0] ))
files.append( ('55C-01-TRAPstk-TrpB',	275.15+55, 1416.6, 0.07500E-3, 0.76522E-3, [0] ))
files.append( ('55C-02-TRAPJ-TrpF',		275.15+55, 1416.6, 0.02464E-3, 0.28418E-3, [0] ))
files.append( ('55C-03-TRAPK-TrpC',		275.15+55, 1416.6, 0.01016E-3, 0.17962E-3, [0] ))
files.append( ('55C-04-TRAPL-TrpD',		275.15+55, 1416.6, 0.03501E-3, 0.34632E-3, [0] ))
files.append( ('55C-05-TRAPN-TrpD',		275.15+55, 1416.6, 0.02996E-3, 0.34632E-3, [0] ))
files.append( ('55C-06-TRAPP-TrpE',		275.15+55, 1416.6, 0.02010E-3, 0.24900E-3, [0] ))
files.append( ('65C-01-TRAPstk-TrpB',	275.15+65, 1416.6, 0.07500E-3, 0.76522E-3, [0,85,91,94] ))
files.append( ('65C-02-TRAPQ-TrpJ',		275.15+65, 1416.6, 0.03004E-3, 0.48671E-3, [0] ))

# get simple model dG dH fit coefficients
handle = open('simple.log')
params,keys = {},zip(*files)[0]
for name,dG,dH in [l.split()[:3] for l in handle.readlines()]:
	#params[name] = (float(dG),float(dH))
	params[name] = (-3.5931E+04,-7.9152E+04)
handle.close()

for name,T,V0,M0,L0,skip in files:
	if isfile("post_%s.png"%name):
		continue

	sim = ITCSim(T_ref=T,threads=1,verbose=True)
	sim.setup_model( ['./itcsimlib/itc_sim_nn.so',(11,1)] )

	sim.set_params(
		dG	= [params[name][0]]+[0.0]*3,
		dH	= [params[name][1]]+[0.0]*3,
		dCp	= [0.0]*4
	)

	sim.load_file( "../data/%s.txt"%name,T=T,V0=V0,M0=M0/11,L0=L0,skip=skip )
	sim.update_fits()
	sim.make_plots(hardcopy=True,hardcopyprefix='pre_')

	fit = ITCFit(sim,maxfun=1E5,method='powell',verbose=True)
	dG,dH,rmsd = fit.fit_dGdH()

	sim.set_params(dG,dH)
	sim.update_fits()
	sim.make_plots(hardcopy=True,hardcopyprefix='post_')

	h = open('fit.log','a')
	h.write("%s	%s	%s	%f\n"%(name,"\t".join(map(str,dG)),"\t".join(map(str,dH)),rmsd))
	h.close()

	sim.close()