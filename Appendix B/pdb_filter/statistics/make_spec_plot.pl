#!/usr/bin/perl

use File::Basename;

if( $#ARGV < 1 )
{
	print "Usage: make_spec_plot.pl <x_y.tbl> <target_spec_file.txt>\n";
	exit;
}

if( !-e $ARGV[0] )
{
	print "Could not open $ARGV[0]\n";
	exit;
}

if( !-e $ARGV[1] )
{
	print "Could not open $ARGV[1]\n";
	exit;
}

`tread -col 0 $ARGV[0] > /tmp/temp1.tbl`;
`tread -col 1 $ARGV[0] | twrite -col 1 /tmp/temp1.tbl`;
`tread -col 1 $ARGV[1] | twrite -col 2 /tmp/temp1.tbl`;
`tread -col 1 $ARGV[1] > /tmp/sort.dat`;
`cat /tmp/temp1.tbl | tsnort -by /tmp/sort.dat > /tmp/temp.tbl`;

$max = `tread -col 2 /tmp/temp.tbl | tcalc -max`;
$multiplier = 255 / $max;

$title = basename( $ARGV[1] );
$title =~ s/\_/\\\_/g;

$x_label = $ARGV[2];
$y_label = "R_{g}";

$output = basename( $ARGV[1] );
$output =~ /^(\w+)\.(\w+)/;
$output = $1.".ps";
$output = "output.ps";

# open the pipe to GNUPLOT and make it hot
open( GNUPLOT, "| /usr/bin/gnuplot");
select GNUPLOT;
$| = 1;
select STDOUT;

print GNUPLOT <<EOPLOT;
set term postscript enhanced
set output '$output'
#set term aqua

set encoding iso_8859_1

set size 1,1

set title '$title'
set nokey

set xlabel "$x_label"
set ylabel "$y_label"

max(a) = $multiplier*a
rgb(r,g,b) = int(r)*65536 + int(g)*256 + int(b)

plot '/tmp/temp.tbl' using 1:2:3:(rgb(max(\$3),0,0)) with points pt 6 ps 0.7 lc rgb variable
EOPLOT

sleep(1);

`ps2pdf $output`;
`rm $output`;
