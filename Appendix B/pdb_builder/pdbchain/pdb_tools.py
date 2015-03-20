import re

"""General-purpose homegrown PDB parser
Last modified: 01.04.2012 E. Ihms"""

def parsePDB( file ):
	""" Reads the specified file and returns an array containing all ATOM records. Ignores anything that's not an ATOM or HETATM record """
	
	# list container initialization
	list = []

	# no error checking (for now)
	f = open(file, 'r')	
	for line in f:
		# regex the string
		if (line[0:4] == 'ATOM') or (line[0:6] == 'HETATM'):
			list.append({'i':int(line[6:11]),'name':line[12:16].strip(),'res':{'num':int(line[22:26]),'type':line[17:20].strip(),'chain':line[21]},'coords':[float(line[30:37]),float(line[38:45]),float(line[46:53])]})
		
	f.close()
	
	print ("%i ATOMs read." % (len(list)))
	
	return list
			
def writePDB( file, atomlist, remarks=None ):
	""" Writes a provided (well-formed, see list output format from parsePDB()) array to a specifed PDB file path """
	
	# pdb format specification
	fmt = "ATOM  %5i %4s %3s %1s%4i    %8.3f%8.3f%8.3f\n"
	
	f = open(file, 'w')
	
	if (remarks != None):
		for i in range(len(remarks)):
			f.write("REMARK   %i %s\n" % (i, remarks[ i ]))

	chainlist = ('A','B','C','D','E','F','G','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z')

	atomcounter = 0
	chaincounter = 0
	for atom in atomlist:
		
		# boolean false as TER
		if( atom == False ):
			f.write("TER\n")
			chaincounter+=1
		else:
			f.write(fmt % (atomcounter,atom['name'].center(4,' '),atom['res']['type'],chainlist[ chaincounter ],atom['res']['num'],atom['coords'][0],atom['coords'][1],atom['coords'][2]) )
			atomcounter+=1
		
	f.write("END\n")
	f.close()
	
	print ("%i ATOMs written." % (len(atomlist)))
	
	return
	
def getDist( point1, point2 ):
	""" Returns the euclidian distance between two cartesian points """
	
	return sqrt( (point1[0] - point2[0])**2 + (point1[1] - point2[1])**2 + (point1[2] - point2[2])**2 )

def getDRMSD( atomname, pdb1, pdb2 ):
	""" Returns the DRMSD between two PDBs of the provided atomname """
	
	#
	# Reference: Rozycki et al. "SAXS Ensemble Refinement of ESCRT-III CHMP3 Conformational Transiions", Cell Structure (2011) 
	# doi: 10.1016/j.str.2010.10.006
	#
	
	len1 = 0
	points1 = []
	len2 = 0
	points2 = []
	
	for i in range( len(pdb1) ):
		if ( pdb1[ i ]['name'] == atomname ):
			points1.append( pdb1[ i ]['coords'] )
			len1+=1
	
	for i in range( len(pdb2) ):
		if ( pdb2[ i ]['name'] == atomname ):
			points2.append( pdb2[ i ]['coords'] )
			len2+=1
	
	if( len1 != len2 ) or (len1 == 0):
		return None
	
	sum = 0
	count = 0
	for i in range( len1 ):
		for j in range( i+1, len1 ):
			sum += (getDist( points1[ i ], points1[ j ] ) - getDist( points2[ i ], points2[ j ] ) )**2
			count += 1
			
	return sqrt( sum / count )
		
	
	
	
	
	
	
	
	
						
			