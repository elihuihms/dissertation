#!/usr/bin/perl

#
# When passed a number of output .pdb or .sa files from Xplor-NIH, prints a table of the total energies and violations for each file
#

if( $#ARGV == -1 )
{
	print "Usage: get_sa_energies.pl *pdb > results.tbl\n";
	exit;
}

#
# Example header:
#
#REMARK summary    Name       Energy      RMS     Violations
#REMARK summary total         1671.65                55
#REMARK summary ANGL           295.71    0.667        3
#REMARK summary BOND            81.89    0.006        0
#REMARK summary CDIH           241.77    3.421       35
#REMARK summary HBDB           -89.40                  
#REMARK summary IMPR            84.47    0.693        0
#REMARK summary NOE            405.20    0.051        7
#REMARK summary RDC             57.46    0.298        0
#REMARK summary SAXS            85.91    1.465         
#REMARK summary SYMM             7.89    0.045        0
#REMARK summary VDW            500.75                10
#

@results = ();
@headers = ();

$firstfile = 0;
foreach $file (@ARGV)
{
	open( SRCFILE, $file ) || die "Can't read '$file': $!\n";
	@data = <SRCFILE>;
	close( SRCFILE );
	
	my %fields = {};
	foreach $line (@data)
	{
		if( $line =~ m/^REMARK summary\s+(\w+)\s+(-?\d+\.\d+)\s+\S*\s+(\d*)/ )
		{
			if( $firstfile == 0 ){
				push( @headers, $1 );
			}
			
			if( $1 ne ''){
				$fields{ $1 } = $2;
			}
		}
			
	}
	$firstfile = 1;
	push( @results, { %fields } );
}


print "# pdb"."\t".join( "\t", @headers )."\n";
for( $i=0; $i<=$#ARGV; $i++ )
{
	print $ARGV[ $i ]."\t";
	foreach $field (@headers){
		print $results[ $i ]{ $field }."\t";
	}
	print "\n";
}





