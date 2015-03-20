#!/usr/bin/env python

import sys

sys.path.append("/Volumes/FosterLab/users/ihms/Projects/MESMER/utilities/pyParaTools_modified")

from ParaParser	import *
from CalcPara	import *
from FitPara	import *
from ExplorePara import *
from ParaUtils	import *

# Metal coordinates: -5.885, 8.219, 1.059

#
# Initial RDC and PCS Tb and Tm tensor axial and rhombicities taken from Bertini et al. (2004) PNAS
# doi: 10.1073/pnas.0308641101
#

# These same values available in the Max occurence demo file "tensor.tns" :
#9825.     3692.    0.511     -0.47     -0.61
#6767.     2417.   -2.377     -1.170     0.697
#8958.    -3974.   -3.209      0.210    -0.123

#print FromVVU(9825)
#print FromVVU(6767)
#print FromVVU(8958)
#print
#print FromVVU(3692)
#print FromVVU(2417)
#print FromVVU(-3974)

# 0: fit metal X, Y, Z, Dax, Drh, a, b, g
# 1: fit Dax, Drh, a, b, g
# 7: fit a, b, g (special case)
fittype = 1

print "PCS analysis, Calmodulin N-term domain, Thulium"
#params = ['', 'pcs', './usecase_Nmet.pdb', 'tables/Bertini_2004_Tm.pcs', -5.885, 8.219, 1.059, 26, -9.1, 90, 90, 90]
#params = ['', 'pcs', './usecase_Nmet.pdb', 'tables/Bertini_2004_Tm.pcs', -5.885, 8.219, 1.059, FromVVU(6767), FromVVU(2417), 90, 90, 90]
params = ['', 'pcs', './usecase_Nmet.pdb', 'tables/Bertini_2004_Tm.pcs', -5.885, 8.219, 1.059, FromVVU(6767), FromVVU(-2417), 90, 90, 90]

pcs			= PCSParser(params)
fit			= FitPara()
calculator	= CalcPara()
analysis	= ExplorePara()
pcs.doParse()

if(fittype>0):
	print "Metal loc fixed to %.3f,%.3f,%.3f" % (params[4],params[5],params[6])
if(fittype==7):
	print "Dax fixed to: %.3f" % params[7]
	print "Drh fixed to: %.3f" % params[8]

fit.PCS(pcs, fittype)
calculator.PCS(pcs, 'ZYZ')
analysis.buildNumbatTBL(pcs, './Tm_calc.pcs')

print "PCS analysis, Calmodulin N-term domain, Terbium"
#params = ['', 'pcs', './usecase_Nmet.pdb', 'tables/Bertini_2004_Tb.pcs', -5.885, 8.219, 1.059, 37, -14, 90, 90, 90]
#params = ['', 'pcs', './usecase_Nmet.pdb', 'tables/Bertini_2004_Tb.pcs', -5.885, 8.219, 1.059, FromVVU(9825), FromVVU(3692), 90, 90, 90]
params = ['', 'pcs', './usecase_Nmet.pdb', 'tables/Bertini_2004_Tb.pcs', -5.885, 8.219, 1.059, FromVVU(9825), FromVVU(-3692), 71, 43, 56]

pcs			= PCSParser(params)
fit			= FitPara()
calculator	= CalcPara()
analysis	= ExplorePara()
pcs.doParse()

if(fittype>0):
	print "Metal loc fixed to %.3f,%.3f,%.3f" % (params[4],params[5],params[6])
if(fittype==7):
	print "Dax fixed to: %.3f" % params[7]
	print "Drh fixed to: %.3f" % params[8]

fit.PCS(pcs, fittype)
calculator.PCS(pcs, 'ZYZ')
analysis.buildNumbatTBL(pcs, './Tb_calc.pcs')

print "PCS analysis, Calmodulin C-term domain, Dysprosium"
params = ['', 'pcs', './usecase_Cmet.pdb', 'tables/Bertini_2010_Dy.pcs', -5.885, 8.219, 1.059, FromVVU(8958), FromVVU(-3974), -184, 12.0, -7.05]

pcs			= PCSParser(params)
fit			= FitPara()
calculator	= CalcPara()
analysis	= ExplorePara()
pcs.doParse()

if(fittype>0):
	print "Metal loc fixed to %.3f,%.3f,%.3f" % (params[4],params[5],params[6])
if(fittype==7):
	print "Dax fixed to: %.3f" % params[7]
	print "Drh fixed to: %.3f" % params[8]

fit.PCS(pcs, fittype)
calculator.PCS(pcs, 'ZYZ')
analysis.buildNumbatTBL(pcs, './Dy_calc.pcs')

print "RDC analysis, Calmodulin C-term domain, Dysprosium"
params = ['','rdc','./usecase_Cmet.pdb', 'tables/Bertini_2010_Dy.rdc', -1, 1, 62.77, 347.2, 116.8, 16.44, 298.0, 1.0]

rdc			= RDCParser(params)
fit			= FitPara()
calculator	= CalcPara()
analysis	= ExplorePara()

rdc.doParse()
fit.RDC(rdc, 2, 1)
analysis.buildNumbatTBL(rdc, './Dy_calc.rdc')

print "A,B,G fixed to: %.3f,%.3f,%.3f" % (params[6],params[7],params[8])
