#!/usr/bin/perl
use strict;
if(scalar @ARGV!=6){
	print "Usage: perl show_chinese.pl a_aid a_name ch_name ch_token ban_name ban_token\n";
	exit 0;
}


open(A_AID,"<",$ARGV[0]) or die "Can not open $ARGV[0].\n";
open(A_NAME,"<",$ARGV[1]) or die "Can not open $ARGV[1].\n";
open(CH_NAME,"<",$ARGV[2]) or die "Can not open $ARGV[2].\n";
open(CH_TOKE,"<",$ARGV[3]) or die "Can not open $ARGV[3].\n";


sub how_many_full;
sub who_is_full;
sub list_matching;
sub hash_matching;
sub list_excluding;
sub load_line_to_list;


print "Loading author name.\n";
my %author_name;
while(<A_AID>){
	my $aid=$_;
	chomp $aid;
	my $aname=<A_NAME>;
	chomp $aname;
	push(@{$author_name{$aid}},$aname);
}


print "Load bad list and trust list.\n";
my @ban_list_name=load_line_to_list($ARGV[4]);
my @ban_list_token=load_line_to_list($ARGV[5]);
my %chinese_name;
my %all_chinese_name;
my @all_chinese_name;
my %chinese_token;
my %all_chinese_token;
my @all_chinese_token;
my %wide_range_chinese;
my @wide_range_chinese;

print "Loading chinese name.\n";
while(<CH_NAME>){
	my $line=$_;
	my $matches=0;
	chomp $line;
	$line=~tr/A-Z/a-z/;
	$all_chinese_name{$line}=0;
	$wide_range_chinese{$line}=0;
	foreach(@ban_list_name){
		$matches++ if($line eq $_);
	}
	$chinese_name{$line}=0 if($matches==0);
}

print "Loading chinese token.\n";
while(<CH_TOKE>){
	my $line=$_;
	my $matches=0;
	chomp $line;
	$line=~tr/A-Z/a-z/;
	$line=~s/`//g;
	$all_chinese_token{$line}=0;
	$wide_range_chinese{$line}=0;
	foreach(@ban_list_token){
		$matches++ if($line eq $_);
	}
	$chinese_token{$line}=0 if($matches==0);
}

@all_chinese_name=sort {length($b) <=> length($a)} keys %all_chinese_name;
@all_chinese_token=sort {length($b) <=> length($a)} keys %all_chinese_token;
@wide_range_chinese=sort {length($b) <=> length($a)} keys %wide_range_chinese;

print "Start to detect chinese author.\n";
foreach my $aid(keys %author_name){
	my $length_ok=0;
	my $last_ok=0;
	my $ch_num=0;
	# Check author name in a.csv
	foreach my $name(@{$author_name{$aid}}){
		my $backup=$name;
		$name=~s/\W/ /g;
		$name=~s/ {2,}/ /g;
		$name=~tr/A-Z/a-z/;
		my @tokens=split(/ /,$name);
		my @full;
		@full=who_is_full(\@tokens);
		if(scalar @full==1){
			# maybe we can check number of abbr. also
			my @ch_name_matches=hash_matching(\%chinese_name,\@full);
			my @ch_token_matches=hash_matching(\%chinese_token,\@full);
			my @ch_token_matches_ex=list_excluding(\@ch_token_matches,\@ch_name_matches);
			if(scalar @ch_name_matches>=1 or scalar @ch_token_matches>=1){
				my @ban_name_matches=list_matching(\@ban_list_name,\@full);
				my @ban_token_matches=list_matching(\@ban_list_token,\@full);
				if(scalar @ch_name_matches==1 or scalar @ban_name_matches==1){
					print "+ $aid,$backup\n";
				}else{
					print "- $aid,$backup\n";#,", join(' ',@full), "\n";
				}

			}else{
				if(scalar @ch_name_matches==1){
					print "+ $aid,$backup\n";
				}else{
					print "- $aid,$backup\n";
				}
			}
		}elsif(scalar @full==2){
			# maybe we can check number of abbr. also
			my @ch_name_matches=hash_matching(\%chinese_name,\@full);
			my @ch_token_matches=hash_matching(\%chinese_token,\@full);
			my @ch_token_matches_ex=list_excluding(\@ch_token_matches,\@ch_name_matches);
			if(scalar @ch_name_matches>=1 or scalar @ch_token_matches>=1){
				my @ban_name_matches=list_matching(\@ban_list_name,\@full);
				my @ban_token_matches=list_matching(\@ban_list_token,\@full);
				if(scalar @ch_name_matches>=1 or scalar @ban_name_matches>=1){
					print "+ $aid,$backup\n";
				}else{
					print "- $aid,$backup\n";
				}
			}else{
				if(scalar @ch_name_matches>=1){
					print "+ $aid,$backup\n";
				}else{
					print "- $aid,$backup\n";
				}
			}
		}elsif(scalar @full>=3){
			# maybe we can check number of abbr. also
			my @ch_name_matches=hash_matching(\%chinese_name,\@full);
			my @ch_token_matches=hash_matching(\%chinese_token,\@full);
			my @ch_token_matches_ex=list_excluding(\@ch_token_matches,\@ch_name_matches);
			my $cname=scalar @ch_name_matches;
			my $ctoken=scalar @ch_token_matches_ex;
			if(scalar @ch_name_matches>=1 or scalar @ch_token_matches>=1){
				my @ban_name_matches=list_matching(\@ban_list_name,\@full);
				my @ban_token_matches=list_matching(\@ban_list_token,\@full);
				$cname+=scalar @ban_name_matches;
				$ctoken+=scalar @ban_token_matches;
				if($cname+$ctoken>=scalar(@full)-1){
					print "+ $aid,$backup\n";
				}else{
					print "- $aid,$backup\n";
				}
			}else{
				if($cname+$ctoken>=scalar(@full)-1){
					print "+ $aid,$backup\n";
				}else{
					print "- $aid,$backup\n";
				}
			}
		}
	}
}

sub how_many_full{
	my @tokens=@_;
	my $full=0;
	foreach my $tok(@tokens){
		$tok=~s/\W/ /g;
		$tok=~s/ //g;
		$full++ if (length($tok)>1);
	}
	return $full;
}

sub who_is_full{
	my @tokens=@{$_[0]};
	my @full;
	foreach my $tok(@tokens){
		$tok=~s/\W//g;
		$tok=~s/ //g;
		push(@full,$tok) if (length($tok)>1);
	}
	return @full;
}

sub list_matching{
	my $list_ref=$_[0];
	my $token_ref=$_[1];
	my @matches;
	foreach my $tok(@$token_ref){
		foreach my $ban(@$list_ref){
			if($tok eq $ban){
				push(@matches,$tok);
				last;
			}
		}
	}
	return @matches;
}

sub hash_matching{
	my $hash_ref=$_[0];
	my $token_ref=$_[1];
	my @matches;
	foreach my $tok(@$token_ref){
		my $temp=$tok;
		push(@matches,$temp) if (defined $hash_ref->{$temp});
	}
	return @matches;
}

sub list_excluding{
	my $list_ref1=$_[0];
	my $list_ref2=$_[1];
	my @unique_for_1;
	foreach my $ele(@$list_ref1){
		my $matches=0;
		foreach(@$list_ref2){
			$matches++ if($ele eq $_);
		}
		push(@unique_for_1,$ele) if ($matches==0);
	}
	return @unique_for_1;
}

sub load_line_to_list{
	my $filename=$_[0];
	my %dictionary;
	open(my $fh,"<",$filename) or die "Can not open $filename.\n";
	while(<$fh>){
		chomp;
		tr/A-Z/a-z/;
		$dictionary{$_}=0;
	}
	return sort keys %dictionary;
}
