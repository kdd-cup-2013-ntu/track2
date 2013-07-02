#!/usr/bin/python -u
import sys, pickle
from collections import defaultdict
from name_grouping import *
from chinese_name_list_v4 import *

def cut_chinese_wrong_link(abbr_dict, extend_dict):
#	only preserve the pair abbr_name <--> extend_name, if abbr_name is not Chinese name or is_chinese_abbr(abbr_name, extend_name)
	print 'cut_chinese_wrong_link'
	for abbr_name in extend_dict:
		if not is_chinese_name(abbr_name):
			continue
		for extend_name in extend_dict[abbr_name].copy():
			if not is_chinese_abbr(abbr_name, extend_name): 
				extend_dict[abbr_name].remove(extend_name)
				abbr_dict[extend_name].remove(abbr_name)
						
def remove_concat_name(abbr_dict, extend_dict):
	print 'remove_concat_name'
	name_set = set([name for name in abbr_dict])
	remove_name_set = set()
	concat_dict = defaultdict(set)
#	build the mapping: concatenated name -> set of names
	for name in name_set:
		concat_dict[name.replace(' ', '')].add(name)
	for concat_name in concat_dict:
		if len(concat_dict[concat_name]) == 1:
			continue
		for name in concat_dict[concat_name]:
			if name != max(concat_dict[concat_name], key = len): # only preserve the longest one among all names with same concatenated name
				remove_name_set.add(name)
	remove_name(abbr_dict, extend_dict, remove_name_set)

def remove_name(abbr_dict, extend_dict, remove_name_set):
	new_abbr_dict = defaultdict(set)
	new_extend_dict = defaultdict(set)
	for a in extend_dict:
		if a in remove_name_set:
			continue
		for e in extend_dict[a]:
			if e in remove_name_set:
				continue
			new_abbr_dict[e].add(a)
			new_extend_dict[a].add(e)
	del abbr_dict
	del extend_dict
	abbr_dict = new_abbr_dict
	extend_dict = new_extend_dict

def remove_suffix_name(abbr_dict, extend_dict, suffix_dict):
	print 'remove_suffix_name'
	remove_name_set = set()
	for name in suffix_dict:
		if len(name) <= 8:
			continue
		for typoname in suffix_dict[name].copy():
			if name.split()[-1] in chinese_name_list and typoname.split()[-1] in chinese_name_list:
				remove_name_set.add(typoname)
			elif not len(typoname.replace(' ', '')) - len(name.replace(' ', '')) < min(len(typoname.split()[-1]), 4):
				remove_name_set.add(typoname)
	remove_name(abbr_dict, extend_dict, remove_name_set)

def main():
	if len(sys.argv) != 5:
		print 'Usage: %s suffix_dict abbr_dict extend_dict group_dict' % (sys.argv[0])
		exit(1)
	with open(sys.argv[1], 'rb') as f:
		suffix_dict = pickle.load(f)
	with open(sys.argv[2], 'rb') as f:
		abbr_dict = pickle.load(f)
	with open(sys.argv[3], 'rb') as f:
		extend_dict = pickle.load(f)
	
	all_names = set([name for name in abbr_dict])
	assert all_names == set([name for name in extend_dict])
	cut_chinese_wrong_link(abbr_dict, extend_dict)
	remove_concat_name(abbr_dict, extend_dict)
	remove_suffix_name(abbr_dict, extend_dict, suffix_dict)

	pairs = map(lambda name: (name, max_common_subgroup(name, abbr_dict, extend_dict)), all_names)
	group_dict = dict(pairs)

	cut_not_symetric_link(group_dict)
	build_transitive_link(group_dict)

	with open(sys.argv[4], 'wb') as f:
		pickle.dump(group_dict, f)

if __name__ == "__main__":
	main()
