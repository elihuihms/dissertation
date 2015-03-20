#! /usr/bin/env python

# Based on code from Pierre Poulain, Justine Guegan, and Edithe Selwa
# last update: 20110414

import numpy
from math import sqrt
from Bio.PDB.PDBParser import PDBParser

def getAtomCoordsBio(path,modelID=None,chainID=None,startRes=None,endRes=None,atomName=None,CAonly=False):
	parser=PDBParser(PERMISSIVE=True,QUIET=True)
	structure=parser.get_structure('', path )

	xyz = []
	for model in structure:
		if (model.id!=modelID) and (modelID!=None):
			continue

		for chain in model:
			if (chain.id!=chainID) and (chainID!=None):
				continue

			for residue in chain:

				if (residue.id[1]<startRes) and (startRes!=None) :
					continue
				if (residue.id[1]>endRes) and (endRes!=None):
					continue

				for atom in residue:

					if (CAonly and (atom.name=='CA')) or (atom.name==atomName):
						xyz.append( atom.get_coord() )

	return xyz

def getAtomCoords(file,chainID=None,startRes=None,endRes=None,atomName='CA',modelID=None):

	f = open(file, 'r')

	ret, toggle = [], True

	line = f.readline()
	while( line ):

		if (line[0:5] == 'MODEL'):
			if (int(line[6:]) == modelID):
				toggle = True
				line = f.readline()
				continue

			if (int(line[6:]) != modelID and modelID != None):
				toggle = False
				line = f.readline()
				continue

		if( toggle ):
			if (line[0:4] != 'ATOM') and (line[0:6] != 'HETATM'):
				line = f.readline()
				continue

			if (line[21]==chainID) or (chainID==None):
				resnum = int(line[22:26])
				if (resnum>=startRes) or (startRes==None):
					if (resnum<=endRes) or (endRes==None):
						if( line[12:16].strip() == atomName ):
							ret.append( (float(line[30:38]),float(line[38:46]),float(line[46:54])) )

		line = f.readline()
	f.close()

	return ret

def parseAtomLine(line):

	l = line.strip().ljust(80)
	if (l[0:4]!='ATOM') and (l[0:6]!='HETATM'):
		return None

	return {
		'serial':int(l[6:11]),
		'name':l[12:16].strip(),
		'resname':l[17:20].strip(),
		'resnum':int(l[22:26]),
		'chain':l[21],
		'coords':(float(l[30:38]),float(l[38:46]),float(l[46:54])),
		'occupancy':float(l[54:60]),
		'bfactor':float(l[60:66]),
		'segment':l[72:76],
		'element':l[76:78].strip()
		}

def writeAtomLine( handle, a ):

	#                    s   n   R   N  R      X  Y  Z  O  B        S  E
	handle.write( "ATOM  %5d %4s %3s %1s%4s    %8s%8s%8s%6s%6s      %4s%2s  \n" % (
		a['serial'],
		a['name'].center(4),
		a['resname'],
		a['chain'],
		a['resnum'],
		str("%.3f" % a['coords'][0]).rjust(8),
		str("%.3f" % a['coords'][1]).rjust(8),
		str("%.3f" % a['coords'][2]).rjust(8),
		str("%.2f" % a['occupancy']).rjust(6),
		str("%.2f" % a['bfactor']).rjust(6),
		a['segment'],
		a['element'])
	)
	return

def getDistance(coord1,coord2):
	return sqrt( (coord1[0]-coord2[0])**2 + (coord1[1]-coord2[1])**2 + (coord1[2]-coord2[2])**2 )

def getAverage(coord1,coord2):
	return ( ((coord1[0]+coord2[0])/2),((coord1[1]+coord2[1])/2),((coord1[2]+coord2[2])/2) )

def getCenter(coords):
	return numpy.mean(numpy.array(coords, float), 0)

def getRMSD(c1,c2):
	n=len(c1)
	assert( n == len(c2) )

	sum=0.0
	for i in range(n):
		sum += ( (c1[i][0]-c2[i][0])**2 + (c1[i][1]-c2[i][1])**2 + (c1[i][2]-c2[i][2])**2 )
	return sqrt(sum/n)

def getPrincipleAxes( xyz ):

	# author: Pierre Poulain
	# contributors: Justine Guegan, Edithe Selwa

	#create coordinates array
	coord = numpy.array(xyz, float)

	# compute geometric center
	center = numpy.mean(coord, 0)

	# center with geometric center
	coord = coord - center

	# compute principal axis matrix
	inertia = numpy.dot(coord.transpose(), coord)
	e_values, e_vectors = numpy.linalg.eig(inertia)
	# warning eigen values are not necessary ordered!
	# http://docs.numpy.org/doc/numpy/reference/generated/numpy.linalg.eig.html

	# order eigen values (and eigen vectors)
	axis = [None,None,None]
	for i in range(len(e_values)):
		# find biggest eigen value
		if e_values[i] == max(e_values):
			axis[0] = e_vectors[:,i]
		# find smallest eigen value
		elif e_values[i] == min(e_values):
			axis[2] = e_vectors[:,i]
		# middle eigen value
		else:
			axis[1] = e_vectors[:,i]

	# CONSISTENCY checks - axes are frequently mirrored - need to maintain consistent directionality
	# find farthest point from CoM
	max_c = (0,0,0)
	max_d = 0.0
	for tmp in xyz:
		if( getDistance(tmp,center) > max_d ):
			max_c = tmp
	# reflect axis if necessary
	if( numpy.dot(max_c-center,axis[0]) < 0 ):
		for i in range(3):
			axis[i] *= -1.0

	return axis

def writeAtomToPDB( handle, serial, x, y, z, name, residue='', segid='', o=1, b=0, seqid=1 ):

	x = "%.3f" % x
	y = "%.3f" % y
	z = "%.3f" % z
	o = "%.2f" % o
	b = "%.2f" % b

	handle.write( 'ATOM'.ljust(6) )
	handle.write( "%5d" % serial )
	handle.write( "%1s" % " " )
	handle.write( name.center(4) )
	handle.write( "%1s" % " " )
	handle.write( "%3s" % residue )
	handle.write( "%1s" % " " )
	handle.write( "%1s" % segid )
	handle.write( "%4s" % seqid )
	handle.write( "%1s" % " " )
	handle.write( "%3s" % "   " )
	handle.write( x.rjust(8) )
	handle.write( y.rjust(8) )
	handle.write( z.rjust(8) )
	handle.write( o.rjust(6) )
	handle.write( b.rjust(6) )
	handle.write( "%6s" % "      " )
	handle.write( "%4s\n" % segid )

def writeConnectToPDB( handle, serial1, serial2, serial3='' ):
	handle.write( "CONECT%5s%5s%5s\n" % (serial1,serial2,serial3) )

def writeAxisToPDB( handle, center, axis1, axis2, axis3, serial, segid, seqid=999, residue='AXI', axis1_length=3.0,axis2_length=2.0,axis3_length=1.0 ):

	atoms = []
	atoms.append( ('QA',center) )
	atoms.append( ('QX',(axis1*axis1_length) + center) )
	atoms.append( ('QY',(axis2*axis2_length) + center) )
	atoms.append( ('QZ',(axis3*axis3_length) + center) )

	for (name,coord) in atoms:
		writeAtomToPDB( handle, serial, coord[0],coord[1],coord[2], name, segid=segid, seqid=seqid, residue='AXI' )
		serial +=1

	writeConnectToPDB( handle, serial-4, serial-3 )
	writeConnectToPDB( handle, serial-4, serial-2 )
	writeConnectToPDB( handle, serial-4, serial-1 )

	handle.write("TER\n")
pass

def rmsd(V, W):
	D = len(V[0])
	N = len(V)
	rmsd = 0.0
	for v, w in zip(V, W):
		rmsd += numpy.sqrt(sum([(v[i]-w[i])**2.0 for i in range(D)])/N)
	return rmsd

def kabsch(A, B):

	n = len(A)
	assert( n == len(B) )
	assert( n > 4 )

	P = numpy.array( A, float )
	Q = numpy.array( B, float )

	# translate both coordinate set's center of mass to the origin
	Pm = sum(P)/n
	P -= Pm
	Qm = sum(Q)/n
	Q -= Qm

	# Computation of the covariance matrix
	C = numpy.dot(numpy.transpose(P), Q)

	# Computation of the optimal rotation matrix
	V, S, W = numpy.linalg.svd(C)
	d = (numpy.linalg.det(V) * numpy.linalg.det(W)) < 0.0

	if(d):
		S[-1] = -S[-1]
		V[:,-1] = -V[:,-1]

	# Create Rotation matrix U
	return (Pm,Qm,numpy.dot(V, W))

