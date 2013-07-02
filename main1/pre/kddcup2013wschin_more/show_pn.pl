#!/usr/bin/perl
my @p;
my @n;
while(<>){
	if(/^\- /){
		push(@n,$_);
	}elsif(/^\+ /){
		push(@p,$_);
	}
}

print $_ foreach(@p);
print $_ foreach(@n);
