#!/usr/bin/perl

#
# When passed a sa.viols file from Xplor-NIH, looks for SAXS term and pulls out interpolated exp. data and fit
#

if( $#ARGV == -1 )
{
	print "Usage: get_sa_saxs.pl *sa.viols > fit.dat\n";
	exit;
}

#
# Example header:
#
#    Calculated I(q) 
#----------------------------------------------------------------------
#       q      I [calc]       I [obs]    Icalc-Iobs   Obs Error   gCorrect
#  0.0106  82.79         84.78        -1.9909        4.3103       0.71856 

# start of saxs data block
$start = 0;

open( SRCFILE, $ARGV[0] ) || die "Can't read '$ARGV[0]': $!\n";
@data = <SRCFILE>;
close( SRCFILE );

$toggle = 0;
for( my $i=0; $i<=$#data; $i++ )
{
	$line = $data[ $i ];
	
	if( $line =~ m/^\s+q\s+I\s+\[calc\]\s+I\s+\[obs\]\s+Icalc-Iobs\s+Obs\s+Error\s+gCorrect/ ){
		$toggle = 1;
		
		print "#q\tI_exp\tI_fit\n";
	}elsif( $toggle == 1 )
	{
		if( $line =~ m/^\s*(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)/ ){
			print "$1\t$3\t$2\n";
		}else{
			last;
		}
	}
}



       