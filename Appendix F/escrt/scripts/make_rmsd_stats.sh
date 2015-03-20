#!/bin/bash

#./compile_domain_rmsd.py				\
#	-pdb pdbs/ESCRT1_9376.pdb			\
#	-dir pdbs							\
#	-domain 1 999						\
#	-out all_open_RMSD.tbl

#./compile_domain_rmsd.py				\
#	-pdb pdbs/ESCRT1_7612.pdb			\
#	-dir pdbs							\
#	-domain 1 999						\
#	-out all_closed_RMSD.tbl

./compile_domain_rmsd.py				\
	-pdb pdbs/ESCRT1_9376.pdb			\
	-dir pdbs							\
	-domain A   9 159					\
	-out VPS23_open_RMSD.tbl

./compile_domain_rmsd.py				\
	-pdb pdbs/ESCRT1_7612.pdb			\
	-dir pdbs							\
	-domain A   9 159					\
	-out VPS23_closed_RMSD.tbl

./compile_domain_rmsd.py				\
	-pdb pdbs/ESCRT1_9376.pdb			\
	-dir pdbs							\
	-domain C   1  34					\
	-out VPS37_open_RMSD.tbl

./compile_domain_rmsd.py				\
	-pdb pdbs/ESCRT1_7612.pdb			\
	-dir pdbs							\
	-domain C   1  34					\
	-out VPS37_closed_RMSD.tbl

./compile_domain_rmsd.py				\
	-pdb pdbs/ESCRT1_9376.pdb			\
	-dir pdbs							\
	-domain B 148 242					\
	-out VPS28_open_RMSD.tbl

./compile_domain_rmsd.py				\
	-pdb pdbs/ESCRT1_7612.pdb			\
	-dir pdbs							\
	-domain B 148 242					\
	-out VPS28_closed_RMSD.tbl
