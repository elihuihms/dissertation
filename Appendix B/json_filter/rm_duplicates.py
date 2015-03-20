#!/usr/bin/python

import os

from sys import argv,exit
from json import loads,dumps

from rm_duplicates_lib import *

if (len(argv) < 2):
	print "Usage: remove_duplicates.py 'json_file.json'"
	print "Builds a 2D map of each chain present in the json file, and compares to to every other chain. Unique chains are returned."
	exit(0)

# attempt to read the file
f = open(argv[1], 'r')	
file = f.read()
f.close()

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

# an array to hold all unique chains
uniqueChains = []

# an array to hold a point representation of all unique chains
uniqueList = []

for chain in chains:
	if( findDuplicateByDist(uniqueList,chain,cyclic=False) < 0 ):
		uniqueChains.append( chain )
pass

#print "%i unique chains from %i starting chains" % (len(uniqueChains),len(chains))
print dumps( uniqueChains )
