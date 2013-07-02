#!/usr/bin/python
import sys, pickle, os
from DATA import *
from collections import defaultdict
from is_abbr import is_abbr
from name_grouping import max_common_subgroup
from filter_v6 import author_name_filter
from chinese_name_list_v4 import *

def link_concat_names(name_id_dict):
	print 'link_concat_names'
	concat_dict = defaultdict(set)
	for name in name_id_dict:
		concat_dict[name.replace(' ', '')].add(name)
	for concat_name in concat_dict:
		if len(concat_dict[concat_name]) == 1:
			continue
		for name in concat_dict[concat_name]:
			for uname in concat_dict[concat_name]:
				name_id_dict[name].update(name_id_dict[uname])
def main():
	global AuthorPath
	global PaperAuthorPath

	if len(sys.argv) != 3:
		sys.stderr.write('Usage: %s more_name_dict name_id_pickle\n' % (sys.argv[0]))
		exit(1)
		
	with open(sys.argv[1], 'rb') as f:
		more_name_dict = pickle.load(f)

	if os.path.isfile('/tmp2/Simplex/kdd2013/competition/pkl/dedup_Ids.pkl'):
		with open('/tmp2/Simplex/kdd2013/competition/pkl/dedup_Ids.pkl', 'rb') as f:
			dedup_Ids = pickle.load(f)
	elif os.path.isfile('dedup_Ids.pkl'):
		with open('dedup_Ids.pkl', 'rb') as f:
			dedup_Ids = pickle.load(f)
	else:
		sys.stderr.write('Error: cannot find dedup_Ids.pkl')
		exit(1)

	Author_attr, Author_table = readinput(AuthorPath)
	dedup_dict = dict([(row[0], author_name_filter(row[1])) for row in Author_table if row[0] in dedup_Ids])
	


	name_id_dict = defaultdict(set)
	# Restrict to common and not abbr
	for authorId in dedup_dict:
		origin_name = dedup_dict[authorId]
		if origin_name == '':
			extends = more_name_dict[authorId]
			for name in extends:
				name_id_dict[name].add(authorId)
		else:
			name_id_dict[origin_name].add(authorId)
			more_name_dict[authorId].add(origin_name)
			sub_dict = defaultdict(set)
			sup_dict = defaultdict(set)
			for a in more_name_dict[authorId]:
				for e in more_name_dict[authorId]:
					if is_abbr(a, e) and ((not is_chinese_name(a) or not is_chinese_name(e)) or is_chinese_abbr(a,e)):
						sub_dict[e].add(a)
						sup_dict[a].add(e)
			for name in sup_dict[origin_name] | sub_dict[origin_name]: # The best of our team on the leaderboard used only sup_dict[origin_name]
				name_id_dict[name].add(authorId)

	link_concat_names(name_id_dict)
	
	with open(sys.argv[2], 'wb') as f:
		pickle.dump(name_id_dict, f)
	

if __name__ == '__main__':
	main()
