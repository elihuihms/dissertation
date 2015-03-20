#!/usr/bin/python

import glob

files = glob.glob('./pdbs/*cam.pdb')

for file in files:

	lines = open(file,'r').readlines()
	for i in range(0,len(lines)):
		lines[i] = lines[i].replace(' Q ',' H ')
	
	open(file,'w').writelines(lines)