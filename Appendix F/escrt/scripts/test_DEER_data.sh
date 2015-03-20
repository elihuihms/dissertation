#!/bin/bash

for FILE in ./pdbs/ESCRT1_9*.pdb
do
	NAME=`basename $FILE .pdb`

	if [ ! -s temp/${NAME}_pseudo.pdb ]
	then
		echo "temp/${NAME}_pseudo.pdb missing"
	fi

	if [ ! -s DEER_distributions/${NAME}_1.dat ]
	then
		echo "DEER_distributions/${NAME}_1.dat missing"
	fi

	if [ ! -s DEER_distributions/${NAME}_2.dat ]
	then
		echo "DEER_distributions/${NAME}_2.dat missing"
	fi

	if [ ! -s DEER_distributions/${NAME}_3.dat ]
	then
		echo "DEER_distributions/${NAME}_3.dat missing"
	fi

	if [ ! -s DEER_curves/${NAME}_1.dat ]
	then
		echo "DEER_curves/${NAME}_1.dat missing"
	fi

	if [ ! -s DEER_curves/${NAME}_2.dat ]
	then
		echo "DEER_curves/${NAME}_3.dat missing"
	fi

	if [ ! -s DEER_curves/${NAME}_3.dat ]
	then
		echo "DEER_curves/${NAME}_3.dat missing"
	fi

done
