#!/usr/bin/perl

#
# This script iterates over a set of passed files and removes all entries that have an RMSD for ALL marker atoms less than the cutoff distance.
# This script requires the rmsd_calc program from the "pdb_score" utilities

# NOTE: this version attempts to cross-match each model with all models that have the same number of matching atoms
#
#
#

if ($#ARGV < 3)
{
	print "Usage: uniquify_all <atomname> <cutoff> *pdbs\n";
	exit;
}

# the atomname to compare (e.g. CA, etc.)
$atomname = $ARGV[0];

# the RMSD cutoff (in Angstroms)
$cutoff = $ARGV[1]*1.0;

#
#
#

# make a copy of the passed files
@files = @ARGV;

$n = ($#files -1);
print "Starting search on $n files, will mark models with '$atomname' ATOMS with RMSD < $cutoff A...\n";

for( $i=2; $i<=$n; $i++)
{	
	if ($files[$i] eq ''){
		next;
	}
	
	@dupes = ();
	for( $j=$i+1; $j<=$n; $j++)
	{
		# if the file has been removed, skip
		if ($files[$j] eq ''){
			next;
		}
		
		$tmp =`rmsd_calc "$atomname" "$files[$i]" "$files[$j]"`;
		@out = split("\t",$tmp);
		
		chomp($out[2]);
		
		# move to the next model if models don't have the same number of matching atoms
		if ( $out[0] =~ /Atom number mismatch/){
			next;
		}
				
		# sometimes, if the centers align very closely, the RMSD will be undefined from the rmsd_calc algorithm
		if($out[2] eq 'NaN')
		{
			print "WARNING: rmsd_calc reported a NaN between files $files[$i] and $files[$j]\n";
			next;
		}

		if (($out[2]*1.0) < $cutoff)
		{
			push( @dupes, $files[$j] );
			`mv "$files[$j]" "$files[$j].duplicate"`;
			
			# remove the file from the array
			$files[$j] = '';
		}
	}
	if( $#dupes == -1){
		print "File $files[$i] has no duplicates.\n";
	}else{
		print "File $files[$i] has ".($#dupes+1)." duplicate(s): ".join( ',', @dupes )."\n";
	}
}

print "Done.\n"
