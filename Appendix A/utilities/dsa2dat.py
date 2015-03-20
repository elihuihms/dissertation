#!/usr/bin/env python

import argparse
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument('files',		nargs='+',							help='.dsa file(s) to parse')
parser.add_argument('-quiet',	default=False,	action='store_true',	help='Print header info?')
parser.add_argument('-query',	default=False,	action='store_true',	help='Check with user?')

args = parser.parse_args()

for filename in args.files:

	try:
		f = open( filename )
	except:
		print "Error reading %s" % (filename)
		exit()

	x_var, y_var = [],[]

	counter = 0
	line = f.readline()
	while line:

		if counter < 17 and not args.quiet:
			print "%s" % (line),
		if counter == 17:
			x_var = line.strip().split(',')
		elif counter == 24:
			y_var = line.strip().split(',')

		counter+=1
		line = f.readline()

	f.close()

	if len(x_var) != len(y_var):
		print "Error parsing %s" % (filename)

	if args.query:
		plt.scatter(map(float,x_var),map(float,y_var))
		plt.show()

		input = raw_input("Convert %s? (Y/N):" % (filename))

		if input != 'y' and input != 'Y':
			continue

	f = open( "%s.dat" % (filename.split('.')[0]), 'w' )
	for i in range(len(x_var)):
		f.write( "%s\t%s\n" % (x_var[i],y_var[i]) )
	f.close()