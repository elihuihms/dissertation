/Volumes/FosterLab/users/ihms/Projects/TRAP_AT/models/stochastic/NFsim_v1.11/BNG2.pl $1.bngl
/Volumes/FosterLab/users/ihms/Projects/TRAP_AT/models/stochastic/NFsim_v1.11/bin/NFsim_i386-darwin -cb -bscb -xml $1.xml -sim 100 -oSteps 10000 -ss $1.final -o $1.gdat.$2
rm $1.xml
