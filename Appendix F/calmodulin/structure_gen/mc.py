import protocol
import regularize
from potList import PotList
from xplorPot import XplorPot
from ivm import IVM
from monteCarlo import randomizeTorsions
from simulationTools import StructureLoop
from pdbTool import PDBTool

numStructures = 1
pdbStart = "cam.pdb"
pdbTemplate = "./cam_STRUCTURE.pdb"

protocol.initRandomSeed(666)
protocol.loadPDB(pdbStart)
regularize.addUnknownAtoms()
#protocol.initRamaDatabase()

linkers = AtomSel("(resid 1:4) or (resid 76:82) or (resid 147:148)")

dyn = IVM()
dyn.fix( AtomSel("resid 5:75") )
dyn.group( AtomSel("resid 83:146") )

#extraTerms = []
#extraTerms.append( XplorPot('RAMA') )
#regularize.fixupCovalentGeomIVM(verbose=2,extraTerms=extraTerms)
#regularize.fixupCovalentGeomIVM(sel=linkers,verbose=0)

#pdb = PDBTool( 'cam_fixup_rama.pdb' )
#pdb.write()
#exit()

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
