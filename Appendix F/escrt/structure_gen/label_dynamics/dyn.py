import protocol, regularize
from potList import PotList
from xplorPot import XplorPot
from ivm import IVM
from simulationTools import StructureLoop

bathTemp = 500	#K
finalTime = 5	#ps
numStructures = 1000
pdbTemplate = "dyn/ESCRT1_labeled_STRUCTURE.pdb"

protocol.initTopology('protein')
protocol.initParams('protein')

protocol.initStruct("ESCRT1_labeled.psf")
protocol.initCoords("ESCRT1_labeled.sa")
regularize.fixupCovalentGeomIVM( useVDW=1, useDynamics=1, verbose=2 )

label_sel = "((segid A and resid 108) or (segid A and resid 137) or (segid A and resid 223) or (segid A and resid 256) or (segid B and resid 27) or (segid B and resid 65) or (segid B and resid 151) or (segid C and resid 12) or (segid C and resid 173))"

# keep everything rigid except for the spin labels
dyn = IVM()
dyn.fix( AtomSel( "not %s" % label_sel ) )

potList = PotList()
potList.add( XplorPot("BOND") )
potList.add( XplorPot("ANGL") )
potList.add( XplorPot("IMPR") )
potList.add( XplorPot('VDW') )

protocol.torsionTopology(dyn)

def sim( loopInfo ):

	protocol.initDynamics(
	ivm	= dyn,
	bathTemp	= bathTemp,
	initVelocities	= True,
	finalTime	= finalTime,
	potList = potList,
	printInterval	= finalTime*100)
	
	dyn.run()
	
StructureLoop(
	numStructures=numStructures,
	structLoopAction=sim,
	doWriteStructures=True,
	pdbTemplate=pdbTemplate,
	).run()
