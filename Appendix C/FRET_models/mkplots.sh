teval -range 0,1 -points 1000 -f "1*(x[0]**0)*((1-x[0])**3)" 	> trimer_label_partition.dat 
teval -range 0,1 -points 1000 -f "3*(x[0]**1)*((1-x[0])**2)" -y	| twrite -col 2 trimer_label_partition.dat 
teval -range 0,1 -points 1000 -f "3*(x[0]**2)*((1-x[0])**1)" -y	| twrite -col 3 trimer_label_partition.dat
teval -range 0,1 -points 1000 -f "1*(x[0]**3)*((1-x[0])**0)" -y	| twrite -col 4 trimer_label_partition.dat

teval -range 0,1 -points 1000 -f "1*(0./3.)*(x[0]**0)*((1-x[0])**3)" 	> trimer_fret_partition.dat 
teval -range 0,1 -points 1000 -f "3*(1./3.)*(x[0]**1)*((1-x[0])**2)" -y	| twrite -col 2 trimer_fret_partition.dat 
teval -range 0,1 -points 1000 -f "3*(2./3.)*(x[0]**2)*((1-x[0])**1)" -y	| twrite -col 3 trimer_fret_partition.dat
teval -range 0,1 -points 1000 -f "1*(3./3.)*(x[0]**3)*((1-x[0])**0)" -y	| twrite -col 4 trimer_fret_partition.dat

cat trimer_fret_partition.dat | teval -f "x[2]+x[3]+x[4]" -y | twrite -col 5 trimer_fret_partition.dat

tread -col 0 trimer_fret_partition.dat > FRET_component_ratios.dat
cat trimer_fret_partition.dat | teval -f "x[2]/(x[2]+x[3]+x[4])" -y | twrite -col 1 FRET_component_ratios.dat
cat trimer_fret_partition.dat | teval -f "x[3]/(x[2]+x[3]+x[4])" -y | twrite -col 2 FRET_component_ratios.dat
cat trimer_fret_partition.dat | teval -f "x[4]/(x[2]+x[3]+x[4])" -y | twrite -col 3 FRET_component_ratios.dat
