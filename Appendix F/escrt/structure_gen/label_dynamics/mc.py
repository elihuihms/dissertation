import protocol
import regularize
from potList import PotList
from xplorPot import XplorPot
from ivm import IVM
from monteCarlo import randomizeTorsions
from simulationTools import StructureLoop

numStructures = 1000
pdbTemplate = "mc/ESCRT1_labeled_STRUCTURE.pdb"

protocol.initTopology('protein')
protocol.initParams('protein')

protocol.initStruct("ESCRT1_labeled.psf")
protocol.initCoords("ESCRT1_labeled.sa")

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

def randomize( loopInfo ):
	
	randomizeTorsions(dyn)
	regularize.fixupCovalentGeomIVM( sel=label_sel, useVDW=1, useDynamics=1, verbose=2 )
	
	protocol.initMinimize(
	ivm = dyn,
	potList = potList,
	printInterval = 50,
	numSteps = 500)
		
	dyn.run()

StructureLoop(
	numStructures=numStructures,
	structLoopAction=randomize,
	doWriteStructures=True,
	pdbTemplate=pdbTemplate,
	).run()
