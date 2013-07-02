#!/usr/bin/perl
use strict;
if(scalar @ARGV < 1){
	print "Usage: perl filter.pl file [files]\n";
	print "The script will print all alphabelic tokens to STDOUT.\n";
	exit 0;
}

my %dictionary;
foreach my $file(@ARGV){
	open(IN,"<",$file) or die "Can not open $file.\n";
	while(<IN>){
		my $line = $_;
		chomp $line;
=for debug, before replacement
		print "b:$line\n";
=cut
		$line =~ tr/A-Z/a-z/;
		$line =~ s/\W/ /g;
		$line =~ s/\s+/ /g;
=for debug, after replacement
		print "a:$line\n";
=cut
		my @tokens = split(/ /,$line);
		foreach my $tok (@tokens){
=for debug, print all tokens with their decisions
			if($tok =~ /0x\w/i){
				print "- ";
			}elsif($tok =~ /^[0-9]*$/){
				print "- ";
			}else{
				print "+ ";
			}
			print "$tok\n";
=cut
			if($tok =~ /0x\w/i){# hex number
			}elsif($tok =~ /^[0-9]*$/){# dec number
			}else{# word
				$dictionary{$tok}=1;
				#print "$tok\n";
			}
		}
	}
	close(IN);
}

foreach (sort keys %dictionary){
	print "$_\n";
}
