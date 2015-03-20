#!/bin/bash

FILES=$1/ensembles_*dat
PLOT=/Volumes/ihms/MESMER_testing/scripts/make_conf_plot.pl
TABLES=/Volumes/ihms/MESMER_testing/tables

mkdir "$1_conf_history_avg"

COUNT="0"
for f in $FILES
do
	$PLOT $TABLES/corr_QAavg_Rg.tbl $2 $f "Average AT-AT Distance"
	sips -s format jpeg output.pdf -o QAavg.jpg

	$PLOT $TABLES/corr_QTavg_Rg.tbl $2 $f "Average TRAP-TRAP Distance"
	sips -s format jpeg output.pdf -o QTavg.jpg
	
	$PLOT $TABLES/corr_QTQAavg_Rg.tbl $2 $f "Average TRAP-AT Distance"
	sips -s format jpeg output.pdf -o QTQAavg.jpg
		
	montage -quiet "QAavg.jpg" "QTavg.jpg" "QTQAavg.jpg" -geometry 1650x -tile 3x1 "$COUNT-avg.jpg"
	mv "$COUNT-avg.jpg" "$1_conf_history_avg/"
	
	COUNT=`expr $COUNT + 1` 
done

rm QT*jpg
rm QA*jpg
rm output.pdf