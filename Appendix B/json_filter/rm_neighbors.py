#!/usr/bin/python

import os
from sys import argv,exit
from json import loads,dumps

if (len(argv) < 2):
	print "Usage: remove_neighbors.py 'json_file.json'"
	exit(0)

f = open(argv[1], 'r')	
file = f.read()
f.close()

if( file == None ):
	print "Bad file '%s'" % ( argv[1] )
	exit(0)

# split the single line containing all of the chains into many lines containing one chain per
file = file.replace('[[{','[{')
file = file.replace('}]]','}]')
file = file.replace('}], [{',"}]\n[{")
chains = file.split("\n")

ret = []
for string in chains:
	string.strip()
	
	# decode the JSON string into a python array
	try:
		chain = loads(string)
	except:
		print "The JSON parser ran into an error."
		print string
		exit(0)
	
	if(len(chain) < 1):
		print "A malformed JSON string was provided."
		exit(0)
	
	chain_good = True
	for i in range(len(chain)):
		if (chain[i]['type'] == 0):
			for site1 in range( len(chain[i]['sites']) ):
				
				if( site1 == len(chain[i]['sites']) -1 ):
					site2 = 0
				else:
					site2 = site1 +1
				
				if( (chain[i]['sites'][ site1 ] != None) and (chain[i]['sites'][ site2 ] != None) ):
					chain_good = False
					break
					
	if( chain_good ):				
		ret.append( chain )


print dumps(ret)
