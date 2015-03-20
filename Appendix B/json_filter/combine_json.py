#!/usr/bin/python

"""
Combines all the passed .json argument into a single object and prints it to STDOUT
"""

import glob
import json
import sys

files = glob.glob( "*.json" )

if( len(sys.argv) < 2 ):
	print "Usage: combine_json.py *json > combined.json"
	sys.exit(0)

ret = []
for i in range( 1, len(sys.argv) ):
	f = open( sys.argv[i] )
	string = f.read()
	f.close()

	try:
		ret.extend( json.loads( string ) )
	except:
		print "Error reading \"%s\"" % ( sys.argv[i] )
		sys.exit(0)
pass

print json.dumps( ret )
