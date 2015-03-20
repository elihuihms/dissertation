These directories contain utilities and scripts that make up the structure generation routines for TRAP+AT clusters.

./chain_plotter: A javascript / HTML5 2D viewer for the JSON connectivity/topology arrays.

./json_builder: Contains two different programs for generating the JSON connectivity arrays used to build TRAP-AT heteromers.

The resulting json arrays are then used as input for the pdb_builder program, which assembles the connectivity topologies into PDBs using a series of translational and rotational matricies. This program is also written in Python.

./json_filter: Contains several Python scripts that can process json arrays to remove structural duplicates, etc.

The resulting pdbs can be "scored" or otherwise analyzed by applying the pdb_score suite of C programs which collect information from the pdbs based on placement of marker atoms and other structural statistics. These were written in C to be as fast as possible and will definitely require recompiling and/or rewriting based on future needs.

./pdb_builder: Contains the mkchains program that constructs TRAP-AT complex coordinate files from component structures using a json connectivity file and rotation/translation matrices 

./pdb_filter: contains several scripts that utilize the pdb_score programs to select PDBs or generate different types of statistical data.

./pdb_score: Suite of simple programs written in C that extract structural information from a coordinate file

./saxs_structures: GNOM output files and DAMN/GASBOR scripts for generation of TRAP and AT structure generation from SAXS profiles