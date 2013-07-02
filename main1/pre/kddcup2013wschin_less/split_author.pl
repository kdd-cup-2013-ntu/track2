#!/usr/bin/perl
use strict;
use Text::CSV;

if(scalar @ARGV < 1){
	print "Usage: perl split_author.pl filename\n";
	print "This function is designed for spliting Author.csv.\n";
	exit 0;
}

open(my $IN,"<",$ARGV[0]) or die "Can not open $ARGV[0] as input.\n";
open(OUTAID,">",$ARGV[0].".aid") or die "Can not open $ARGV[0].aid as output.\n";
open(OUTNAME,">",$ARGV[0].".name") or die "Can not open $ARGV[0].name as output.\n";
open(OUTAFFILIA,">",$ARGV[0].".affilia") or die "Can not open $ARGV[0].affilia as output.\n";

my$csv = Text::CSV->new ({binary => 1,eol => $\});

readline(<IN>);

while(my $row = $csv->getline($IN)){
	my ($AuthorId, $AuthorName, $AuthorAffiliation) = @$row;
	$AuthorName =~ s/\W/ /g;
	print OUTAID "$AuthorId\n";
	print OUTNAME "$AuthorName\n";
	print OUTAFFILIA "$AuthorAffiliation\n";
}
