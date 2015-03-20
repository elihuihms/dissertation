#!/usr/bin/perl

use File::Basename;

#
# Generates a file list of PDBs in a provided directory that have more than a specified number of CA, N, or C atoms within a specified distance 
#

$clash_bin = '/export/foster_group/ihms_scratch/tools/clash_count';
#"/Volumes/FosterLab/users/ihms/Projects/TRAP_AT/models/chain_structure/pdb_score/bin/clash_count";

if( $#ARGV < 2 )
{
	print "Usage: get_clashing_pdb.pl <pdb_dir> <CA/C/N dist> <cutoff>\n";
	exit;
}

@files = glob( "$ARGV[0]/*.pdb" );

for $file (@files)
{
	($name,$path,$suffix) = fileparse($file);

	$s = `$clash_bin $ARGV[1] "$file"`;
	@a = split("\t",$s);
	chomp(@a);
	
	if( $a[2] > $ARGV[2] ){
		print "$name\t$ARGV[1]\t$a[2]\n";
	}
}