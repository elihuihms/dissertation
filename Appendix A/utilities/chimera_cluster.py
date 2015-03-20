#!/usr/bin/python
""" Hooks into the UCSF Chimera "Ensemble Cluster" routine
Originally from: http://plato.cgl.ucsf.edu/pipermail/chimera-users/2010-May/005166.html
"""

import time

reftime = time.clock()
def report(s):
	now = time.clock()
	print "%8.2g: %s" % (now - reftime, s)

def main():
	import chimera
	modelList = chimera.openModels.list(modelTypes=[chimera.Molecule])
	subSelection = None		# Change this to CAs or  heavy atoms
	clusterInfo = _cluster(modelList, subSelection)
	saveReps(clusterInfo, "reps.pdb")	# Change file name if needed

def _cluster(modelList, subSelection):
	from chimera import match
	from EnsembleMatch.distmat import DistanceMatrix
	print "Computing distance matrix"
	fulldm = DistanceMatrix(len(modelList))
	report("created distance matrix")
	sameAs = {}
	atoms = [ match._coordArray(_getAtoms(m, subSelection))
			for m in modelList ]
	for i in range(len(modelList)):
		mi = modelList[i]
		if mi in sameAs:
			continue
		ai = atoms[i]
		for j in range(i + 1, len(modelList)):
			aj = atoms[j]
			m = match.Match(ai, aj)
			if m.rms <= 0:
				mj = modelList[j]
				sameAs[mj] = mi
				print "Zero RMSD between %s and %s" % (
						mi.oslIdent(), mj.oslIdent())
			fulldm.set(i, j, m.rms)
	report("filled distance matrix")
	if not sameAs:
		dm = fulldm
		models = modelList
	else:
		dm = DistanceMatrix(len(modelList) - len(sameAs))
		models = []
		indexMap = []
		for i, mi in enumerate(modelList):
			if mi in sameAs:
				continue
			models.append(mi)
			indexMap.append(i)
		for i in range(len(models)):
			im = indexMap[i]
			for j in range(i + 1, len(models)):
				jm = indexMap[j]
				dm.set(i, j, fulldm.get(im, jm))
	print "Using %d of %d models for clustering" % (dm.size, fulldm.size)
	report("pruned distance matrix")

	from EnsembleMatch.nmrclust import NMRClust
	nmrc = NMRClust(dm)
	report("finished clustering")
	id = 0
	cList = []
	for c in nmrc.clusters:
		members = c.members()
		cList.append((len(members), c, members))
	cList.sort()
	cList.reverse()
	clusterInfo = []
	for i, (size, c, members) in enumerate(cList):
		mList = []
		for member in members:
			m = models[member]
			m.clusterId = id
			m.clusterRep = 0
			mList.append(m)
		rep = nmrc.representative(c)
		m = models[rep]
		m.clusterRep = size
		clusterInfo.append((m, mList))
		id += 1
	for mj, mi in sameAs.iteritems():
		mj.clusterId = mi.clusterId
		mj.clusterRep = 0
		clusterInfo[mj.clusterId][1].append(mj)
	print "Generated %d clusters" % id
	for i, (rep, mList) in enumerate(clusterInfo):
		print "Cluster %d: size:%d, rep:%s, members:%s" % (i + 1,
						len(mList), rep.oslIdent(),
						' '.join([m.oslIdent()
								for m in mList]))
	return clusterInfo

def _getAtoms(m, subSelection):
	if not subSelection:
		#atoms = m.sortedAtoms()
		atoms = m.atoms
	else:
		osl = '%s%s' % (m.oslIdent(), subSelection)
		s = selection.OSLSelection(osl)
		wanted = s.vertices(asDict=True)
		#atoms = [ a for a in m.sortedAtoms() if a in wanted ]
		atoms = [ a for a in m.atoms if a in wanted ]
	return atoms

def saveReps(clusterInfo, filename):
	import Midas
	Midas.write([ ci[0] for ci in clusterInfo ],	# list of models to save
			None,				# reference position model
			filename)			# path to output file

if 1:
	main()
else:
	import cProfile
	cProfile.runctx("main()", globals(), locals())