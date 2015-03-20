#!/usr/bin/perl

use File::Slurp;

#
# quick script to perform a NFsim titration, because it looks like you can't change the number of reactants on the fly using the .rnf
#

@titration = (0,100,200,300,400,500,600,700,800,900,1000,1200,1400,1600,1800,2000,2200,2400,2600,2800,3000,3200);

if( ! -e  $ARGV[0] ){
	print "Can't read '$ARGV[0]': $!\n";
	exit;
}

$xml = read_file( $ARGV[0] );

`rm -f temp.gdat`;
`touch temp.gdat`;
for $point (@titration)
{
	$copy = $xml;
	$copy =~ s/\$1/$point/g;

	open( XML_out, '>temp.xml' ) or die("Could not open temp.xml");
	print XML_out $copy;
	close( XML_out );
	
	`../NFsim_i386-darwin -xml temp.xml -cb -bscb -ss state_$point.final -o out_$point.gdat > log_$point.txt`;
	`tail -n 10 out_$point.gdat >> temp.gdat`;
	
	open( FILE, "state_$point.final" ) or die("Couldn't open state_$point.final: $!");
	@lines = <FILE>;
	close( FILE );
	
	$sum = 0;
	$count = 0;
	foreach $line (@lines)
	{
		@matches = $line =~ /(TRAP)/g;
		if( $line =~ m/(\d+)\s$/ ){ $n = $1; }
		
		if( $#matches > -1){
			$count += $n;
			$sum += $n * ($#matches +1);
		}
	}
	$avg = $sum / $count;
	
	print "$point\t$avg\n";	
}

`tconvert -w -ignore temp.gdat > out_compiled.dat`;
$n = ($#titration +1)*10;
$n1 = ($#titration +1)*10 +1;
`teval -f "x[0]" -y -range 1,$n1 -points $n | twrite -col 0 out_compiled.dat`;

