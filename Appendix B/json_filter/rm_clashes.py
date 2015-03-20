#!/usr/bin/python

import os
from sys import argv,exit
from json import loads,dumps

from pointmaps import *
from rm_duplicates_lib import *

if (len(argv) < 3):
	print "Usage: rm_clashes.py 'json_file.json' <cutoff> > output.json"
	exit(0)

f = open(argv[1], 'r')	
file = f.read()
f.close()

cutoff = float(argv[2])

if( file == None ):
	print "Bad file '%s'" % ( argv[1] )
	exit(0)

# load the chains from the json array
try:
	chains = loads(file)
except:
	print "The JSON parser ran into an error."
	exit(0)
pass

# an array to hold all non-clashing chains
goodChains = []

for chain in chains:
	map = makePointMap(chain,True)
#	print getMinDistance(map)
	if( getMinDistance(map) > cutoff ):
		goodChains.append( chain )
pass

print dumps( goodChains )
