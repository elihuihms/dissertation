import protocol
import regularize
from potList import PotList
from xplorPot import XplorPot
from ivm import IVM
from monteCarlo import randomizeTorsions
from simulationTools import StructureLoop
from pdbTool import PDBTool

numStructures = 10000
pdbStart = "ESCRT1_minimized.pdb"
pdbTemplate = "pdbs/ESCRT1_1_STRUCTURE.pdb"

protocol.initRandomSeed(666)
protocol.loadPDB(pdbStart)
xplor.simulation.deleteAtoms("not known")
regularize.fixupCovalentGeomIVM(verbose=1)

dyn = IVM()
dyn.fix( AtomSel("segid A and (resid 218:385)" ) )
dyn.fix( AtomSel("segid B and (resid 1:117)" ) )
dyn.fix( AtomSel("segid C and (resid 47:213)" ) )
dyn.fix( AtomSel("segid D and (resid 1:81)" ) )

dyn.group( AtomSel("segid A and (resid 9:159)" ) )
dyn.group( AtomSel("segid B and (resid 148:242)" ) )
dyn.group( AtomSel("segid C and (resid 1:34)" ) )

linkers = AtomSel("(segid A and (resid 159:217)) or (segid B and (resid 118:147)) or (segid C and (resid 33:46)) or (segid D and (resid 81:101))")

potList = PotList()
potList.add( XplorPot("BOND") )
potList.add( XplorPot("ANGL") )
potList.add( XplorPot("IMPR") )
potList.add( XplorPot('VDW') )

protocol.torsionTopology(dyn)

def randomize( loopInfo ):
	
	randomizeTorsions(dyn)
	try:
		# When fixupCovalentGeomIVM starts with minimization of all possible covalent restraints,
		# the very small stepsizes will cause this call to fail. Try them again later w/ seed+1
		regularize.fixupCovalentGeomIVM( sel=linkers, useVDW=1, useDynamics=1, verbose=2 )
	except:
		return

	protocol.initMinimize(
	ivm = dyn,
	potList = potList,
	printInterval = 50,
	numSteps = 500)
		
	dyn.run()
	
	# write as PDB, not XPLOR format!
	tmp = pdbTemplate
	pdb = PDBTool( tmp.replace('STRUCTURE',str(loopInfo.count)) )
	pdb.setWriteChainID(True)
	pdb.write()
	
StructureLoop(
	numStructures=numStructures,
	structLoopAction=randomize,
	doWriteStructures=False,
	pdbTemplate=pdbTemplate,
	calcMissingStructs=True,
	).run()
