#!/usr/bin/perl

use File::Basename;
use File::Spec;

if( $#ARGV < 0 )
{
	print "Usage: mk_chisq_prog_plot.pl mesmer.log\n";
	exit;
}

# extract the component names and weights
open( FILE, $ARGV[0] ) or die( "Couldn't open \"$ARGV[0]\"\n" );
@lines = <FILE>;
close( FILE );

@best_chisq = [];
@avg_chisq = [];

for( $i=0; $i<=$#lines; $i++ )
{
	if( $lines[$i] =~ m/^(\d+): Best: (\d+\.\d+), Average: (\d+\.\d+),/ )
	{
		push(@best_chisq, $2);
		push(@avg_chisq, $3);
	}
}
		
open( OUT, ">/tmp/temp.tbl" ) or die("Couldn't write to temp file!");
for( $i=1; $i<=$#best_chisq; $i++){
	print OUT $i."\t".$best_chisq[$i]."\t".$avg_chisq[$i]."\n";
}

# open the pipe to GNUPLOT and make it hot
open( GNUPLOT, "| /usr/bin/gnuplot");
select GNUPLOT;
$| = 1;
select STDOUT;

print GNUPLOT <<EOPLOT;
set term postscript enhanced
set output 'chisq_progress.ps'
#set term aqua

set encoding iso_8859_1

set size 1,1

set title '$title'

set xlabel "Iteration"
set ylabel "{/Symbol C}^{2}"

set log y

plot '/tmp/temp.tbl' using 1:2 with lines lc rgb "#FF0000" ti "Best", '/tmp/temp.tbl' using 1:3 with lines lc rgb "#0000FF" ti "Average"
EOPLOT

sleep(2);

`ps2pdf chisq_progress.ps`;
`rm chisq_progress.ps`;


