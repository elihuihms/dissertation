This directory contains the scripts and other files necessary to generate ESCRT1 complex PDBs and then apply the different positions (libraries) of the MTSL spin labels to each position.

ESCRT1 PDBs were generated with the mc.py (monte carlo) and mc_rg.py (monte carlo with radius of gyration constraint) Xplor scripts.

The MTSL spin libraries for each rigid domain were generated with the matlab MMM (multiscale modeling) software package, and the program "./align_domains.py" used to align each domain with attached spin probe clusters to the respective domains of each generated ESCRT1 complex.

Some comparison studies using coarse MD and MC randomization of spin probe linkers was also performed to compare with the MMM rotamer libraries (see ./label_dynamics).
