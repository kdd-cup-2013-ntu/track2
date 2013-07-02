#!/usr/bin/python
import sys, pickle
from nick_names import *
from chinese_name_list_v4 import *

def select_suffix_dict(suffix_dict):
	for name in suffix_dict.copy():
		if not suffix_dict[name]:
			continue
		if len(name) <= 8:
			del suffix_dict[name]
			continue
		for typoname in suffix_dict[name].copy():
			if name.split()[-1] in chinese_name_list and typoname.split()[-1] in chinese_name_list:
				suffix_dict[name].remove(typoname)
			elif not len(typoname.replace(' ', '')) - len(name.replace(' ', '')) < min(len(typoname.split()[-1]), 4):
				suffix_dict[name].remove(typoname)

def main():

	if len(sys.argv) != 4:
		sys.stderr.write('Usage: %s suffix_dict name_id_pickle_input name_id_pickle_output\n' % (sys.argv[0]))
		exit(1)
	
	with open(sys.argv[1], 'rb') as f:
		suffix_dict = pickle.load(f)
	with open(sys.argv[2], 'rb') as f:
		name_id_dict = pickle.load(f)
	
	select_suffix_dict(suffix_dict)
	for nickname in name_id_dict.copy():
		full_name = replace_nickname(nickname)
		name_id_dict[full_name] |= name_id_dict[nickname]
	for name in suffix_dict:
		for tname in suffix_dict[name]:
			name_id_dict[name] |= name_id_dict[tname]
	
	with open(sys.argv[3], 'wb') as f:
		pickle.dump(name_id_dict, f)


if __name__ == '__main__':
	main()
