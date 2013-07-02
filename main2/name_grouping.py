#!/usr/bin/python -u
import sys, pickle
from collections import defaultdict
from multiprocessing import Pool
from copy import deepcopy

def max_common_subgroup(target, abbr_dict, extend_dict):
	not_ambiguous_extend_names = [name for name in extend_dict[target] if extend_dict[target] <= abbr_dict[name] | extend_dict[name]]
	max_not_ambiguous_extend_name = max(not_ambiguous_extend_names, key = lambda x: len(abbr_dict[x]))
	return abbr_dict[max_not_ambiguous_extend_name].copy()

def cut_not_symetric_link(group_dict):
	for extend_name in group_dict:
		for abbr_name in group_dict[extend_name].copy():
			if extend_name not in group_dict[abbr_name]:
				group_dict[extend_name].remove(abbr_name)

def build_transitive_link(group_dict):
	for name in group_dict:
		for t_name in group_dict[name]:
			group_dict[t_name] |= group_dict[name]


def main():
	if len(sys.argv) != 4:
		print 'Usage: %s abbr_dict extend_dict group_dict' % (sys.argv[0])
		exit(1)
	global abbr_dict, extend_dict
	with open(sys.argv[1], 'rb') as f:
		abbr_dict = pickle.load(f)
	with open(sys.argv[2], 'rb') as f:
		extend_dict = pickle.load(f)
	
	all_names = set([name for name in abbr_dict])
	assert all_names == set([name for name in extend_dict])

	p = Pool(8)
	pairs = map(lambda name: (name, max_common_subgroup(name, abbr_dict, extend_dict)), all_names)
	group_dict = dict(pairs)
	p.close()
	p.join()

	cut_not_symetric_link(group_dict)
	build_transitive_link(group_dict)

	with open(sys.argv[3], 'wb') as f:
		pickle.dump(group_dict, f)


if __name__ == "__main__":
	main()
