AT trimer structure refinement using SAXS data
2012.04.24
E. Ihms

Note: many of these restraint tables were cleaned up from the versions placed in the BMRB entry, as several of them provided parsing errors, or logical errors.

./dihedrals.tbl
This restraint table had 6 dihedrals between atoms in non-sequential residues, which caused (as you may imagine) several problems. I've commented them out.

./noe_simple_no50HD1.tbl
This is simply the noe_simple.tbl with the several NOEs to the residue 50 HD1s removed, and was used before I created psf files with HD1 protons.

./rdc
A list of all the RDC experiment tables from craig's B. subtilis AT folder.

./saxs
All of my available (formyl) AT SAXS data:
als_01132010_C_merge.dat - 5mg/mL?
als_01132010_D_merge.dat - 10mg/mL?
als_02272011_fAT_1_23.dat - 10mg/mL
als_02272011_fAT_2_23.dat - 5mg/mL
als_02272011_fAT_3_23.dat - 3.3mg/mL

Note that the als_02272011 data seems to have some concentration-dependent behavior. For that reason, I would pick the 3.3mg/mL data, as it still has acceptable S/N.

./zn_chirality.tbl
Had to change the Zn residue to 54