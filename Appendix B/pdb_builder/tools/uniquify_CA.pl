#!/usr/bin/perl

#
# This program iterates over a set of passed files and removes all entries that have an RMSD for ALL marker atoms less than the cutoff distance.
#
# NOTE: this script requires the rmsd_calc program from the "pdb_score" utilities

# NOTE: this is a modified version that uses only CAs
#
#
#

if ($#ARGV < 3)
{
	print "Usage: uniquify_CA.pl <cutoff> *pdbs\n";
	print "Example:\n\tuniquify.pl 10.0 file1.pdb file2.pdb\n";
	exit;
}


@atomnames = [' CA '];

# the RMSD cutoff (in Angstroms)
$cutoff = $ARGV[0]*1.0;

#
#
#

# make a copy of the passed files
@files = @ARGV;

$n = $#files;
print "Starting search on $n files...\n";

for( $i=1; $i<=$#files; $i++)
{
	# print the current progress status
	if ($i % (int($#files / 20)) == 0){
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
		
	
		@out = split("\t",`rmsd_calc ' CA ' "$files[$i]" "$files[$j]"`);
		
		# since the PDBs are generated with increasing numbers of AT and TRAP, once the number of atoms mismatch, we should move to the next model
		if ( $out[0] =~ /Atom number mismatch/){
			next;
		}
			
		# if the centers align very closely, the RMSD will be undefined from the rmsd_calc algorithm
		chomp($out[2]);
		if($out[2] eq 'NaN'){
			$rmsd = 0;
		}else{
			$rmsd = $out[2]*1.00;
		}
		
#		print $files[$i]." vs ".$files[$j]." RMSD:$rmsd, $cutoff\n";

		# only need one significant RMSD to be saveable
		if ($rmsd < $cutoff)
		{
			print "Marking duplicate (".$files[$i].",".$files[$j]." RMSD: ".$rmsd.")\n";
			`mv "$files[$j]" "$files[$j].duplicate"`;
			
			# remove from the array
			delete $files[$j];
		}
	}
}

print "Done.\n"

# cp -RPX 5TRAP_4AT\ copy/curated 5TRAP_4AT/
