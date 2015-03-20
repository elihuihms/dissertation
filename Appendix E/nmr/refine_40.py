
xplor.requireVersion("2.25")

#
# slow cooling protocol in torsion angle space for protein G. Uses 
# NOE, RDC, J-coupling restraints.
#
# this version refines from a reasonable model structure.
#
# CDS 2005/05/10
#

#
# Modified for SAXS refinement of anti-TRAP, starting from Craig's structure deposited in the BMRB and using the available BMRB restraints
#
# ECI 2012/04/26
#

(opts,args) = xplor.parseArguments(["quick","v"]) # check for command-line typos

quick=False
verbosity = False
for opt in opts:
    if opt[0]=="quick":  #specify -quick to just test that the script runs
        quick=True
        pass
    elif opt[0]=="v": #specify -v to make the script print a bunch of stuff, esp in the initialization routines
    	verbosity=True
    	pass
    pass


outFilename = "SCRIPT_STRUCTURE.sa"
numberOfStructures=100

if quick:
    numberOfStructures=3
    pass

# protocol module has many high-level helper functions.
#
import protocol
protocol.initRandomSeed(3421)   #explicitly set random seed

#
# annealing settings
#

command = xplor.command

protocol.initParams("protein")

protocol.initParams("ion.par")
protocol.initTopology("ion.top")

protocol.initStruct("gen_psf/at_trimer.psf")
protocol.initCoords("coordinates/block_487157_e.pdb", verbose=verbosity)
#protocol.loadPDB("coordinates/input.pdb")

protocol.addUnknownAtoms()
protocol.fixupCovalentGeom(maxIters=100,useVDW=1, verbose=verbosity)

#
# a PotList contains a list of potential terms. This is used to specify which
# terms are active during refinement.
#
from potList import PotList
potList = PotList()
crossTerms = PotList()

# parameters to ramp up during the simulated annealing protocol
#
from simulationTools import MultRamp, StaticRamp, InitialParams

rampedParams=[]
highTempParams=[]

# compare atomic Cartesian rmsd with a reference structure
#  backbone and heavy atom RMSDs will be printed in the output
#  structure files
#
from posDiffPotTools import create_PosDiffPot
refRMSD = create_PosDiffPot("refRMSD","name CA or name C or name N", pdbFile='coordinates/block_487157_e.pdb', cmpSel="not name H*")
crossTerms.append(refRMSD)

# dipolar coupling restraints for protein amide NH.  
#
# I've done a bit of hackery from the original gb1_rdc refine.py:
# calcTensor() will optimize Da and R terms for the alignment media given the existing reasonable structure and experimental RDCs
# calcTensorOrientation() will then use the calculated Da and Rh and determine the orientation tensor for the media
#
# 2012.04.26 ECI
#

from rdcPotTools import create_RDCPot, scale_toNH
from varTensorTools import addAxisAtoms, create_VarTensor, calcTensor, calcTensorOrientation

media={}
rdcs = PotList('RDC') 
for (medium,expt,file,scale) in [('phage','NH' ,'restraints/rdc.tbl', 1)]:
	
	name = "%s_%s"%(medium,expt)
	axis = addAxisAtoms()
	media[ medium ] = create_VarTensor(name,axis=axis)
	
	rdc = create_RDCPot(name,file, media[ medium ])
	calcTensor( media[ medium ] )
	calcTensorOrientation(media[medium])
	
	if( verbosity == True ):
	    print "RDC calcTensor() results for RDCPot '%s': " % (name)
	    print "Da = %.2f, Rh = %.3f" % (media[medium].Da(), media[medium].Rh())
		
    #1) scale prefactor relative to NH
    #   see python/rdcPotTools.py for exact calculation
    # scale_toNH(rdc) - not needed for these datasets -
    #                        but non-NH reported rmsd values will be wrong.

    #3) Da rescaling factor (separate multiplicative factor)
    # scale *= ( 1. / rdc.oTensor.Da(0) )**2
	rdc.setScale(scale)
	rdc.setShowAllRestraints(1) #all restraints are printed during analysis
	rdc.setThreshold(1.5)       # in Hz
	rdcs.append(rdc)
	pass

potList.append(rdcs)
rampedParams.append( MultRamp(0.05,5.0, "rdcs.setScale( VALUE )") )
    
# set up NOE potential
noe=PotList('NOE')
potList.append(noe)
from noePotTools import create_NOEPot
for (name,scale,file) in [('noe_simpl',1,"restraints/noe_simple_no50HD1.tbl"),
                          ('noe_ambig',1,"restraints/noe_ambi.tbl"),
                          ('zinc_dist',1,"restraints/zn_distances.tbl")]:
    pot = create_NOEPot(name,file)
    pot.setPotType("soft") # - if you think there may be bad NOEs
    pot.setScale(scale)
    noe.append(pot)
rampedParams.append( MultRamp(2,30, "potList['NOE'].setScale( VALUE )") )

# Set up dihedral angles
from xplorPot import XplorPot
protocol.initDihedrals("restraints/dihedrals.tbl",
                       #useDefaults=False  # by default, symmetric sidechain
                                           # restraints are included
                       )                      

potList.append( XplorPot('CDIH') )
highTempParams.append( StaticRamp("potList['CDIH'].setScale(10)") )
rampedParams.append( StaticRamp("potList['CDIH'].setScale(200)") )
# set custom values of threshold values for violation calculation
#
potList['CDIH'].setThreshold( 5 ) #5 degrees is the default value, though

# Dynamically determined H-bond database
# 2012.04.26 ECI

# hbdb - bb hbonds from database
#
protocol.initHBDB()
potList.append( XplorPot('HBDB') )

#
# I don't know if this DB should be used for the refinement, so commenting out for now
# 2012.04.26 ECI
#

#Rama torsion angle database
#
#protocol.initRamaDatabase()
#potList.append( XplorPot('RAMA') )
#rampedParams.append( MultRamp(.002,1,"potList['RAMA'].setScale(VALUE)") )

#
# setup parameters for atom-atom repulsive term. (van der Waals-like term)
#
potList.append( XplorPot('VDW') )
rampedParams.append( StaticRamp("protocol.initNBond()") )
rampedParams.append( MultRamp(0.9,0.8,
                              "command('param nbonds repel VALUE end end')") )
rampedParams.append( MultRamp(.004,4,
                              "command('param nbonds rcon VALUE end end')") )
# nonbonded interaction only between CA atoms
highTempParams.append( StaticRamp("""protocol.initNBond(cutnb=100,
                                                        rcon=0.004,
                                                        tolerance=45,
                                                        repel=1.2,
                                                        onlyCA=1)""") )

potList.append( XplorPot("BOND") )
potList.append( XplorPot("ANGL") )
potList['ANGL'].setThreshold( 5 )
rampedParams.append( MultRamp(0.4,1,"potList['ANGL'].setScale(VALUE)") )
potList.append( XplorPot("IMPR") )
potList['IMPR'].setThreshold( 5 )
rampedParams.append( MultRamp(0.1,1,"potList['IMPR'].setScale(VALUE)") )

#      
# SAXS term
#
# Had to add aSelection terms to exclude Zn atoms, due to lack of formfactors in the db for this atom type
# 2012.04.25 EI
#

from solnXRayPotTools import create_solnXRayPot
import solnXRayPotTools

xray=create_solnXRayPot('SAXS',aSelection='not PSEUDO and not name H* and not name Zn*',experiment='restraints/saxs/als_02272011_fAT_3_23.dat',numPoints=100,normalizeIndex=-3,preweighted=False)                
solnXRayPotTools.useGlobs(xray)
xray.setNumAngles(100)
xray.setScale(40)
xray.setCmpType("plain")
potList.append(xray)

#
#correct I(q) to higher accuracy, and include solvent contribution corrections
#stride=10 specifies that this fit is performed every 10th temperature during
#simulated annealing.
#

from solnScatPotTools import fitParams

xrayCorrect=create_solnXRayPot('SAXS-c',aSelection='not PSEUDO and not name H* and not name Zn*', experiment='restraints/saxs/als_02272011_fAT_3_23.dat',numPoints=100,normalizeIndex=-3,preweighted=False)
xrayCorrect.setNumAngles(100)
crossTerms.append( xrayCorrect )
rampedParams.append( StaticRamp("fitParams(xrayCorrect);xray.calcGlobCorrect(xrayCorrect.calcd())", stride=10) )

#corrects I(q) to higher accuracy, and include solvent contribution corrections
# Give atoms uniform weights, except for the anisotropy axis
#
protocol.massSetup()

#
# Symmetry restraints
#
# From: http://nmr.cit.nih.gov/xplor-nih/doc/current/python/ref/distSymmTools.html
# From: http://www.mail-archive.com/xplor-nih@nmr.cit.nih.gov/msg01226.html
#
# 2012.04.26 ECI
#

from distSymmTools import create_DistSymmPot, genPolyRestraints
symmPot = create_DistSymmPot('SYMM')
for r in genPolyRestraints( segids=['A','B','C'], resids=range(1,54)  ):
	symmPot.addRestraint( r )
	pass

potList.append( symmPot )
rampedParams.append( StaticRamp("potList['SYMM'].setScale(75)") )

#
# NCS restraints (The old way to do it)
#
# Craig used weighting of 75
#
# From http://www.mail-archive.com/xplor-nih@nmr.cit.nih.gov/msg00664.html
#xplor.command(r"""
#ncs restraints
#	initialize
#	group
#		equi ( segid A ) 
#		equi ( segid B ) 
#		equi ( segid C ) 
#		weight=1
#	end
#	? {* print the NCS relations when starting *}
#end
#""")
#potList.append( XplorPot("NCS") )
#rampedParams.append( StaticRamp("potList['NCS'].setScale(75)") )

# IVM setup
#   the IVM is used for performing dynamics and minimization in torsion-angle
#   space, and in Cartesian space.
#
from ivm import IVM
dyn = IVM()

# initially minimize in Cartesian space with only the covalent constraints.
#   Note that bonds, angles and many impropers can't change with the 
#   internal torsion-angle dynamics
#   breaks bonds topologically - doesn't change force field
#
#dyn.potList().add( XplorPot("BOND") )
#dyn.potList().add( XplorPot("ANGL") )
#dyn.potList().add( XplorPot("IMPR") )
#
#dyn.breakAllBondsIn("not resname ANI")
#import varTensorTools
#for m in media.values():
#    m.setFreedom("fix")                 #fix tensor parameters
#    varTensorTools.topologySetup(dyn,m) #setup tensor topology
#
#protocol.initMinimize(dyn,numSteps=1000)
#dyn.run()

# reset ivm topology for torsion-angle dynamics
#
dyn.reset()

for m in media.values():
#    m.setFreedom("fixDa, fixRh")        #fix tensor Rh, Da, vary orientation
    m.setFreedom("varyDa, varyRh")      #vary tensor Rh, Da, vary orientation
protocol.torsionTopology(dyn)

# minc used for final cartesian minimization
#
minc = IVM()
protocol.initMinimize(minc)

for m in media.values():
    m.setFreedom("varyDa, varyRh")    #allow all tensor parameters float here
    pass
protocol.cartesianTopology(minc)



# object which performs simulated annealing
#
from simulationTools import AnnealIVM
init_t  = 3000.     # Need high temp and slow annealing to converge
cool = AnnealIVM(initTemp =init_t,
                 finalTemp=25,
                 tempStep =12.5,
                 ivm=dyn,
                 rampedParams = rampedParams)

def accept(potList):
    """
    return True if current structure meets acceptance criteria
    """
    if potList['NOE'].violations()>0:
        return False
    if potList['RDC'].rms()>1.2: #this might be tightened some
        return False
    if potList['CDIH'].violations()>0:
        return False
    if potList['BOND'].violations()>0:
        return False
    if potList['ANGL'].violations()>0:
        return False
    if potList['IMPR'].violations()>1:
        return False
    
    return True

def calcOneStructure(loopInfo):
    """ this function calculates a single structure, performs analysis on the
    structure, and then writes out a pdb file, with remarks.
    """

    # initialize parameters for high temp dynamics.
    InitialParams( rampedParams )
    # high-temp dynamics setup - only need to specify parameters which
    #   differfrom initial values in rampedParams
    InitialParams( highTempParams )

    # high temp dynamics
    #
    protocol.initDynamics(dyn,
                          potList=potList, # potential terms to use
                          bathTemp=init_t,
                          initVelocities=1,
                          finalTime=50,    # stops at 50ps or 5000 steps
                          numSteps=5000,   # whichever comes first
                          printInterval=100)

    dyn.setETolerance( init_t/100 )  #used to det. stepsize. default: t/1000 
    dyn.run()

    # initialize parameters for cooling loop
    InitialParams( rampedParams )


    # initialize integrator for simulated annealing
    #
    protocol.initDynamics(dyn,
                          potList=potList,
                          numSteps=200,       #at each temp: 200 steps or
                          finalTime=.5 ,       # .5ps, whichever is less
                          printInterval=100)

    # perform simulated annealing
    #
    cool.run()
              
              
    # final torsion angle minimization
    #
    protocol.initMinimize(dyn,
                          printInterval=50)
    dyn.run()

    # final all- atom minimization
    #
    protocol.initMinimize(minc,
                          potList=potList,
                          dEPred=10)
    minc.run()

    #do analysis and write structure
    loopInfo.writeStructure(potList)
    pass



from simulationTools import StructureLoop, FinalParams
StructureLoop(numStructures=numberOfStructures,
              pdbTemplate=outFilename,
              structLoopAction=calcOneStructure,
              genViolationStats=1,
              averagePotList=potList,
#              averageSortPots=[potList['BOND'],potList['ANGL'],potList['IMPR'],
#                               noe,rdcs,potList['CDIH']],
              averageCrossTerms=crossTerms,
              averageTopFraction=0.2, #report only on best 50% of structs
              averageContext=FinalParams(rampedParams),
              averageFilename="SCRIPT_ave.pdb",    #generate regularized ave structure
              averageFitSel="name CA",
              averageCompSel="not resname ANI and not name H*"     ).run()

