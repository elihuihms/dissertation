#!/bin/bash

PLOT=/Volumes/ihms/MESMER_testing/scripts/make_spec_plot.pl
TABLES=/Volumes/ihms/MESMER_testing/tables

$PLOT $TABLES/corr_QTmin_Rg.tbl *spec "Minimum TRAP-TRAP Distance"
sips -s format jpeg output.pdf -o QTmin.jpg
$PLOT $TABLES/corr_QTavg_Rg.tbl *spec "Average TRAP-TRAP Distance"
sips -s format jpeg output.pdf -o QTavg.jpg
$PLOT $TABLES/corr_QTmax_Rg.tbl *spec "Maximum TRAP-TRAP Distance"
sips -s format jpeg output.pdf -o QTmax.jpg
montage -quiet "QTmin.jpg" "QTavg.jpg" "QTmax.jpg" -geometry 1650x -tile 1x3 "spec_QT.jpg"

$PLOT $TABLES/corr_QAmin_Rg.tbl *spec "Minimum AT-AT Distance"
sips -s format jpeg output.pdf -o QAmin.jpg
$PLOT $TABLES/corr_QAavg_Rg.tbl *spec "Average AT-AT Distance"
sips -s format jpeg output.pdf -o QAavg.jpg
$PLOT $TABLES/corr_QAmax_Rg.tbl *spec "Maximum AT-AT Distance"
sips -s format jpeg output.pdf -o QAmax.jpg
montage -quiet "QAmin.jpg" "QAavg.jpg" "QAmax.jpg" -geometry 1650x -tile 1x3 "spec_QA.jpg"

$PLOT $TABLES/corr_QTQAmin_Rg.tbl *spec "Minimum TRAP-AT Distance"
sips -s format jpeg output.pdf -o QTQAmin.jpg
$PLOT $TABLES/corr_QTQAavg_Rg.tbl *spec "Average TRAP-AT Distance"
sips -s format jpeg output.pdf -o QTQAavg.jpg
$PLOT $TABLES/corr_QTQAmax_Rg.tbl *spec "Maximum TRAP-AT Distance"
sips -s format jpeg output.pdf -o QTQAmax.jpg
montage -quiet "QTQAmin.jpg" "QTQAavg.jpg" "QTQAmax.jpg" -geometry 1650x -tile 1x3 "spec_QTQA.jpg"

rm QT*jpg
rm QA*jpg
rm output.pdf


