#!/usr/bin/perl

#
# This program iterates over a set of passed files and removes all entries that have over a specified number of clashes
#
# NOTE: this script requires the clash_count program from the "pdb_score" utilities

$clash_count_bin = '/Volumes/FosterLab/ihms/Projects/TRAP_AT/models/chaining_structure/pdb_score/bin/clash_count';

if ($#ARGV < 1)
{
	print "Usage: rmclash.pl <distance> <count> *pdbs\n";
	exit;
}

# the distance between atoms that defines a clash
$distance = $ARGV[0]*1.0;

# the # of backbone clashes at which point we mark the entry
$n_clash = $ARGV[1]*1.0;

#
#
#

for( $i=3; $i<=$#ARGV; $i++)
{	
	$ret = `$clash_count_bin $distance "$ARGV[$i]"`;
	chomp($ret);
	
	@out = split("\t",$ret);
	
	if ($out[2] > $n_clash)
	{
		print "Marking file '$ARGV[$i]' ($out[2] interatomic distances < $distance)\n";
		`mv "$ARGV[$i]" "$ARGV[$i].clash" `;
	}
}
