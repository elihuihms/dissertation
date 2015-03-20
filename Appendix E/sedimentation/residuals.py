#!/usr/bin/env python

import sys

assert( sys.argv[3] != sys.argv[1] )
assert( sys.argv[3] != sys.argv[2] )

f1 = open(sys.argv[1])
f2 = open(sys.argv[2])

d1 = []
d2 = []
d3 = []

while True:

	try:
		l1 = f1.readline()
		l2 = f1.readline()
	except:
		break

	a1 = map(float,l1.split())
	a2 = map(float,l2.split())

	if a1 == [] or a2 == []:
		break

	d3.append([a1[0]])
	for i in xrange(1,len(a1)):
		d3[-1].append(a1[i]-a2[i])

f1.close()
f2.close()

f3 = open(sys.argv[3],'w')
for i in xrange(len(d3)):
	f3.write("%f	%s\n"%(d3[i][0],"\t".join(map(str,d3[i][1:]))))
f3.close()
