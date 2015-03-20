#!/usr/bin/env python

from itcsimlib			import ITCSim,ITCFit
from itcsimlib.thermo	import *

sim = ITCSim(T_ref=275.15+25.127772)
sim.setup_model( ['./itcsimlib/itc_sim_n_identical.so',(1,)] )
sim.set_params(
	dG	= [dG_from_Kd(1.0E-6,sim.T_ref)],
	dH	= [J_from_cal(-2.0E7)],
	dCp	= [0]
)

sim.load_file( '../data/fake-25C.txt', T=sim.T_ref, V0=199.3, M0=0.1E-3, L0=1.0E-3, skip=[0] )
sim.update_fits()
sim.make_plots(hardcopy=True,hardcopyprefix='1site_pre_')

fit = ITCFit(sim,maxfun=1E5,method='',verbose=True)
dG,dH,sse = fit.fit_dGdH()

print "%0.2E" % (1.0/Kd_from_dG(dG[0],sim.T_ref))
print cal_from_J(dH[0])
print dS_from_dGdH(dG[0],dH[0],sim.T_ref)

sim.set_params(dG,dH)
sim.update_fits()
sim.make_plots(hardcopy=True,hardcopyprefix='1site_post_')
sim.close()

#
#
#

sim = ITCSim(T_ref=275.15+25.127772)
sim.setup_model( ['./itcsimlib/itc_sim_simple.so',(11,1)] )
sim.set_params(
	dG	= [dG_from_Kd(1.0E-6,sim.T_ref)],
	dH	= [J_from_cal(-2.0E7)],
	dCp	= [0]
)

sim.load_file( '../data/fake-25C.txt', T=sim.T_ref, V0=199.3, M0=0.1E-3/11, L0=1.0E-3, skip=[0] )
sim.update_fits()
sim.make_plots(hardcopy=True,hardcopyprefix='simple_pre_')

fit = ITCFit(sim,maxfun=1E5,method='',verbose=True)
dG,dH,sse = fit.fit_dGdH()

print "%0.2E" % (1.0/Kd_from_dG(dG[0],sim.T_ref))
print cal_from_J(dH[0])
print dS_from_dGdH(dG[0],dH[0],sim.T_ref)

sim.set_params(dG,dH)
sim.update_fits()
sim.make_plots(hardcopy=True,hardcopyprefix='simple_post_')
sim.close()

#
#
#

sim = ITCSim(T_ref=275.15+25.127772)
sim.setup_model( ['./itcsimlib/itc_sim_nnx.so',(11,1)] )
sim.set_params(
	dG	= [dG_from_Kd(1.0E-6,sim.T_ref)]*3,
	dH	= [J_from_cal(-2.0E7)]*3,
	dCp	= [0]*3
)

sim.load_file( '../data/fake-25C.txt', T=sim.T_ref, V0=199.3, M0=0.1E-3/11, L0=1.0E-3, skip=[0] )
sim.update_fits()
sim.make_plots(hardcopy=True,hardcopyprefix='nnx_pre_')

fit = ITCFit(sim,maxfun=1E5,method='',verbose=True)
dG,dH,sse = fit.fit_dGdH()

print "%0.2E" % (1.0/Kd_from_dG(dG[0],sim.T_ref))
print cal_from_J(dH[0])
print dS_from_dGdH(dG[0],dH[0],sim.T_ref)

sim.set_params(dG,dH)
sim.update_fits()
sim.make_plots(hardcopy=True,hardcopyprefix='nnx_post_')
sim.close()

#
#
#

sim = ITCSim(T_ref=275.15+25.127772)
sim.setup_model( ['./itcsimlib/itc_sim_nn.so',(11,1)] )
sim.set_params(
	dG	= [dG_from_Kd(1.0E-6,sim.T_ref)]+[0]*3,
	dH	= [J_from_cal(-2.0E7)]+[0]*3,
	dCp	= [0]*4
)

sim.load_file( '../data/fake-25C.txt', T=sim.T_ref, V0=199.3, M0=0.1E-3/11, L0=1.0E-3, skip=[0] )
sim.update_fits()
sim.make_plots(hardcopy=True,hardcopyprefix='nn_pre_')

fit = ITCFit(sim,maxfun=1E5,method='',verbose=True)
dG,dH,sse = fit.fit_dGdH()

print "%0.2E" % (1.0/Kd_from_dG(dG[0],sim.T_ref))
print cal_from_J(dH[0])
print dS_from_dGdH(dG[0],dH[0],sim.T_ref)

sim.set_params(dG,dH)
sim.update_fits()
sim.make_plots(hardcopy=True,hardcopyprefix='nn_post_')
sim.close()
