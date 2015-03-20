from numpy import *
from copy import deepcopy
from json import loads
import re

from pdb_tools import parsePDB,writePDB

def readMatrices( filename ):
	""" Reads a matrix file containing the names of the components and their transformation matrices """
	
	f = open(filename, 'r')	
	if( f == None ):
		return (None, None)
		
	lines = f.readlines()
	f.close()
	
	# get the list of components from the first line of the matrix file
	string = lines[0].strip()
	components = string.split("\t");
	
	# create the component transformation matrices
	matrices = []
	for i in range( len(components) ):
		matrices.append( [] )
	
	for i in range( 1, len(lines) ):
		obj = re.search( "^(\S+\.pdb)\s+(\S+\.pdb)", lines[i] )
		if( obj != None):
			name = obj.group(1)
			
			if( name not in components ):
				print "Error reading matrix.txt on line %i, unrecognized component '%s'" % (i+1, name )
				return (None, None)
			
			matrix = []
			t = []
			for j in range( 1,5 ):
				
				# grep out the X,Y,Z transformates
				obj = re.search( "^(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)", lines[ i+j ] )
				
				if( obj == None ):
					print "Error reading matrix.txt on line %i" % (i+j+1)
					return (None, None)
				else:
					x = float(obj.group(1))
					y = float(obj.group(2))
					z = float(obj.group(3))
					
					if( j == 4):
						matrix.append( [ x, y, z, 1.0] )
					else:
						matrix.append( [ x, y, z, 0.0] )
			
			matrices[ components.index( name ) ].append( matrix )
			i += j

	return (components,matrices)

def txformPDB( list, matrix ):
	""" Applies a single structural transform based on a chimera-style 3x4 rotation/translation matrix """
	
	for atom in list:
		# generate a homogenous coordinate
		coords = array( [ atom['coords'][0], atom['coords'][1], atom['coords'][2], 1 ] )
		coords = dot(coords,matrix)

		# save back to the atom object
		atom['coords'][0] = coords[0]
		atom['coords'][1] = coords[1]
		atom['coords'][2] = coords[2]
		
	return
	
def makeChainMatrices( matrices, chain ):
	
	# chain indexes of already cached components
	seen = [0]
	
	# 4x4 identity matrix
	I_matrix = array([ [1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1] ])
	
	# first component is untransformed
	chain[0]['matrix'] = I_matrix
	
	# recursively iterate over the chain
	chainIterator( matrices, 0, chain, seen )

	return


def chainIterator( matrices, parent, chain, seen ):
	""" Recursive iterator that goes through the components of the chain, assigning transformation matrices as it proceeds """
	
	#component: {'depth':0,'type':0,'name':'name','sites':[]}
	for i in range(len(chain[ parent ]['sites'])):
		if (chain[ parent ]['sites'][i] != None):

			# get the position of the child component in the array			
			child = chain[ parent ]['sites'][ i ] / 100 #integer math
			
			# if it's new append it and apply the appropriate matrix
			if(child not in seen):
				seen.append( child )
								
				# use the appropriate matrix
				matrix = matrices[ chain[ parent ]['type'] ][ i ] #(i + site) % len(TRAP_matrix)

				# transformation matrix is the product of the parent's matrix plus the additional positioning transformation
				chain[ child ]['matrix'] = dot( matrix, chain[ parent ]['matrix'] )
				
				# recursively check all of the components this component is bound to
				chainIterator(matrices, child, chain, seen)
				
	return

def makeModelFromJSON( matrices, string, TRAP_pdb, AT_pdb ):
	""" Generates a PDB from a TRAP+AT chain as specified in the passed JSON string """
	
	# decode the JSON string into a python array
	try:
		chain = loads(string)
	except:
		print "The JSON parser ran into an error."
		print string
		return
	
	if(len(chain) < 1):
		print "A malformed JSON string was provided."
		return

	# assign the component transformation matrices
	makeChainMatrices( matrices, chain )

	# initialize the components of the PDB
	remarks = [string]
	atoms = []
	model = []
	
	# generate an array of transformed structures, placed in the atoms[] container
	pdb_mw = 0
	for i in range(len(chain)):
		
		if (chain[i]['type'] == 0):
			atoms.append( deepcopy(TRAP_pdb) )
			remarks.append("COMPONENT:TRAP")
			pdb_mw += 91612.4
		else:
			atoms.append( deepcopy(AT_pdb) )
			remarks.append("COMPONENT:AT")
			pdb_mw += 16948.5
			
		txformPDB(atoms[i], chain[i]['matrix'])
		
		# append the atoms of the current structure to the output model
		model.extend(atoms[i])
		
		# use boolean False as a TER
		model.append( False )
		
	remarks.append( "MW:%.1f" % pdb_mw )
		
	return model,remarks
	
def writePDBFromJSON( matrices, json, filename, TRAP_pdb, AT_pdb ):
	""" Writes to file a TRAP+AT chain as specified in the passed JSON string """
	
	(atomlist, remarks) = makeModelFromJSON( matrices, json, TRAP_pdb, AT_pdb )
	writePDB( filename, atomlist, remarks )
	
	return
	
