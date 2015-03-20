#!/bin/bash

PLOT=../../scripts/make_spec_plot.pl
TABLES=../../tables

#../../scripts/make_conf_chisq.py *mes ../../conf_lifetime/ > conf_chisq.tbl
#11site_1T_nA_00000.mes	1000
#11site_1T_nA_00001.mes	1000
#11site_1T_nA_00002.mes	1000
#11site_1T_nA_00003.mes	1000
#11site_1T_nA_00004.mes	1000
#11site_1T_nA_00005.mes	1000
#11site_1T_nA_00006.mes	1000
#11site_1T_nA_00007.mes	1000
#11site_1T_nA_00008.mes	1000
#11site_1T_nA_00009.mes	1000
#11site_1T_nA_00010.mes	1000
#11site_1T_nA_00011.mes	1000
#11site_1T_nA_00012.mes	1000
#11site_1T_nA_00013.mes	1000
#11site_1T_nA_00014.mes	1000
#11site_1T_nA_00015.mes	1000
#11site_1T_nA_00016.mes	1000
#11site_1T_nA_00017.mes	1000

tread -col 0 conf_chisq.tbl > temp.tbl
cat conf_chisq.tbl | teval -f "1/x[1]" -y | twrite -col 1 temp.tbl

$PLOT $TABLES/corr_QTmin_Rg.tbl temp.tbl "Minimum TRAP-TRAP Distance"
sips -s format jpeg output.pdf -o QTmin.jpg
$PLOT $TABLES/corr_QTavg_Rg.tbl temp.tbl "Average TRAP-TRAP Distance"
sips -s format jpeg output.pdf -o QTavg.jpg
$PLOT $TABLES/corr_QTmax_Rg.tbl temp.tbl "Maximum TRAP-TRAP Distance"
sips -s format jpeg output.pdf -o QTmax.jpg
montage -quiet "QTmin.jpg" "QTavg.jpg" "QTmax.jpg" -geometry 1650x -tile 1x3 "chisq_QT.jpg"

$PLOT $TABLES/corr_QAmin_Rg.tbl temp.tbl "Minimum AT-AT Distance"
sips -s format jpeg output.pdf -o QAmin.jpg
$PLOT $TABLES/corr_QAavg_Rg.tbl temp.tbl "Average AT-AT Distance"
sips -s format jpeg output.pdf -o QAavg.jpg
$PLOT $TABLES/corr_QAmax_Rg.tbl temp.tbl "Maximum AT-AT Distance"
sips -s format jpeg output.pdf -o QAmax.jpg
montage -quiet "QAmin.jpg" "QAavg.jpg" "QAmax.jpg" -geometry 1650x -tile 1x3 "chisq_QA.jpg"

$PLOT $TABLES/corr_QTQAmin_Rg.tbl temp.tbl "Minimum TRAP-AT Distance"
sips -s format jpeg output.pdf -o QTQAmin.jpg
$PLOT $TABLES/corr_QTQAavg_Rg.tbl temp.tbl "Average TRAP-AT Distance"
sips -s format jpeg output.pdf -o QTQAavg.jpg
$PLOT $TABLES/corr_QTQAmax_Rg.tbl temp.tbl "Maximum TRAP-AT Distance"
sips -s format jpeg output.pdf -o QTQAmax.jpg
montage -quiet "QTQAmin.jpg" "QTQAavg.jpg" "QTQAmax.jpg" -geometry 1650x -tile 1x3 "chisq_QTQA.jpg"

rm QT*jpg
rm QA*jpg
rm output.pdf
rm temp.tbl

