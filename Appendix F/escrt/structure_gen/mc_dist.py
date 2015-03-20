import protocol
import regularize
import random
from atomSel import AtomSel
from atomSelAction import minDistance
from potList import PotList
from xplorPot import XplorPot
from noePotTools import create_NOEPot
from ivm import IVM
from monteCarlo import randomizeTorsions
from simulationTools import StructureLoop
from pdbTool import PDBTool

numStructures = 2
startStructure = 10002
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

distPotTuples = (
	(
		'VPS23',
		'resid 108 and segid A and name CA',
		'resid 256 and segid A and name CA',
		(25.9,5.1,5.1),
		(48.4,5.2,5.2)
	),(
		'VPS37',
		'resid  12 and segid C and name CA',
		'resid 223 and segid A and name CA',
		(24.7,4.1,4.1),
		(42.7,4.3,4.3)
	),(
		'VPS28',
		'resid  65 and segid B and name CA',
		'resid 151 and segid B and name CA',
		(21.9,4.4,4.4),
		(40.7,6.4,6.4)
	)
)

def makeRestraint( sel1, sel2, d ):
	return "assign (%s) (%s) %d %d %d" % (sel1,sel2,d[0],d[1],d[2])

distPots = []
for (name,sel1,sel2,low,high) in distPotTuples:
	distPots.append( create_NOEPot('%s_L'%name,restraints=makeRestraint(sel1,sel2,low)) )
	distPots[-1].setPotType("log")
	distPots[-1].setAveType("center")
	distPots.append( create_NOEPot('%s_H'%name,restraints=makeRestraint(sel1,sel2,high)) )
	distPots[-1].setPotType("log")
	distPots[-1].setAveType("center")
for pot in distPots:
	potList.append( pot )

protocol.torsionTopology(dyn)

def checkdistPots():
	for r in distPotTuples:
		d = minDistance(AtomSel(r[1]),AtomSel(r[2]))
		print "CHECKING RESTRAINT \"%s\" D: %d" % (r[0],d)

		if( d < r[3][0]-r[3][1] ):
			return False
		if( d > r[4][0]+r[4][2] ):
			return False
		if( d > r[3][0]+r[3][2] and d < r[4][0]-r[4][1] ):
			return False

	return True

def randomize( loopInfo ):

	randomizeTorsions(dyn)
	try:
		# When fixupCovalentGeomIVM starts with minimization of all possible covalent restraints,
		# the very small stepsizes will cause this call to fail.
		regularize.fixupCovalentGeomIVM( sel=linkers, useVDW=1, useDynamics=1, verbose=0 )
	except:
		print "RECALCULATING - fixupCovalentGeom FAIL"
		randomize( loopInfo )

	for i in range(0,len(distPots),2):
		if( random.random() < 0.5 ):
			distPots[ i ].setScale(1.0)
			distPots[i+1].setScale(0.0)
		else:
			distPots[ i ].setScale(0.0)
			distPots[i+1].setScale(1.0)

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

	if checkdistPots():
		pdb.write()
	else:
		print "RECALCULATING - checkdistPots FAIL"
		randomize( loopInfo )

StructureLoop(
	numStructures=numStructures,
	startStructure=startStructure,
	structLoopAction=randomize,
	doWriteStructures=False,
	pdbTemplate=pdbTemplate,
	calcMissingStructs=True,
	).run()
