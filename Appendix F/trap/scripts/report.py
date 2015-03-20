#!/usr/bin/env python

import sys
import scipy

f = open( sys.argv[1], 'r' )

a = f.readlines()

f.close()

def make_report( lines ):

	name,weight,error = [],[],[]

	for l in lines:
		a = l.split()

		if len(a) != 4:
			break

		name.append( a[3] )
		weight.append( float(a[0]) )
		error.append( float(a[2]) )

	order = scipy.argsort( name )
	name, weight, error = scipy.take( name, order ), scipy.take( weight, order ), scipy.take( error, order )

	return (name,weight,error)

reports = [None]*9
for (i,tmp) in enumerate(a):

	if tmp.strip() == 'Bsu_TRAP_0.5xAT_3mgmL':
		reports[0] = make_report( a[i+1:] )
	elif tmp.strip() == 'Bsu_TRAP_0.5xAT_5mgmL':
		reports[1] = make_report( a[i+1:] )
	elif tmp.strip() == 'Bsu_TRAP_0.5xAT_10mgmL':
		reports[2] = make_report( a[i+1:] )
	elif tmp.strip() == 'Bsu_TRAP_1xAT_3mgmL':
		reports[3] = make_report( a[i+1:] )
	elif tmp.strip() == 'Bsu_TRAP_1xAT_5mgmL':
		reports[4] = make_report( a[i+1:] )
	elif tmp.strip() == 'Bsu_TRAP_1xAT_10mgmL':
		reports[5] = make_report( a[i+1:] )
	elif tmp.strip() == 'Bsu_TRAP_1.5xAT_3mgmL':
		reports[6] = make_report( a[i+1:] )
	elif tmp.strip() == 'Bsu_TRAP_1.5xAT_5mgmL':
		reports[7] = make_report( a[i+1:] )
	elif tmp.strip() == 'Bsu_TRAP_1.5xAT_10mgmL':
		reports[8] = make_report( a[i+1:] )

def print1( r ):
	for i in range(len(r[0][0])):
		print "'%s\t" % (r[0][0][i]),
		print "%.3f\t%.3f\t" % (r[0][1][i],r[0][2][i]),
		print "%.3f\t%.3f\t" % (r[3][1][i],r[3][2][i]),
		print "%.3f\t%.3f\t" % (r[6][1][i],r[6][2][i]),
		print "\t",
		print "%.3f\t%.3f\t" % (r[1][1][i],r[1][2][i]),
		print "%.3f\t%.3f\t" % (r[4][1][i],r[4][2][i]),
		print "%.3f\t%.3f\t" % (r[7][1][i],r[7][2][i]),
		print "\t",
		print "%.3f\t%.3f\t" % (r[2][1][i],r[2][2][i]),
		print "%.3f\t%.3f\t" % (r[5][1][i],r[5][2][i]),
		print "%.3f\t%.3f\t" % (r[8][1][i],r[8][2][i]),
		print ""


def print2( r ):
	for i in range(len(r[0][0])):
		print "'%s\t" % (r[0][0][i]),
		print "%.3f\t%.3f\t%.3f\t" % (r[0][1][i],r[3][1][i],r[6][1][i]),
		print "%.3f\t%.3f\t%.3f\t" % (r[1][1][i],r[4][1][i],r[7][1][i]),
		print "%.3f\t%.3f\t%.3f\t" % (r[2][1][i],r[5][1][i],r[8][1][i]),
		print "\t",
		print "%.3f\t%.3f\t%.3f\t" % (r[0][2][i],r[3][2][i],r[6][2][i]),
		print "%.3f\t%.3f\t%.3f\t" % (r[1][2][i],r[4][2][i],r[7][2][i]),
		print "%.3f\t%.3f\t%.3f\t" % (r[2][2][i],r[5][2][i],r[8][2][i]),
		print ""

def print3( r ):
	for j in (0,1,2):
		for i in range(len(r[0][0])):
			print "'%s\t" % (r[0][0][i]),
			print "%.3f\t%.3f\t" % (r[0+j][1][i],r[0+j][2][i]),
			print "%.3f\t%.3f\t" % (r[3+j][1][i],r[3+j][2][i]),
			print "%.3f\t%.3f\t" % (r[6+j][1][i],r[6+j][2][i]),
			print ""
		print ""

#print1( reports )
#print "\n"
#print2( reports )
#print "\n"
print3( reports )
