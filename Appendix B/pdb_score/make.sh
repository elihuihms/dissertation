#!/bin/sh

cc src/atom_distance.c -lm -o bin/atom_distance
cc src/2atom_distance.c -lm -o bin/2atom_distance
cc src/clash_count.c -lm -o bin/clash_count
cc src/rg_calc.c -lm -o bin/rg_calc
cc src/rmsd_calc.c -lm -o bin/rmsd_calc
cc src/com_calc.c -lm -o bin/com_calc
cc src/atom_distances.c -lm -o bin/atom_distances