This directory contains data analysis / setup and structural generation scripts for the calmodulin system used to test MESMER

./cam.target: The MESMER target for globally fitting experimental calmodulin data

./paramagnetic: Contains raw data and scripts used to obtain/verify the paramagnetic tensors for PCS and RDC back-calculation

./structure_gen: Contains the starting N and C-termini domains of calmodulin used by RanCh to generate the structural library. Note that RanCh normally strips hydrogens, so pseudo atoms were used for hydrogen atom coordinates, and then switched back afterwards. Also contains an Xplor-NIH script that was tested for monte-carlo structure generation.