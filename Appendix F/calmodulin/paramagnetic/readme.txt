This directory contains scripts for calculating/fitting the paramagnetic tensors for calmodulin, as well as the raw data for several lanthanides.

./calc_para.py: Calculates PCS and RDCs for a given PDB, using hard-coded tensors (see source code)

./cam_calc_all.py: Generates tensors from fits obtained from PCS data on the calmodulin N-term domain, uses to calculate PCS and RDCs for the C-terminal domain

./cam_fit.py: Tries several different pyParaTools fit routines to determine paramagnetic tensors

./tables: Experimental data from Bertini's paper on maximum occurrence analysis of calmodulin, in several different formats.


