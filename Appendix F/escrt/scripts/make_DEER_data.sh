#!/bin/bash

if [ ! -d temp ]; then
	mkdir temp
fi
if [ ! -d DEER_distributions ]; then
	mkdir DEER_distributions
fi
if [ ! -d DEER_curves ]; then
	mkdir DEER_curves
fi

COUNT=0
for FILE in ESCRT1_*.pdb
do
	NAME=`basename $FILE .pdb`

	# check to see if we've already computed the curves
	if [ -s DEER_curves/${NAME}_1.dat ]; then
		if [ -s DEER_curves/${NAME}_2.dat ]; then
			if [ -s DEER_curves/${NAME}_3.dat ]; then
				echo "Skipping ${NAME}.pdb"
				continue
			fi
		fi
	fi

	# aligns the domains containing spin probes to the corresponding domain in the given complex
	./align_domains.py 							\
		-pdb $FILE								\
		-domain core_rotamers.pdb				\
		-domain	A_9-159_rotamers.pdb 			\
		-domain B_148-242_rotamers.pdb 			\
		-domain C_1-34_rotamers.pdb 			\
		-out temp/${NAME}_rotamers.pdb

	# generates a PDB containing QZ ATOMs at the spin probe locations
	./pdb_get_midpoints.py 						\
		-pdb temp/${NAME}_rotamers.pdb 			\
		-pseudo QZ								\
		-atoms A 108 N1 O1						\
		-atoms A 223 N1 O1 						\
		-atoms A 256 N1 O1						\
		-atoms B  27 N1 O1 						\
		-atoms B  65 N1 O1 						\
		-atoms B 151 N1 O1						\
		-atoms C  12 N1 O1						\
		-atoms C 173 N1 O1						\
		-out temp/${NAME}_pseudo.pdb

	# calculate the distance distributions for spin probe pairs
	./pdb_deer_dist.py							\
		-pdb temp/${NAME}_pseudo.pdb			\
		-label A 108 QZ							\
		-label A 256 QZ							\
		-out DEER_distributions/${NAME}_1.dat

	./pdb_deer_dist.py							\
		-pdb temp/${NAME}_pseudo.pdb			\
		-label C  12 QZ							\
		-label A 223 QZ							\
		-out DEER_distributions/${NAME}_2.dat

	./pdb_deer_dist.py							\
		-pdb temp/${NAME}_pseudo.pdb			\
		-label B  65 QZ							\
		-label B 151 QZ							\
		-out DEER_distributions/${NAME}_3.dat

	# calculate the predicted DEER curves for spin probe pairs
	./pdb_deer_sim.py							\
		-dist DEER_distributions/${NAME}_1.dat	\
		-out DEER_curves/${NAME}_1.dat

	./pdb_deer_sim.py							\
		-dist DEER_distributions/${NAME}_2.dat	\
		-out DEER_curves/${NAME}_2.dat

	./pdb_deer_sim.py							\
		-dist DEER_distributions/${NAME}_3.dat	\
		-out DEER_curves/${NAME}_3.dat

	rm temp/${NAME}_rotamers.pdb
	#rm temp/${NAME}_pseudo.pdb

	COUNT=$[COUNT + 1]
done
