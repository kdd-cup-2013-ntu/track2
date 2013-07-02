#!/usr/bin/python
#	is_abbr.py version 1
#	written by Felix Wu. on 2013/6/1
#
#	
import sys
from collections import defaultdict

def split_abbr_full(name):
	full = defaultdict(int)
	abbr = defaultdict(int)
	for word in name.split():
		abbr[word[0]] += 1
		if len(word) > 1:
			full[word] += 1
	return (abbr, full)

def is_subdictset(sub, sup):
	if len(sub) == 0:
		return True
	return min([sub[word] <= sup[word] for word in sub])

def dictset_substract(minuend, subtrahend):
	diffrence = defaultdict(int)
	for word in minuend:
		if minuend[word] - subtrahend[word] > 0:
			diffrence[word] = minuend[word] - subtrahend[word]
	return diffrence


def is_abbr(abbr, extend):
#	Use to speed up
	if not set([x[0] for x in abbr]) <= set([x[0] for x in extend]):
		return False

	if abbr == extend:
		return True

	a_abbr, a_full = split_abbr_full(abbr)
	e_abbr, e_full = split_abbr_full(extend)

	if not is_subdictset(a_abbr, e_abbr):
		return False
	
	if is_subdictset(a_full, e_full):
		return True

	a_remain = dictset_substract(a_full, e_full)
	if len(a_remain) > 1:
		return False
	e_remain = dictset_substract(e_full, a_full)

	# TODO: Do not del with {'matt':2} with {'mattmack':1} This would be accepted and return True.
	# For now, we just believe that there is only one abbr in the name that has more than one character.
	return min([prefix in [full[0:len(prefix)] for full in e_remain if len(full) >= len(prefix)] for prefix in a_remain])

if __name__ == '__main__':
	if len(sys.argv) != 3:
		sys.stderr.write('Usage: %s abbr_name extend_name\n' % (sys.argv[0]))
		exit(1)
	print is_abbr(sys.argv[1], sys.argv[2])
