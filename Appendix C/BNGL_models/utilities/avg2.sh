tread -w -col 0 $1_3.fit > $1_avg.fit
tread -w -col 1 $1_3.fit | twrite -col 1 $1_avg.fit
tread -w -col 1 $1_3.fit | tmath -f multiply 0.05 | twrite -col 2 $1_avg.fit