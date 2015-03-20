#!/usr/bin/perl

#
# This program iterates over a set of passed files and removes all entries that have an RMSD for ALL marker atoms less than the cutoff distance.
#
# NOTE: this script requires the rmsd_calc program from the "pdb_score" utilities

#
#
#

if ($#ARGV < 3)
{
	print "Usage: uniquify.pl <cutoff> <atomlist> *pdbs\n";
	print "Example:\n\tuniquify.pl 10.0 ' CA ' file1.pdb file2.pdb\n";
	print "or\n\tuniquify.pl 10.0 'Zn1 ','Zn2 ' *pdb\n";
	print "Note: atom names must be 4 characters long.\n";
	exit;
}

# the RMSD cutoff (in Angstroms)
$cutoff = $ARGV[0]*1.0;

# get the list of atomnames we are to compare e.g. (' CA ')
@atomnames = split(/,/, $ARGV[1]);

#
#
#

# make a copy of the passed files
@files = @ARGV;

$n = $#files -1;
print "Starting search on $n files...\n";

for( $i=2; $i<=$#files; $i++)
{
	# print the current progress status
	if ($i % (int($#files / 20)+1) == 0){
		print int(($i / $#files)*100)."% ";
	}
	
	if ($files[$i] eq ''){
		next;
	}
		
	for( $j=$i+1; $j<=$#files; $j++)
	{		
		if ($files[$j] eq ''){
			next;
		}
	
		# assume bad until proven otherwise
		$bad = 1;
		for ( $k=0; $k <= $#atomnames; $k++)
		{
			@out = split("\t",`rmsd_calc '$atomnames[$k]' "$files[$i]" "$files[$j]"`);
			
			# if the centers align closely, the RMSD will be undefined from the rmsd_calc algorithm
			chomp($out[2]);
			if($out[2] eq 'NaN'){
				$rmsd = 0;
			}else{
				$rmsd = $out[2]*1.00;
			}
			
#			print $files[$i]." vs ".$files[$j]." RMSD:$rmsd, $cutoff\n";

			# only need one significant RMSD to be saveable
			if ($rmsd > $cutoff){ $bad = 0; }
		}

		if( $bad > 0 )
		{
			print "Marking duplicate (".$files[$i]." = ".$files[$j].")\n";
			`mv "$files[$j]" "$files[$j].duplicate"`;
			
			# remove from the array
			delete $files[$j];
		}
	}
}

print "Done.\n"

# cp -RPX 5TRAP_4AT\ copy/curated 5TRAP_4AT/
