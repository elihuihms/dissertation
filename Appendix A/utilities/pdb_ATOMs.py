#!/usr/bin/env python

import sys

f = open(sys.argv[1])
lines = f.readlines()
f.close()

f = open(sys.argv[1],'w')
for line in lines:
	if( line[:4] == 'ATOM' ):
		f.write(line)
f.close()
