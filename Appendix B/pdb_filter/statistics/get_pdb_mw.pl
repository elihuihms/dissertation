#!/usr/bin/perl

if( $#ARGV == -1 )
{
	print "Usage: get_pdb_mw.pl <file>\n";
	exit;
}

if( ! -e $ARGV[0] )
{
	print "File $ARGV[0] invalid!\n";
	exit;
}
	
$head = `head -n 50 $ARGV[0]`;
	
$head =~ m/MW\:(\d+?.\d?)\s+/;
print "$ARGV[0]\t$1\n";

