#!/usr/bin/python
import sys, pickle
from collections import defaultdict
from copy import deepcopy
from name_grouping import build_transitive_link
from predict_io import write_predict

def main():

	if len(sys.argv) != 4:
		sys.stderr.write('Usage: %s group_dict_pickle name_id_pickle predict_file\n' % (sys.argv[0]))
		exit(1)

	with open(sys.argv[1], 'rb') as f:
		group_dict = pickle.load(f)
	with open(sys.argv[2], 'rb') as f:
		name_id_dict = pickle.load(f)
	
	name_id_group = defaultdict(set)
	for name in group_dict:
		for cname in group_dict[name]:
			name_id_group[name] |= name_id_dict[cname]
			
	id_group_dict = defaultdict(set)
	for name in name_id_group:
		for authorId in name_id_group[name]:
			id_group_dict[authorId] |= name_id_group[name]
	i = 0
	while True:
		before_modify = deepcopy(id_group_dict)
		build_transitive_link(id_group_dict)
		if before_modify == id_group_dict:
			break
		i += 1
	sys.stderr.write('i = ' + str(i) + '\n')
	write_predict(id_group_dict, sys.argv[3], False)

if __name__ == '__main__':
	main()
