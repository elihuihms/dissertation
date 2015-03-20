#!/bin/bash

axes='/fosterlab/users/ihms/Projects/MESMER/testing/structure_analysis/compile_domain_axes.py'
stats='/fosterlab/users/ihms/Projects/MESMER/testing/structure_analysis/compile_domain_stats.py'

# make a PDB containing the principle axes of the domains
$axes									\
	-dir pdbs							\
	-domain A   9 159					\
	-domain B 148 242					\
	-domain C   1  34					\
	-out principle_axes.pdb

# create tables of the distances between the CA atoms of each residue
$stats									\
	-dir pdbs							\
	-domain A 108 108					\
	-domain A 256 256					\
	-out label_stats_1.tbl

$stats									\
	-dir pdbs							\
	-domain C  12  12					\
	-domain A 223 223					\
	-out label_stats_2.tbl

$stats									\
	-dir pdbs							\
	-domain B  65  65					\
	-domain B 151 151					\
	-out label_stats_3.tbl

# create tables of the orientation of each domain w/ respect to other labeled domain
$stats									\
	-dir pdbs							\
	-domain A   9 159					\
	-domain A 218 385					\
	-out domain-domain_stats_1.tbl

$stats									\
	-dir pdbs							\
	-domain C   1  34					\
	-domain A 218 385					\
	-out domain-domain_stats_2.tbl

$stats									\
	-dir pdbs							\
	-domain B   1 117					\
	-domain B 148 242					\
	-out domain-domain_stats_3.tbl

# create tables of the orientation of each labeled domain w/ respect to core
$stats									\
	-dir pdbs							\
	-domain A   9 159					\
	-domain D	1  81					\
	-out domain-core_stats_1.tbl

$stats									\
	-dir pdbs							\
	-domain C   1  34					\
	-domain D	1  81					\
	-out domain-core_stats_2.tbl

$stats									\
	-dir pdbs							\
	-domain B 148 242					\
	-domain D	1  81					\
	-out domain-core_stats_3.tbl

# compile all desired info into the label stats tables
tread -col 1 domain-domain_stats_1.tbl	| twrite -col 2 label_stats_1.tbl
tread -col 1 domain-core_stats_1.tbl	| twrite -col 3 label_stats_1.tbl
tread -col 2 domain-domain_stats_1.tbl  | twrite -col 4 label_stats_1.tbl
tread -col 2 domain-core_stats_1.tbl	| twrite -col 5 label_stats_1.tbl

tread -col 1 domain-domain_stats_2.tbl	| twrite -col 2 label_stats_2.tbl
tread -col 1 domain-core_stats_2.tbl	| twrite -col 3 label_stats_2.tbl
tread -col 2 domain-domain_stats_2.tbl  | twrite -col 4 label_stats_2.tbl
tread -col 2 domain-core_stats_2.tbl	| twrite -col 5 label_stats_2.tbl

tread -col 1 domain-domain_stats_3.tbl	| twrite -col 2 label_stats_3.tbl
tread -col 1 domain-core_stats_3.tbl	| twrite -col 3 label_stats_3.tbl
tread -col 2 domain-domain_stats_3.tbl  | twrite -col 4 label_stats_3.tbl
tread -col 2 domain-core_stats_3.tbl	| twrite -col 5 label_stats_3.tbl
