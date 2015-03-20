#!/usr/bin/env python

import sys

sys.path.append("/Volumes/FosterLab/users/ihms/Projects/MESMER/utilities/pyParaTools_modified")

from ParaParser	import *
from CalcPara	import *
from FitPara	import *
from ExplorePara import *
from ParaUtils	import *

#
# Initial RDC and PCS Tb and Tm tensor axial and rhombicities taken from Bertini et al. (2004) PNAS
# doi: 10.1073/pnas.0308641101
#

# Metal coordinates: -5.885, 8.219, 1.059
print "PCS analysis, Calmodulin N-term domain, Thulium"
params = ['', 'pcs', 'cam_H/00001cam_Nterm.pdb', 'tables/Bertini_2004_Tm.pcs', -5.885, 8.219, 1.059, 26, -9.1, 90, 90, 90]
pcs			= PCSParser(params)
fit			= FitPara()
calculator	= CalcPara()
analysis	= ExplorePara()

pcs.doParse()
fit.PCS(pcs, 1) # fixed metal loc
calculator.PCS(pcs, 'ZYZ')
analysis.buildNumbatTBL(pcs, './cam_all/00001cam_Nterm_Tm_calc.pcs')

print "PCS analysis, Calmodulin C-term domain, Thulium"
params = ['', 'pcs', 'cam_H/00001cam_Cterm.pdb', 'tables/Bertini_2004_Tm.pcs', -5.885, 8.219, 1.059, 26, -9.1, 90, 90, 90]
pcs			= PCSParser(params)
fit			= FitPara()
calculator	= CalcPara()
analysis	= ExplorePara()

pcs.doParse()
fit.PCS(pcs, 1) # fixed metal loc
calculator.PCS(pcs, 'ZYZ')
analysis.buildNumbatTBL(pcs, './cam_all/00001cam_Cterm_Tm_calc.pcs')

### Terbium

print "PCS analysis, Calmodulin N-term domain, Terbium"
params = ['', 'pcs', 'cam_H/00001cam_Nterm.pdb', 'tables/Bertini_2004_Tb.pcs', -5.885, 8.219, 1.059, 37, -14, 90, 90, 90]
pcs			= PCSParser(params)
fit			= FitPara()
calculator	= CalcPara()
analysis	= ExplorePara()

pcs.doParse()
fit.PCS(pcs, 1) # fixed metal loc
calculator.PCS(pcs, 'ZYZ')
analysis.buildNumbatTBL(pcs, './cam_all/00001cam_Nterm_Tb_calc.pcs')

print "PCS analysis, Calmodulin C-term domain, Terbium"
params = ['', 'pcs', 'cam_H/00001cam_Cterm.pdb', 'tables/Bertini_2004_Tb.pcs', -5.885, 8.219, 1.059, 37, -14, 90, 90, 90]
pcs			= PCSParser(params)
fit			= FitPara()
calculator	= CalcPara()
analysis	= ExplorePara()

pcs.doParse()
fit.PCS(pcs, 1) # fixed metal loc
calculator.PCS(pcs, 'ZYZ')
analysis.buildNumbatTBL(pcs, './cam_all/00001cam_Cterm_Tb_calc.pcs')

### Fixed tensor analysis

# Thulium:

# Don't know why I got these, I think they're wrong!
#  1    30.0       -5.4447   +/- 0.728436
#  2    10.0       30.2089   +/- 1.002580
#  3    90.0       42.9950   +/- 2.051151
#  4    90.0      131.6188   +/- 1.865808
#  5    90.0       66.1022   +/- 1.521604

#  1    26.0       25.3790   +/- 0.857698
#  2    -9.1        9.6598   +/- 0.855452
#  3    90.0      149.3937   +/- 0.770878
#  4    90.0      107.6289   +/- 0.933394
#  5    90.0      314.1788   +/- 2.073204

# Terbium:
#  1    30.0       39.1810   +/- 6.141370
#  2    10.0      -13.5686   +/- 3.270938
#  3    90.0       70.5410   +/- 4.517362
#  4    90.0       43.4947   +/- 1.249078
#  5    90.0       60.2376   +/- 10.281537

print "00001 PCS analysis (fixed tensor), Thulium"
#params = ['', 'pcs', 'cam_H/00001cam.pdb', 'tables/Bertini_2004_Tm.pcs', -5.885, 8.219, 1.059, -5.4447, 30.2089, 42.9950, 131.6188, 66.1022]
params = ['', 'pcs', 'cam_H/00001cam.pdb', 'tables/Bertini_2004_Tm.pcs', -5.885, 8.219, 1.059, 25.3790, 9.6598, 149.3937, 107.6289, 314.1788]
pcs			= PCSParser(params)
calculator	= CalcPara()
analysis	= ExplorePara()

pcs.doParse()
calculator.PCS(pcs, 'ZYZ')
analysis.buildNumbatTBL(pcs, './cam_all/00001cam_Th_calc.pcs')

print "00001 PCS analysis (fixed tensor), Terbium"
params = ['', 'pcs', 'cam_H/00001cam.pdb', 'tables/Bertini_2004_Tb.pcs', -5.885, 8.219, 1.059, 39.1810, -13.5686, 70.5410, 43.4947, 60.2376]
pcs			= PCSParser(params)
calculator	= CalcPara()
analysis	= ExplorePara()

pcs.doParse()
calculator.PCS(pcs, 'ZYZ')
analysis.buildNumbatTBL(pcs, './cam_all/00001cam_Tb_calc.pcs')

print "2VO2_aligned PCS analysis (fixed tensor), Thulium"
#params = ['', 'pcs', 'cam_H/2VO2_aligned.pdb', 'tables/Bertini_2004_Tm.pcs', -5.885, 8.219, 1.059, -5.4447, 30.2089, 42.9950, 131.6188, 66.1022]
params = ['', 'pcs', 'cam_H/00001cam.pdb', 'tables/Bertini_2004_Tm.pcs', -5.885, 8.219, 1.059, 25.3790, 9.6598, 149.3937, 107.6289, 314.1788]
pcs			= PCSParser(params)
calculator	= CalcPara()
analysis	= ExplorePara()

pcs.doParse()
calculator.PCS(pcs, 'ZYZ')
analysis.buildNumbatTBL(pcs, './cam_all/2VO2_aligned_Th_calc.pcs')

print "2VO2_aligned PCS analysis (fixed tensor), Terbium"
params = ['', 'pcs', 'cam_H/2VO2_aligned.pdb', 'tables/Bertini_2004_Tb.pcs', -5.885, 8.219, 1.059, 39.1810, -13.5686, 70.5410, 43.4947, 60.2376]
pcs			= PCSParser(params)
calculator	= CalcPara()
analysis	= ExplorePara()

pcs.doParse()
calculator.PCS(pcs, 'ZYZ')
analysis.buildNumbatTBL(pcs, './cam_all/2VO2_aligned_Tb_calc.pcs')

