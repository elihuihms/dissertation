#!/usr/bin/perl

open FILE, $ARGV[0] or die("Could not open ".$ARGV[0]);
@lines = <FILE>;
close( FILE );
chomp( @lines );

@exp_x = ();
@exp_y = ();
@exp_d = ();

@fit_y = ();

foreach $line (@lines)
{
	if( $line =~ /\s+OLIGOMER/ ){
		next;
	}
	
	@values = split(/\s+/, $line);
	
	push( @exp_x, $values[1] );
	push( @exp_y, $values[2] );
	push( @fit_y, $values[3] );
	push( @exp_d, $values[4] );
}

open(TMP, ">/tmp/oligomer_fit.dat") or die("Can't open tmp file for writing: $!");
for( $i=0; $i< $#exp_y; $i++ ){
	if( $fit_y[ $i ] != 0 )
	{
		print TMP $exp_x[$i]."\t".$exp_y[$i]."\t".$fit_y[$i]."\t".($exp_y[$i] / $fit_y[$i])."\n";
	}
}
close(TMP);

write_pars();

$title="\"OLIGOMER Fit To Experimental Data\"";
$subtitle="Result:".$ARGV[0];

$s ="xmgrace ";

$s.=" -graph 0 -p /tmp/xmgrace1.par -pexec 'title $title' -pexec 'subtitle \"$subtitle\"'";
$s.=" -autoscale y -block /tmp/oligomer_fit.dat -type xy -bxy 1:2 -type xy -bxy 1:3";
$s.=" -pexec 'world 0, 1, 0.275, 2000'";

$s.=" -graph 1 -p /tmp/xmgrace2.par -block /tmp/oligomer_fit.dat -bxy 1:4";
$s.=" -pexec 'world 0, 0.75, 0.26, 1.25'";

print `$s`;
`rm /tmp/xmgrace1.par`;
`rm /tmp/xmgrace2.par`;
`tread -col 0 /tmp/oligomer_fit.dat > residuals.dat`;
`tread -col 0 /tmp/oligomer_fit.dat > fit.dat`;
`tread -col 3 /tmp/oligomer_fit.dat | twrite -col 1 residuals.dat`;
`tread -col 2 /tmp/oligomer_fit.dat | twrite -col 1 fit.dat`;
`rm /tmp/oligomer_fit.dat`;

sub write_pars
{
	$string = <<par_END;
# Grace project file
#
version 50122
page size 792, 612
page scroll 5%
page inout 5%
link page off
map font 0 to "Times-Roman", "Times-Roman"
map font 1 to "Times-Italic", "Times-Italic"
map font 2 to "Times-Bold", "Times-Bold"
map font 3 to "Times-BoldItalic", "Times-BoldItalic"
map font 4 to "Helvetica", "Helvetica"
map font 5 to "Helvetica-Oblique", "Helvetica-Oblique"
map font 6 to "Helvetica-Bold", "Helvetica-Bold"
map font 7 to "Helvetica-BoldOblique", "Helvetica-BoldOblique"
map font 8 to "Courier", "Courier"
map font 9 to "Courier-Oblique", "Courier-Oblique"
map font 10 to "Courier-Bold", "Courier-Bold"
map font 11 to "Courier-BoldOblique", "Courier-BoldOblique"
map font 12 to "Symbol", "Symbol"
map font 13 to "ZapfDingbats", "ZapfDingbats"
map color 0 to (255, 255, 255), "white"
map color 1 to (0, 0, 0), "black"
map color 2 to (255, 0, 0), "red"
map color 3 to (0, 255, 0), "green"
map color 4 to (0, 0, 255), "blue"
map color 5 to (255, 255, 0), "yellow"
map color 6 to (188, 143, 143), "brown"
map color 7 to (220, 220, 220), "grey"
map color 8 to (148, 0, 211), "violet"
map color 9 to (0, 255, 255), "cyan"
map color 10 to (255, 0, 255), "magenta"
map color 11 to (255, 165, 0), "orange"
map color 12 to (114, 33, 188), "indigo"
map color 13 to (103, 7, 72), "maroon"
map color 14 to (64, 224, 208), "turquoise"
map color 15 to (0, 139, 0), "green4"
reference date 0
date wrap off
date wrap year 1950
default linewidth 1.0
default linestyle 1
default color 1
default pattern 1
default font 0
default char size 1.000000
default symbol size 1.000000
default sformat "%.8g"
background color 0
page background fill on
timestamp off
timestamp 0.03, 0.03
timestamp color 1
timestamp rot 0
timestamp font 0
timestamp char size 1.000000
timestamp def "Wed Feb 29 14:04:35 2012"
r0 off
link r0 to g0
r0 type above
r0 linestyle 1
r0 linewidth 1.0
r0 color 1
r0 line 0, 0, 0, 0
r1 off
link r1 to g0
r1 type above
r1 linestyle 1
r1 linewidth 1.0
r1 color 1
r1 line 0, 0, 0, 0
r2 off
link r2 to g0
r2 type above
r2 linestyle 1
r2 linewidth 1.0
r2 color 1
r2 line 0, 0, 0, 0
r3 off
link r3 to g0
r3 type above
r3 linestyle 1
r3 linewidth 1.0
r3 color 1
r3 line 0, 0, 0, 0
r4 off
link r4 to g0
r4 type above
r4 linestyle 1
r4 linewidth 1.0
r4 color 1
r4 line 0, 0, 0, 0
g0 on
g0 hidden false
g0 type XY
g0 stacked false
g0 bar hgap 0.000000
g0 fixedpoint off
g0 fixedpoint type 0
g0 fixedpoint xy 0.000000, 0.000000
g0 fixedpoint format general general
g0 fixedpoint prec 6, 6
with g0
    world 0, 1, 0.275, 2000
    stack world 0, 0, 0, 0
    znorm 1
    view 0.150000, 0.150000, 1.150000, 0.850000
    title "OLIGMER Fit To Experimental Data"
    title font 4
    title size 1.500000
    title color 1
    subtitle ""
    subtitle font 4
    subtitle size 1.000000
    subtitle color 1
    xaxes scale Normal
    yaxes scale Logarithmic
    xaxes invert off
    yaxes invert off
    xaxis  on
    xaxis  type zero false
    xaxis  offset 0.000000 , 0.000000
    xaxis  bar on
    xaxis  bar color 1
    xaxis  bar linestyle 1
    xaxis  bar linewidth 1.0
    xaxis  label "q (1/\\cE\\C)"
    xaxis  label layout para
    xaxis  label place auto
    xaxis  label char size 1.000000
    xaxis  label font 4
    xaxis  label color 1
    xaxis  label place normal
    xaxis  tick on
    xaxis  tick major 0.05
    xaxis  tick minor ticks 1
    xaxis  tick default 6
    xaxis  tick place rounded true
    xaxis  tick in
    xaxis  tick major size 1.000000
    xaxis  tick major color 1
    xaxis  tick major linewidth 1.0
    xaxis  tick major linestyle 1
    xaxis  tick major grid off
    xaxis  tick minor color 1
    xaxis  tick minor linewidth 1.0
    xaxis  tick minor linestyle 1
    xaxis  tick minor grid off
    xaxis  tick minor size 0.500000
    xaxis  ticklabel on
    xaxis  ticklabel format general
    xaxis  ticklabel prec 5
    xaxis  ticklabel formula ""
    xaxis  ticklabel append ""
    xaxis  ticklabel prepend ""
    xaxis  ticklabel angle 0
    xaxis  ticklabel skip 0
    xaxis  ticklabel stagger 0
    xaxis  ticklabel place normal
    xaxis  ticklabel offset auto
    xaxis  ticklabel offset 0.000000 , 0.010000
    xaxis  ticklabel start type auto
    xaxis  ticklabel start 0.000000
    xaxis  ticklabel stop type auto
    xaxis  ticklabel stop 0.000000
    xaxis  ticklabel char size 1.000000
    xaxis  ticklabel font 4
    xaxis  ticklabel color 1
    xaxis  tick place normal
    xaxis  tick spec type none
    yaxis  on
    yaxis  type zero false
    yaxis  offset 0.000000 , 0.000000
    yaxis  bar on
    yaxis  bar color 1
    yaxis  bar linestyle 1
    yaxis  bar linewidth 1.0
    yaxis  label "I(q), Intensity"
    yaxis  label layout para
    yaxis  label place auto
    yaxis  label char size 1.000000
    yaxis  label font 4
    yaxis  label color 1
    yaxis  label place normal
    yaxis  tick on
    yaxis  tick major 10
    yaxis  tick minor ticks 9
    yaxis  tick default 6
    yaxis  tick place rounded true
    yaxis  tick in
    yaxis  tick major size 1.000000
    yaxis  tick major color 1
    yaxis  tick major linewidth 1.0
    yaxis  tick major linestyle 1
    yaxis  tick major grid off
    yaxis  tick minor color 1
    yaxis  tick minor linewidth 1.0
    yaxis  tick minor linestyle 1
    yaxis  tick minor grid off
    yaxis  tick minor size 0.500000
    yaxis  ticklabel on
    yaxis  ticklabel format general
    yaxis  ticklabel prec 5
    yaxis  ticklabel formula ""
    yaxis  ticklabel append ""
    yaxis  ticklabel prepend ""
    yaxis  ticklabel angle 0
    yaxis  ticklabel skip 0
    yaxis  ticklabel stagger 0
    yaxis  ticklabel place normal
    yaxis  ticklabel offset auto
    yaxis  ticklabel offset 0.000000 , 0.010000
    yaxis  ticklabel start type auto
    yaxis  ticklabel start 0.000000
    yaxis  ticklabel stop type auto
    yaxis  ticklabel stop 0.000000
    yaxis  ticklabel char size 1.000000
    yaxis  ticklabel font 4
    yaxis  ticklabel color 1
    yaxis  tick place normal
    yaxis  tick spec type none
    altxaxis  off
    altyaxis  off
    legend on
    legend loctype view
    legend 0.2, 0.3
    legend box color 1
    legend box pattern 1
    legend box linewidth 1.0
    legend box linestyle 0
    legend box fill color 0
    legend box fill pattern 0
    legend font 4
    legend char size 1.000000
    legend color 1
    legend length 4
    legend vgap 1
    legend hgap 1
    legend invert false
    frame type 0
    frame linestyle 1
    frame linewidth 1.0
    frame color 1
    frame pattern 1
    frame background color 0
    frame background pattern 0
    s0 hidden false
    s0 type xy
    s0 symbol 1
    s0 symbol size 0.330000
    s0 symbol color 1
    s0 symbol pattern 1
    s0 symbol fill color 1
    s0 symbol fill pattern 0
    s0 symbol linewidth 1.0
    s0 symbol linestyle 1
    s0 symbol char 65
    s0 symbol char font 0
    s0 symbol skip 0
    s0 line type 0
    s0 line linestyle 1
    s0 line linewidth 1.0
    s0 line color 1
    s0 line pattern 1
    s0 baseline type 0
    s0 baseline off
    s0 dropline off
    s0 fill type 0
    s0 fill rule 0
    s0 fill color 1
    s0 fill pattern 1
    s0 avalue off
    s0 avalue type 2
    s0 avalue char size 1.000000
    s0 avalue font 0
    s0 avalue color 1
    s0 avalue rot 0
    s0 avalue format general
    s0 avalue prec 3
    s0 avalue prepend ""
    s0 avalue append ""
    s0 avalue offset 0.000000 , 0.000000
    s0 errorbar on
    s0 errorbar place both
    s0 errorbar color 1
    s0 errorbar pattern 1
    s0 errorbar size 1.000000
    s0 errorbar linewidth 1.0
    s0 errorbar linestyle 1
    s0 errorbar riser linewidth 1.0
    s0 errorbar riser linestyle 1
    s0 errorbar riser clip off
    s0 errorbar riser clip length 0.100000
    s0 comment "Cols 1:2"
    s0 legend  "Experimental profile"
    s1 hidden false
    s1 type xy
    s1 symbol 0
    s1 symbol size 1.000000
    s1 symbol color 2
    s1 symbol pattern 1
    s1 symbol fill color 2
    s1 symbol fill pattern 0
    s1 symbol linewidth 1.0
    s1 symbol linestyle 1
    s1 symbol char 65
    s1 symbol char font 0
    s1 symbol skip 0
    s1 line type 1
    s1 line linestyle 3
    s1 line linewidth 1.5
    s1 line color 2
    s1 line pattern 1
    s1 baseline type 0
    s1 baseline off
    s1 dropline off
    s1 fill type 0
    s1 fill rule 0
    s1 fill color 1
    s1 fill pattern 1
    s1 avalue off
    s1 avalue type 2
    s1 avalue char size 1.000000
    s1 avalue font 0
    s1 avalue color 1
    s1 avalue rot 0
    s1 avalue format general
    s1 avalue prec 3
    s1 avalue prepend ""
    s1 avalue append ""
    s1 avalue offset 0.000000 , 0.000000
    s1 errorbar on
    s1 errorbar place both
    s1 errorbar color 2
    s1 errorbar pattern 1
    s1 errorbar size 1.000000
    s1 errorbar linewidth 1.0
    s1 errorbar linestyle 1
    s1 errorbar riser linewidth 1.0
    s1 errorbar riser linestyle 1
    s1 errorbar riser clip off
    s1 errorbar riser clip length 0.100000
    s1 comment "Cols 1:3"
    s1 legend  "OLIGOMER fit"
par_END

	open(OUTPUT, ">/tmp/xmgrace1.par") or die("Can't open '/tmp/xmgrace1.par' for writing: $!");
	print OUTPUT $string;
	close(OUTPUT);
	
	$string = <<par_END;
# Grace project file
#
version 50122
page size 792, 612
page scroll 5%
page inout 5%
link page off
map font 0 to "Times-Roman", "Times-Roman"
map font 1 to "Times-Italic", "Times-Italic"
map font 2 to "Times-Bold", "Times-Bold"
map font 3 to "Times-BoldItalic", "Times-BoldItalic"
map font 4 to "Helvetica", "Helvetica"
map font 5 to "Helvetica-Oblique", "Helvetica-Oblique"
map font 6 to "Helvetica-Bold", "Helvetica-Bold"
map font 7 to "Helvetica-BoldOblique", "Helvetica-BoldOblique"
map font 8 to "Courier", "Courier"
map font 9 to "Courier-Oblique", "Courier-Oblique"
map font 10 to "Courier-Bold", "Courier-Bold"
map font 11 to "Courier-BoldOblique", "Courier-BoldOblique"
map font 12 to "Symbol", "Symbol"
map font 13 to "ZapfDingbats", "ZapfDingbats"
map color 0 to (255, 255, 255), "white"
map color 1 to (0, 0, 0), "black"
map color 2 to (255, 0, 0), "red"
map color 3 to (0, 255, 0), "green"
map color 4 to (0, 0, 255), "blue"
map color 5 to (255, 255, 0), "yellow"
map color 6 to (188, 143, 143), "brown"
map color 7 to (220, 220, 220), "grey"
map color 8 to (148, 0, 211), "violet"
map color 9 to (0, 255, 255), "cyan"
map color 10 to (255, 0, 255), "magenta"
map color 11 to (255, 165, 0), "orange"
map color 12 to (114, 33, 188), "indigo"
map color 13 to (103, 7, 72), "maroon"
map color 14 to (64, 224, 208), "turquoise"
map color 15 to (0, 139, 0), "green4"
reference date 0
date wrap off
date wrap year 1950
default linewidth 1.0
default linestyle 1
default color 1
default pattern 1
default font 0
default char size 1.000000
default symbol size 1.000000
default sformat "%.8g"
background color 0
page background fill on
timestamp off
timestamp 0.03, 0.03
timestamp color 1
timestamp rot 0
timestamp font 0
timestamp char size 1.000000
timestamp def "Wed Feb 29 14:05:35 2012"
r0 off
link r0 to g0
r0 type above
r0 linestyle 1
r0 linewidth 1.0
r0 color 1
r0 line 0, 0, 0, 0
r1 off
link r1 to g0
r1 type above
r1 linestyle 1
r1 linewidth 1.0
r1 color 1
r1 line 0, 0, 0, 0
r2 off
link r2 to g0
r2 type above
r2 linestyle 1
r2 linewidth 1.0
r2 color 1
r2 line 0, 0, 0, 0
r3 off
link r3 to g0
r3 type above
r3 linestyle 1
r3 linewidth 1.0
r3 color 1
r3 line 0, 0, 0, 0
r4 off
link r4 to g0
r4 type above
r4 linestyle 1
r4 linewidth 1.0
r4 color 1
r4 line 0, 0, 0, 0
g1 on
g1 hidden false
g1 type XY
g1 stacked false
g1 bar hgap 0.000000
g1 fixedpoint off
g1 fixedpoint type 0
g1 fixedpoint xy 0.000000, 0.000000
g1 fixedpoint format general general
g1 fixedpoint prec 6, 6
with g1
    world 0, 0.75, 0.26, 1.25
    stack world 0, 0, 0, 0
    znorm 1
    view 0.600000, 0.500000, 1.129118, 0.830000
    title ""
    title font 0
    title size 1.500000
    title color 1
    subtitle ""
    subtitle font 0
    subtitle size 1.000000
    subtitle color 1
    xaxes scale Normal
    yaxes scale Normal
    xaxes invert off
    yaxes invert off
    xaxis  on
    xaxis  type zero false
    xaxis  offset 0.000000 , 0.000000
    xaxis  bar on
    xaxis  bar color 1
    xaxis  bar linestyle 1
    xaxis  bar linewidth 1.0
    xaxis  label "q (1/\\cE\\C)"
    xaxis  label layout para
    xaxis  label place auto
    xaxis  label char size 0.740000
    xaxis  label font 4
    xaxis  label color 1
    xaxis  label place normal
    xaxis  tick on
    xaxis  tick major 0.1
    xaxis  tick minor ticks 1
    xaxis  tick default 6
    xaxis  tick place rounded true
    xaxis  tick in
    xaxis  tick major size 1.000000
    xaxis  tick major color 1
    xaxis  tick major linewidth 1.0
    xaxis  tick major linestyle 1
    xaxis  tick major grid off
    xaxis  tick minor color 1
    xaxis  tick minor linewidth 1.0
    xaxis  tick minor linestyle 1
    xaxis  tick minor grid off
    xaxis  tick minor size 0.500000
    xaxis  ticklabel on
    xaxis  ticklabel format general
    xaxis  ticklabel prec 5
    xaxis  ticklabel formula ""
    xaxis  ticklabel append ""
    xaxis  ticklabel prepend ""
    xaxis  ticklabel angle 0
    xaxis  ticklabel skip 0
    xaxis  ticklabel stagger 0
    xaxis  ticklabel place normal
    xaxis  ticklabel offset auto
    xaxis  ticklabel offset 0.000000 , 0.010000
    xaxis  ticklabel start type auto
    xaxis  ticklabel start 0.000000
    xaxis  ticklabel stop type auto
    xaxis  ticklabel stop 0.000000
    xaxis  ticklabel char size 0.740000
    xaxis  ticklabel font 4
    xaxis  ticklabel color 1
    xaxis  tick place normal
    xaxis  tick spec type none
    yaxis  on
    yaxis  type zero false
    yaxis  offset 0.000000 , 0.000000
    yaxis  bar on
    yaxis  bar color 1
    yaxis  bar linestyle 1
    yaxis  bar linewidth 1.0
    yaxis  label "I(q)\\sexp\\N / I(q)\\sfit\\N"
    yaxis  label layout para
    yaxis  label place auto
    yaxis  label char size 0.740000
    yaxis  label font 4
    yaxis  label color 1
    yaxis  label place normal
    yaxis  tick on
    yaxis  tick major 0.2
    yaxis  tick minor ticks 1
    yaxis  tick default 6
    yaxis  tick place rounded true
    yaxis  tick in
    yaxis  tick major size 1.000000
    yaxis  tick major color 1
    yaxis  tick major linewidth 1.0
    yaxis  tick major linestyle 1
    yaxis  tick major grid off
    yaxis  tick minor color 1
    yaxis  tick minor linewidth 1.0
    yaxis  tick minor linestyle 1
    yaxis  tick minor grid off
    yaxis  tick minor size 0.500000
    yaxis  ticklabel on
    yaxis  ticklabel format general
    yaxis  ticklabel prec 5
    yaxis  ticklabel formula ""
    yaxis  ticklabel append ""
    yaxis  ticklabel prepend ""
    yaxis  ticklabel angle 0
    yaxis  ticklabel skip 0
    yaxis  ticklabel stagger 0
    yaxis  ticklabel place normal
    yaxis  ticklabel offset auto
    yaxis  ticklabel offset 0.000000 , 0.010000
    yaxis  ticklabel start type auto
    yaxis  ticklabel start 0.000000
    yaxis  ticklabel stop type auto
    yaxis  ticklabel stop 0.000000
    yaxis  ticklabel char size 0.740000
    yaxis  ticklabel font 4
    yaxis  ticklabel color 1
    yaxis  tick place normal
    yaxis  tick spec type none
    altxaxis  off
    altyaxis  off
    legend on
    legend loctype view
    legend 0.5, 0.8
    legend box color 1
    legend box pattern 1
    legend box linewidth 1.0
    legend box linestyle 1
    legend box fill color 0
    legend box fill pattern 1
    legend font 0
    legend char size 1.000000
    legend color 1
    legend length 4
    legend vgap 1
    legend hgap 1
    legend invert false
    frame type 0
    frame linestyle 1
    frame linewidth 1.0
    frame color 1
    frame pattern 1
    frame background color 0
    frame background pattern 0
    s0 hidden false
    s0 type xy
    s0 symbol 0
    s0 symbol size 1.000000
    s0 symbol color 4
    s0 symbol pattern 1
    s0 symbol fill color 4
    s0 symbol fill pattern 0
    s0 symbol linewidth 1.0
    s0 symbol linestyle 1
    s0 symbol char 65
    s0 symbol char font 0
    s0 symbol skip 0
    s0 line type 1
    s0 line linestyle 1
    s0 line linewidth 1.5
    s0 line color 4
    s0 line pattern 1
    s0 baseline type 0
    s0 baseline off
    s0 dropline off
    s0 fill type 0
    s0 fill rule 0
    s0 fill color 1
    s0 fill pattern 1
    s0 avalue off
    s0 avalue type 2
    s0 avalue char size 1.000000
    s0 avalue font 0
    s0 avalue color 1
    s0 avalue rot 0
    s0 avalue format general
    s0 avalue prec 3
    s0 avalue prepend ""
    s0 avalue append ""
    s0 avalue offset 0.000000 , 0.000000
    s0 errorbar on
    s0 errorbar place both
    s0 errorbar color 4
    s0 errorbar pattern 1
    s0 errorbar size 1.000000
    s0 errorbar linewidth 1.0
    s0 errorbar linestyle 1
    s0 errorbar riser linewidth 1.0
    s0 errorbar riser linestyle 1
    s0 errorbar riser clip off
    s0 errorbar riser clip length 0.100000
    s0 legend  ""
par_END

	open(OUTPUT, ">/tmp/xmgrace2.par") or die("Can't open '/tmp/xmgrace2.par' for writing: $!");
	print OUTPUT $string;
	close(OUTPUT);
}
