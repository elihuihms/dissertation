tread -w -col 1 $1.gdat > $1_avg.dat
tread -w -col 2 $1.gdat.1 > temp1.dat
tread -w -col 2 $1.gdat.2 > temp2.dat
tread -w -col 2 $1.gdat.3 > temp3.dat
tread -w -col 2 $1.gdat.4 > temp4.dat
tread -w -col 2 $1.gdat | tmunge -f add temp1.dat | tmunge -f add temp2.dat | tmunge -f add temp3.dat | tmunge -f add temp4.dat | tmath -f divide 5 | twrite -col 1 $1_avg.dat
tread -w -col 1 $1_avg.dat | tmath -f divide 20 | twrite -col 2 $1_avg.dat
rm temp1.dat
rm temp2.dat
rm temp3.dat
rm temp4.dat