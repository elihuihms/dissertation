#!/usr/bin/python

import glob

files = glob.glob('./cam_H/*cam.pdb')

for file in files:

	lines = open(file,'r').readlines()
	for i in range(0,len(lines)):
		lines[i] = lines[i].rstrip()
		lines[i] = "%s  0.00  0.00    \n" % (lines[i])
	
	open(file,'w').writelines(lines)