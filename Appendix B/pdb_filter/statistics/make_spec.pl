#!/usr/bin/perl

if( $#ARGV < 2 )
{
	print "Usage: make_gaussian_spec.pl <PDB_x.txt> <x_center> <x_width> > spec.txt\n";
	exit();
}

if( ! -e $ARGV[0] )
{
	print "File $ARGV[0] does not exist!\n";
	exit();
}

my $file	= $ARGV[0];
my $center	= $ARGV[1] * 1.0;
my $width	= $ARGV[2] * 1.0;

my @PDBs	= split( "\n", `tread -col 0 $file` );
my @Rgs		= split( "\n", `tread -col 1 $file` );

my @weights = [];
my $sum = 0.0;

my $f;
for( my $i=0; $i<=$#PDBs; $i++ )
{
	$f = (1 / ($width * sqrt(2*3.14159))) * exp( -0.5 * (($Rgs[ $i ] - $center) / $width)**2 );
	$weights[$i] = $f;

	if( $f ne 'nan'){
		$sum += $f;
	}
}

for( my $i=0; $i<=$#PDBs; $i++ )
{
	$mes = $PDBs[ $i ];
	$mes =~ s/pdb/mes/g;
	
	print $mes."\t".($weights[$i] / $sum)."\n";
}


