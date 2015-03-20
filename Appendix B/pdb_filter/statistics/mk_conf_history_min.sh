#!/bin/bash

FILES=$1/ensembles_*dat
PLOT=/Volumes/ihms/MESMER_testing/scripts/make_conf_plot.pl
TABLES=/Volumes/ihms/MESMER_testing/tables

mkdir "$1_conf_history_min"

COUNT="0"
for f in $FILES
do
	$PLOT $TABLES/corr_QAmin_Rg.tbl $2 $f "Minimum AT-AT Distance"
	sips -s format jpeg output.pdf -o QAmin.jpg

#	$PLOT $TABLES/corr_QTmin_Rg.tbl $2 $f "Minimum TRAP-TRAP Distance"
#	sips -s format jpeg output.pdf -o QTmin.jpg
	
#	$PLOT $TABLES/corr_QTQAmin_Rg.tbl $2 $f "Minimum TRAP-AT Distance"
#	sips -s format jpeg output.pdf -o QTQAmin.jpg
		
#	montage -quiet "QAmin.jpg" "QTmin.jpg" "QTQAmin.jpg" -geometry 1650x -tile 3x1 "$COUNT-min.jpg"
#	mv "$COUNT-min.jpg" "$1_conf_history_min/"
	mv "QAmin.jpg" "$1_conf_history_min/$COUNT-min.jpg"
		
	COUNT=`expr $COUNT + 1` 
done

rm QT*jpg
rm QA*jpg
rm output.pdf