#!/usr/bin/perl

use File::Basename;
use File::Spec;

if( $#ARGV < 2 )
{
	print "Usage: make_all_conf_plot.pl <x_y.tbl> <target_spec_file.txt> <resultdir/ensembles_n.dat> \n";
	exit;
}

for( $i=0; $i<$#ARGV; $i++)
{
	if( ! -e $ARGV[$i] )
	{
		print "Could not open $f\n";
		exit;
	}
}
open( FILE, $ARGV[0] ) or die( "Couldn't open \"$ARGV[0]\"\n" );
@lines = <FILE>;
close( FILE );

%x = {};
%y = {};

for( $i=0; $i<=$#lines; $i++ )
{
	@a = split("\t", $lines[$i]);
	chomp( @a );
	$x{ $a[2] } = $a[0];
	$y{ $a[2] } = $a[1];
}

# if user specified a specific fit, use that. Otherwise, get latest fit
$path = File::Spec->rel2abs( $ARGV[2] );

if( -f $path ){
	$file = $path;
}elsif( -d $path ){
	$file = getLatestEnsemble( $path );
}

# extract the component names and weights
open( FILE, $file ) or die( "Couldn't open \"$file\"\n" );
@lines = <FILE>;
close( FILE );

%ret_col_1 = {};
%ret_col_2 = {};
%ret_col_3 = {};

for( $i=0; $i<=$#lines; $i++ )
{
	if( $lines[$i] =~ m/^(\d+)\s+(\d+\.\d+)\s+(.+)\s/ )
	{
		@conformers = split("\t", $3);
		
		for $conf (@conformers)
		{
			@a = split(":", $conf);
			
			$ret_col_1{ $a[0].".pdb" } = $x{ $a[0].".pdb" };
			$ret_col_2{ $a[0].".pdb" } = $y{ $a[0].".pdb" };
			$ret_col_3{ $a[0].".pdb" } += $a[1];
			#$ret_col_3{ $a[0].".pdb" } = 1.0;
		}
	}
}
		
open( OUT, ">/tmp/temp1.tbl" ) or die("Couldn't write to temp file!");
while( ($key, $value) = each(%ret_col_1) )
{
	if( ($value ne '') and ($value ne 'nan') )
	{
		print OUT $ret_col_1{$key}."\t".$ret_col_2{$key}."\t".$ret_col_3{$key}."\n";
	}
}

`tread -col 0 $ARGV[0] > /tmp/temp.tbl`;
`tread -col 1 $ARGV[0] | twrite -col 1 /tmp/temp.tbl`;
`tread -col 1 $ARGV[1] | twrite -col 2 /tmp/temp.tbl`;
`tread -col 1 $ARGV[1] > /tmp/sort.dat`;
`cat /tmp/temp.tbl | tsnort -by /tmp/sort.dat > /tmp/temp2.tbl`;

$max = `tread -col 2 /tmp/temp2.tbl | tcalc -max`;
$multiplier = 255 / $max;

$max2 = `tread -col 2 /tmp/temp1.tbl | tcalc -max`;
$multiplier2 = 5 / $max2;

$s = basename( $ARGV[1] );
$s =~ m/^(.+)\.(.+)/;
$s1 = $1;
$s = basename( $file );
$s =~ m/^(.+)\.(.+)/;
$s2 = $1;

$title = "$s1 : $s2";
$title =~ s/\_/\\\_/g;

$output = "output.ps";

$x_label = $ARGV[3];
$y_label = "R_{g}";

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

plot '/tmp/temp2.tbl' using 1:2:3:(rgb(max(\$3),0,0)) with points pt 6 ps 0.7 lc rgb variable, '/tmp/temp1.tbl' using 1:2:(\$3*$multiplier2) with points pt 7 ps variable lc rgb '#0066FF'
EOPLOT

sleep(2);

`ps2pdf $output`;
`rm $output`;

sub getLatestEnsemble
{
	@files = glob( "$_[0]/ensembles_*.dat" );
	@files = sort( @files );
	return $files[ $#files ];
}

