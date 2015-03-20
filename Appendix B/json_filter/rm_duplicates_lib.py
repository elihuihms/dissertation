import math
from pointmaps import *
from kabsch import *

"""
Library to make and compare pointmaps from JSON array definitions of AT-TRAP connectivities
Contents:
	addMapPoints()
	makePointMap()
	isUnique()
"""

def addMapPoints( seen, map, chain, index, currX, currY, currR, isCyclic ):
	"""
	Updates the point map with the members bound to the chain object at "index", and recursively calls itself with those bound members
	If the component index in in the seen array, exits
	If isCyclic is enabled, protomers are treated as potentially cyclic
	"""
	
	if( index in seen ):
		return
	else:
		print chain[index]
		print "X: %.3f, Y: %.3f" % (currX,currY)
		map.append( [currX,currY] )
		seen.append( index )
	
	component = chain[index]
	nSites = len(component['sites'])
		
	if( isCyclic ):
		bump = 0
	else:
		bump = 1
	
	for i in range(nSites):
		if (component['sites'][i] != None):
			newX = currX + math.cos( (2.0 * math.pi) * (float(i) / (nSites +bump)) )
			newY = currY + math.sin( (2.0 * math.pi) * (float(i) / (nSites +bump)) )
			newR = currR + math.pi + (2 * math.pi * (float(i) / (nSites +bump)))

			addMapPoints( seen, map, chain, component['sites'][i]/100 , newX, newY, newR, isCyclic )
	pass
	
	return
pass

def mapIterator( map, parent, chain, seen, isCyclic ):
	
	if( isCyclic ):
		bump = 0
	else:
		bump = 1
	
	for i in range(0,len(parent['sites'])):
		if (parent['sites'][i] != None):

			# get the position of the child component in the array			
			child = chain[ parent['sites'][ i ] / 100 ] #integer math
			
			# if it's new append it and determine it's place in the map
			if(child not in seen):
				seen.append( child )
						
				child['x'] = parent['x'] + math.cos( parent['r'] + (2.0 * math.pi * float(i) / (len(parent['sites']) +bump)) )
				child['y'] = parent['y'] + math.sin( parent['r'] + (2.0 * math.pi * float(i) / (len(parent['sites']) +bump)) )
				child['r'] = parent['r'] + (2.0 * math.pi * float(i) / (len(parent['sites']) +bump) ) + math.pi

				map.append([child['x'],child['y'],child['name']])
				
				# recursively check all of the components this component is bound to
				mapIterator(map, child, chain, seen, isCyclic)
			pass
		pass
	pass
pass
	
def makePointMap( chain, isCyclic=True ):
	"""
	Generates a chain schematic consisting of a point array of the chain
	"""
	
	map = []
	seen = []
	
	chain[0]['x'] = 0.0
	chain[0]['y'] = 0.0
	chain[0]['r'] = 0.0
	
	#addMapPoints( seen, map, chain, 0, 0, 0, 0, isCyclic )
	mapIterator( map, chain[0], chain, seen, isCyclic )

	return map
pass

def findDuplicateByDist( distMaps, chain, cutoff=1E-10, cyclic=True ):
	"""
	Compares the provided chain against all of the previously observed chain pointmaps using the distance of the points in the map from the map's COM.
	Returns the index of the map in distMaps that matches the provided chain, or -1 if there is no match.
	"""
	
	# generate the 2D pointmap for the chain connectivity
	testM = makePointMap(chain, cyclic)
	
	# get the distances of each point in the map from the map's COM
	testD = getMapDistances( testM )
	
	# go through all the maps we have, and see if the testmap superimposes on any of them
	for dist in distMaps:
		
		if( len(dist) != len(testD) ):
			continue
		
		# add up the total distance discrepancy
		diff = 0.0
		for i in range( len(testD) ):
			diff += math.fabs(testD[i] - dist[i])
		diff = diff / len(dist)
		
		if( diff < cutoff ):
			return distMaps.index(dist)
	pass
	
	distMaps.append( testD )
	return -1

pass

def findDuplicateByMap( uniqueMaps, chain, cutoff=1E-10, cyclic=True, mirror=True ):
	"""
	Compares the provided chain against all of the previously observed chain pointmaps by attempting to superimpose a 2D representation of the map upon maps present in the second argument.
	Returns the index of the map in distMaps that matches the provided chain, or -1 if there is no match.
	"""
	
	# generate the 2D pointmap for the chain connectivity
	testMap = makePointMap(chain, cyclic)
		
	# rotate the map such that the point furthest from the origin lies at 1,0
	normalizeMap( testMap )

	# go through all the maps we have, and see if the testmap superimposes on any of them
	for map in uniqueMaps:
	
		if( len(map) != len(testMap) ):
			continue
		
		ssd = getSSD( map, testMap )
#		ssd = getKabschRMSD( map, testMap )

		if (ssd < cutoff):
			return uniqueMaps.index(map)
	pass
	
	# if we're not going to check for mirror images, return now
	if( not mirror ):
		uniqueMaps.append( testMap )
		return True	
	
	# reflect the map to check for mirror image superimpositions
	reflectMapX( testMap )

	for map in uniqueMaps:
	
		if( len(map) != len(testMap) ):
			continue
		
		ssd = getSSD( map, testMap )
#		ssd = getKabschRMSD( map, testMap )

		if (ssd < cutoff):
			return uniqueMaps.index(map)
	pass

	uniqueMaps.append( testMap )
	return -1

pass
