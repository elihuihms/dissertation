#!/bin/bash

# create tables of the orientation of each domain w/ respect to core
./compile_domain_stats.py				\
	-dir pdbs							\
	-domain D	1  81					\
	-domain A 159 218					\
	-out linker_stats_1.tbl

./compile_domain_stats.py				\
	-dir pdbs							\
	-domain D	1  81					\
	-domain C  34  47					\
	-out linker_stats_3.tbl

./compile_domain_stats.py				\
	-dir pdbs							\
	-domain D	1  81					\
	-domain B 117 148					\
	-out linker_stats_2.tbl
