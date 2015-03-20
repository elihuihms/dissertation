#!/usr/bin/env python

from subprocess import call
from random import sample

pdbs = "/Volumes/FosterLab/users/ihms/Projects/MESMER/testing/escrt/result_analysis/library_v5.0/pdbs"

structure_stats,ensemble_stats = [],[]
structure_stats.append("/Volumes/FosterLab/users/ihms/Projects/MESMER/testing/escrt/structure_stats/mc_d_3/mc_d_3_VPS23.tbl")
ensemble_stats.append("/Volumes/FosterLab/users/ihms/Projects/MESMER/testing/escrt/result_analysis/library_v5.0/results_ESCRT1_D3_N2_DEER_20000/component_statistics_ESCRT1_00035.tbl")

structure_stats.append("/Volumes/FosterLab/users/ihms/Projects/MESMER/testing/escrt/structure_stats/mc_d_3/mc_d_3_VPS37.tbl")
ensemble_stats.append("/Volumes/FosterLab/users/ihms/Projects/MESMER/testing/escrt/result_analysis/library_v5.0/results_ESCRT1_D3_N2_DEER_20000/component_statistics_ESCRT1_00035.tbl")

structure_stats.append("/Volumes/FosterLab/users/ihms/Projects/MESMER/testing/escrt/structure_stats/mc_d_3/mc_d_3_VPS28.tbl")
ensemble_stats.append("/Volumes/FosterLab/users/ihms/Projects/MESMER/testing/escrt/result_analysis/library_v5.0/results_ESCRT1_D3_N2_DEER_20000/component_statistics_ESCRT1_00035.tbl")

for i,(n,chain,start,end) in enumerate( [('VPS23','A',1,159),('VPS37','C',1,34),('VPS28','B',148,242)] ):

	stats1,stats2 = [],[]
	f = open( structure_stats[i] )
	for line in f.readlines():
		a = line.split()
		if a[0].find("ESCRT1_") > -1:
			stats1.append( a[0] )
			stats2.append( a )
	f.close()

	names1,names2 = [],[]
	f = open( ensemble_stats[i] )
	for line in f.readlines():
		a = line.split()
		if a[0].find("ESCRT1_") > -1:
#			print a[0]
#			print stats2[ stats1.index(a[0]) ][2]
			if float(stats2[ stats1.index(a[0]) ][2]) < 30:
				names1.append( a[0] )
			else:
				names2.append( a[0] )

	f.close()

#	names1 = sample( names1, min(len(names1),100) )
#	names2 = sample( names2, min(len(names1),100) )

#	args = ['make_models.py',pdbs','-names']
#	args.extend(names1)
#	args.extend( ['-out',"%s_short.pdb"%n] )
#	call( args )

#	args = ['make_models.py',pdbs,'-names']
#	args.extend(names2)
#	args.extend( ['-out',"%s_long.pdb"%n] )
#	call( args )

	import os
	import shutil

	args = map(str,['/Volumes/FosterLab/users/ihms/Projects/MESMER/testing/structure_analysis/compile_domain_axes.py','','-domain',chain,start,end,'-out',''])

	os.mkdir('./tmp1')
	os.mkdir('./tmp2')
	os.mkdir('./tmp3')

	args[-1] = "%s_short_axes.pdb"%n
	args[ 1] = './tmp2'
	for name in names1:
		shutil.copy( "%s/%s.pdb" % (pdbs,name), './tmp1' )
		shutil.copy( "%s/%s.pdb" % (pdbs,name), './tmp2' )
	call(args)
#	os.system('pdb2vol %s_short.pdb %s_short.sit < pdb2vol.txt' % (n,n))

	args[-1] = "%s_long_axes.pdb"%n
	args[ 1] = './tmp3'
	for name in names2:
		shutil.copy( "%s/%s.pdb" % (pdbs,name), './tmp1' )
		shutil.copy( "%s/%s.pdb" % (pdbs,name), './tmp3' )
	call(args)
#	os.system('pdb2vol %s_long.pdb %s_long.sit < pdb2vol.txt' % (n,n))

	args[-1] = "%s_both_axes.pdb"%n
	args[ 1] = './tmp1'
	call(args)
#	os.system('pdb2vol %s_both.pdb %s_both.sit < pdb2vol.txt' % (n,n))

	shutil.rmtree( './tmp1' )
	shutil.rmtree( './tmp2' )
	shutil.rmtree( './tmp3' )



