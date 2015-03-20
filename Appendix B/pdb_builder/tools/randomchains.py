#!/usr/bin/python

from sys import *
from pdbchain.pdb_json import *
import random

if (len(argv) < 4):
	print "Usage: randomchains.py <n_chains> 'in.json' 'out.json'"
	exit(0)

f = open(argv[2], 'r')	
file = f.read()
f.close()

# split the single line containing all of the chains into many lines containing one chain per
file = file.replace("var chains=[",'')
file = file.replace("}], [{", "}]\n[{" )
file = file.replace("]}]];",']}]')
input_chains = file.split("\n")

output_chains = []
for i in range( int(argv[1]) ):
	output_chains.append( random.choice( input_chains ) )

string = ', '.join( output_chains )
string = "var chains=["+string+"];"

f = open(argv[3], 'w')
f.write( string )
f.close()