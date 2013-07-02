#!/usr/bin/python -u
import sys, os, pickle
from collections import defaultdict
from multiprocessing import Pool
from time import time
from is_abbr import *


def select_valid_pair(name):
#	select all names as name + suffix. e.g. given 'c j lin' return ('c j lin', set(['c j linton', 'cj lintttt', 'c jlin', 'c jlinx']))
	global filtered_name_set
	ans = set()
	
	a = name.replace(' ', '')
	for tname in filtered_name_set:
		if tname[0] != name[0] or tname == name:
			continue
		b = tname.replace(' ', '')
		if len(a) <= len(b) and a == b[:len(a)]: # loose criteria: a is the prefix of b
			ans.add(tname)
				
	return (name, ans)


def main():
	if len(sys.argv) != 3:
		sys.stderr.write('Usage: %s filtered_name_set_pickle suffix_dict_pickle\n' % (sys.argv[0]))
		exit(1)
	
	global filtered_name_set
	with open(sys.argv[1], 'rb') as f:
		filtered_name_set = pickle.load(f)
	if '' in filtered_name_set:	
		filtered_name_set.remove('')
	p = Pool(8)
	filtered_name_pair_sets = p.map(select_valid_pair, filtered_name_set)
	p.close()
	p.join()
	suffix_dict = defaultdict(set)
	for name, ans in filtered_name_pair_sets:
		suffix_dict[name] |= ans 
	
	with open(sys.argv[2], 'wb') as f:
		pickle.dump(suffix_dict, f)
	

if __name__ == "__main__":
	main()

