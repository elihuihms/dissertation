import numpy

def getKabschRMSD( map1, map2 ):
	"""
	Applies the Kabsch algorithm to superimpose two pointmaps
	Taken from the pyrosetta implementation here: http://www.pyrosetta.org/scripts
	"""
		
	L = len(map1)
	assert L > 0
	assert L == len(map2)
	
	# must alway center the two proteins to avoid affine transformations
	#     Center the two proteins to their selections
	COM1 = numpy.sum(map1,axis=0) / float(L)
	COM2 = numpy.sum(map2,axis=0) / float(L)
	map1 -= COM1
	map2 -= COM2
	
	# Initial residual, see Kabsch.
	E0 = numpy.sum( numpy.sum(map1 * map1,axis=0),axis=0) + numpy.sum( numpy.sum(map2 * map2,axis=0),axis=0)
	
	# This beautiful step provides the answer.  V and Wt are the orthonormal
	# bases that when multiplied by each other give us the rotation matrix, U.
	# S, (Sigma, from SVD) provides us with the error!  Isn't SVD great!
	V, S, Wt = numpy.linalg.svd( numpy.dot( numpy.transpose(map2), map1))
	
	# we already have our solution, in the results from SVD.
	# we just need to check for reflections and then produce
	# the rotation.  V and Wt are orthonormal, so their det's
	# are +/-1.
	reflect = float(str(float(numpy.linalg.det(V) * numpy.linalg.det(Wt))))
	
	if reflect == -1.0:
		S[-1] = -S[-1]
		V[:,-1] = -V[:,-1]
	
	RMSD = E0 - (2.0 * sum(S))
	RMSD = numpy.sqrt(abs(RMSD / L))
	
	return RMSD
	
	#U is simply V*Wt
	U = numpy.dot(V, Wt)
	
	# rotate and translate the molecule
	map2 = numpy.dot((molsel2 - COM2), U)
	map2 = map2.tolist()
	# center the molecule
	map1 = molsel1 - COM1
	map1 = map1.tolist()
	
pass