import math

def reorderMap( map ):
	"""
	Reorders the elements in a map based upon their distance from the origin
	"""
	
	def dist( a, b ):
		return cmp( math.sqrt(a[0]**2 + a[1]**2), math.sqrt(b[0]**2 + b[1]**2) )
		
	map.sort( dist )

	return
pass

def getUnitAngle( point ):

	angle = math.atan( math.fabs(point[1]) / math.fabs(point[0]) )

	if (point[0] < 0) and (point[1] > 0):
		angle = math.pi - angle
	elif (point[0] < 0) and (point[1] < 0):	
		angle = math.pi + angle
	elif (point[0] > 0) and (point[1] < 0):	
		angle = (2*math.pi) - angle
	
	return angle	
pass

def centerMap( map ):
	"""
	Centers an pointmap so that its centroid is at 0,0
	"""
	
	size = len(map)
	x_avg = 0.0
	y_avg = 0.0
	
	for i in range( size ):
		x_avg += map[i][0]
		y_avg += map[i][1]
	
	x_avg = x_avg / size
	y_avg = y_avg / size

	for i in range( size ):
		map[i][0] -= x_avg
		map[i][1] -= y_avg
	
	return
		
pass

def getMapThetaSSD( map1, map2, reOrder=False ):
	"""
	Returns a theta value that minimizes the sum-square of distances between two pointmaps
	See http://en.wikipedia.org/wiki/Procrustes_analysis for more info
	"""

	size = len(map1)
	assert size == len(map2)
	
	if( reOrder ):
		reorderMap( map1 )
		reorderMap( map2 )
	
	a_sum = 0.0
	b_sum = 0.0
	for i in range( size ):
		a_sum += (map2[i][0] * map1[i][1]) - (map2[i][1] * map1[i][0])
		b_sum += (map2[i][0] * map1[i][0]) + (map2[i][1] * map1[i][1])

	return math.atan( a_sum / b_sum )
pass

def rotateMap( map, theta ):
	"""
	Rotates a map by the provided theta
	"""
	
	for i in range( len(map) ):
		old_x = map[i][0]
		old_y = map[i][1]
		map[i][0] = (old_x * math.cos(theta)) - (old_y * math.sin(theta))
		map[i][1] = (old_x * math.sin(theta)) + (old_y * math.cos(theta))
		
	return
pass

def reflectMapX( map ):
	"""
	Reflects a map across the x axis
	"""
	
	for i in range( len(map) ):
		map[i][1] = -1.0 * map[i][1]
	
	return
pass

def reflectMapY( map ):
	"""
	Reflects a map across the Y axis
	"""
	
	for i in range( len(map) ):
		map[i][0] = -1.0 * map[i][0]
	
	return
pass

def getMapDistances( map ):
	"""
	Returns an ordered list of the distances of each point in the map from the map's COM
	"""

	# center the pointmap at its center of mass (COM)
	centerMap( map )
	
	ret = []
	for p in map:
		ret.append( math.sqrt(p[0]**2 + p[1]**2) )
		
	ret.sort()
	
	return ret

pass

def normalizeMap( map ):
	"""
	Rotates the map until the farthest point from the origin lies upon the positive x-axis
	"""

	# center the pointmap at its center of mass (COM)
	centerMap( map )

	# order the points in the map such that the point nearest the COM is first
	reorderMap( map )
		
	# get the unit angle of rotation for the farthest point from the origin for both maps
	angle = getUnitAngle( map[ len(map) -1] )
	
	# rotate the map such that the point farthest from the origin is along the (positive) x-axis
	rotateMap( map, -1 * angle )
		
	return
	
pass

def getSSD( map1, map2 ):
	"""
	Calculates the sum square of distance (Procrustes distance) for corresponding points in two maps 
	"""
	
	size = len(map1)
	assert size == len(map2)
	
	sum = 0.0
	for i in range( size ):
		sum += ( (map2[i][0] - map1[i][0])**2 + (map2[i][1] - map1[i][1])**2 )
	
	return math.sqrt( sum )
pass

def printMap( map, delim="\t" ):
	"""
	Returns a string with the map coordinates
	"""
	
	ret = ''
	for i in range( len(map) ):
		ret += "%.3f%s%.3f\n" % (map[i][0],delim,map[i][1])
		
	return ret
pass

def getMinDistance( map ):
	"""
	Gets the minimum distance between any two points in the map
	"""

	minDist = 1E9
	for i in range( len(map) ):
		for j in range( len(map) ):
			if( i != j ):

				dist = math.sqrt( (map[i][0] - map[j][0])**2 + (map[i][1] - map[j][1])**2 )
				if( dist < minDist ):
					minDist = dist
	return minDist
pass

def printTDMap( map ):
	for i in range( len(map) ):
		print "%.3f\t%.3f\t%s" % (map[i][0],map[i][1],map[i][2])
pass
