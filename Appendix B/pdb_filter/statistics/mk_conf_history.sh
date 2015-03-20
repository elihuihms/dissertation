#!/bin/bash

FILES=$1/ensembles_*dat
PLOT=/Volumes/ihms/MESMER_testing/scripts/make_conf_plot.pl
TABLES=/Volumes/ihms/MESMER_testing/tables

mkdir "$1_conf_history"

COUNT="0"
for f in $FILES
do

	#if [ $COUNT -le "26" ]
	#then
	#	echo "Skipping $COUNT"		
	#	COUNT=`expr $COUNT + 1`
	#	continue
	#fi
	
	$PLOT $TABLES/corr_QTmin_Rg.tbl $2 $f "Minimum TRAP-TRAP Distance"
	sips -s format jpeg output.pdf -o QTmin.jpg
	
	$PLOT $TABLES/corr_QTavg_Rg.tbl $2 $f "Average TRAP-TRAP Distance"
	sips -s format jpeg output.pdf -o QTavg.jpg
	
	$PLOT $TABLES/corr_QTmax_Rg.tbl $2 $f "Maximum TRAP-TRAP Distance"
	sips -s format jpeg output.pdf -o QTmax.jpg
	
	montage -quiet "QTmin.jpg" "QTavg.jpg" "QTmax.jpg" -geometry 1650x -tile 1x3 "$1_$COUNT-QT.jpg"
	mv "$1_$COUNT-QT.jpg" "$1_conf_history/"

	$PLOT $TABLES/corr_QAmin_Rg.tbl $2 $f "Minimum AT-AT Distance"
	sips -s format jpeg output.pdf -o QAmin.jpg
	
	$PLOT $TABLES/corr_QAavg_Rg.tbl $2 $f "Average AT-AT Distance"
	sips -s format jpeg output.pdf -o QAavg.jpg
	
	$PLOT $TABLES/corr_QAmax_Rg.tbl $2 $f "Maximum AT-AT Distance"
	sips -s format jpeg output.pdf -o QAmax.jpg
	
	montage -quiet "QAmin.jpg" "QAavg.jpg" "QAmax.jpg" -geometry 1650x -tile 1x3 "$1_$COUNT-QA.jpg"
	mv "$1_$COUNT-QA.jpg" "$1_conf_history/"
	
	$PLOT $TABLES/corr_QTQAmin_Rg.tbl $2 $f "Minimum TRAP-AT Distance"
	sips -s format jpeg output.pdf -o QTQAmin.jpg
	
	$PLOT $TABLES/corr_QTQAavg_Rg.tbl $2 $f "Average TRAP-AT Distance"
	sips -s format jpeg output.pdf -o QTQAavg.jpg
	
	$PLOT $TABLES/corr_QTQAmax_Rg.tbl $2 $f "Maximum TRAP-AT Distance"
	sips -s format jpeg output.pdf -o QTQAmax.jpg
	
	montage -quiet "QTQAmin.jpg" "QTQAavg.jpg" "QTQAmax.jpg" -geometry 1650x -tile 1x3 "$1_$COUNT-QTQA.jpg"
	mv "$1_$COUNT-QTQA.jpg" "$1_conf_history/"
	
	COUNT=`expr $COUNT + 1` 
done

rm QT*jpg
rm QA*jpg
rm output.pdf