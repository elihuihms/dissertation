#!/usr/bin/env python

import os
import sys
import glob

sys.path.append("/fosterlab/users/ihms/Projects/MESMER/utilities/pyParaTools_modified")
sys.path.append("/Volumes/FosterLab/users/ihms/Projects/MESMER/utilities/pyParaTools_modified")

from ParaParser	import *
from CalcPara	import *
from FitPara	import *
from ExplorePara import *
from ParaUtils	import *

# Metal coordinates: -5.885, 8.219, 1.059
#
# PCS and RDC Tb and Tm tensor axial and rhombicities available from Bertini et al. (2004) PNAS
# doi: 10.1073/pnas.0308641101
#
# PCS	Dax		Drh
# Tm:	26		-9.1
# Tb:	37		-14
#
# These Dax and Drh from Bertini 2004 for RDCs are the averaged Dax and Drh for the Cterm. Don't use 'em.
# RDC	Dax		Drh
# Tm:	-3.3	2.2
# Tb:	-1.6	0.8
#
# The tensor values are available in the Max occurence demo file "tensor.tns" :
# 9825.     3692.    0.511     -0.47     -0.61
# 6767.     2417.   -2.377     -1.170     0.697
# 8958.    -3974.   -3.209      0.210    -0.123	(I think this is for Dysprosium)
#
# NOTE: I assume that the last three columns are the alpha,beta, and gamma components of the tensor, but they don't match up with values that I've fitted (see below)
#
# Dax and Drh Converted from the above VV (Van vleck) units to 10^-32 m^3 (gives us some more decimal points), and Converted a,b,g from radians to degrees as well
# (note: a flip in Drh negative sign results in a 90deg change in gamma)
#     	Dax		Drh		a		b		g
# Tm:	25.51	9.112	29.28	-26.93	-34.95
# Tb: 	37.04	13.92	-136.2	-67.04	39.94
#
# Attempting to fit data w/ Max occurrence tensor a,b,g gives crappy results. Why?
# Regardless, we can fit them using the PCS obtained from the N-termini (see cam_fit.py):
#
# Fitting Dax, Dr, alpha, beta, and gamma:
#		Dax		Drh		a		b		g
# Tm:	25.38	9.660	149.4	107.6	314.2
# Tb:	39.18	-13.56	70.54	43.49	60.24
#
# Fitting just alpha, beta, and gamma, using the published Dax and Drh:
#		Dax		Drh		a		b		g
# Tm:	25.51	-9.112	149.3	107.3	223.7
# Tb:	37.04	-13.92	71.66	43.89	56.48
#
# Unfortunately, don't have Dysprosium PCS data for Nterm, so can't calculate Dax, Drh
#

_pcs_table_1 = 'tables/Bertini_2004_Tm.pcs'
_pcs_table_2 = 'tables/Bertini_2004_Tb.pcs'
_rdc_table_1 = 'tables/Bertini_2004_Tm.rdc'
_rdc_table_2 = 'tables/Bertini_2004_Tb.rdc'

#			Metal:  x      y      z       Dax      Drh      alpha     beta     gamma
_pcs_params_1 =  [-5.885, 8.219, 1.059, 25.51, -9.112, 149.3, 107.3, 223.7]
_pcs_params_2 =  [-5.885, 8.219, 1.059, 37.04, -13.92, 71.66, 43.89, 56.48]

# Bertini used 600.13 (14.09T) and 700.13 (16.44T) @ 298K (42.58 Mhz/Tesla) Did some comparative fitting, 700MHz fits best
_rdc_params_1 = [ _pcs_params_1[3], _pcs_params_1[4], _pcs_params_1[5], _pcs_params_1[6], _pcs_params_1[7], 16.44, 298.0, 1.0]
_rdc_params_2 = [ _pcs_params_2[3], _pcs_params_2[4], _pcs_params_2[5], _pcs_params_2[6], _pcs_params_2[7], 16.44, 298.0, 1.0]

def mkPCS( pdb, output1, output2 ):
	global _pcs_table_1
	global _pcs_table_2

	global _pcs_params_1
	global _pcs_params_2

	params = ['', 'pcs', pdb, _pcs_table_1]
	params.extend(_pcs_params_1)

	pcs			= PCSParser(params)
	calculator	= CalcPara()
	analysis	= ExplorePara()

	pcs.doParse()
	calculator.PCS(pcs, 'ZYZ')
	analysis.buildNumbatTBL(pcs, output1)

	params = ['', 'pcs', pdb, _pcs_table_2]
	params.extend(_pcs_params_2)

	pcs			= PCSParser(params)
	calculator	= CalcPara()
	analysis	= ExplorePara()

	pcs.doParse()
	calculator.PCS(pcs, 'ZYZ')
	analysis.buildNumbatTBL(pcs, output2)

	return

def mkRDC( pdb, output1, output2 ):
	global _rdc_table_1
	global _rdc_table_2

	global _rdc_params_1
	global _rdc_params_2

	params = ['','rdc',pdb, _rdc_table_1]
	params.extend(_rdc_params_1)

	rdc			= RDCParser(params)
	fit			= FitPara()
	calculator	= CalcPara()
	analysis	= ExplorePara()

	rdc.doParse()
	calculator.RDC(rdc, 'ZYZ')
	analysis.buildNumbatTBL(rdc, output1)

	params = ['','rdc',pdb, _rdc_table_2]
	params.extend(_rdc_params_2)

	rdc			= RDCParser(params)
	fit			= FitPara()
	calculator	= CalcPara()
	analysis	= ExplorePara()

	rdc.doParse()
	calculator.RDC(rdc, 'ZYZ')
	analysis.buildNumbatTBL(rdc, output2)

	return

if( __name__ == "__main__" ):
	if(len(sys.argv) < 2):
		print "Usage: calc_para.py <file.pdb>"
		sys.exit(0)

	name = os.path.splitext(sys.argv[1])[0]

	mkPCS( sys.argv[1], "%s_Tm.pcs" % (name) ,"%s_Tb.pcs" % (name) )
	mkRDC( sys.argv[1], "%s_Tm.rdc" % (name) ,"%s_Tb.rdc" % (name) )
