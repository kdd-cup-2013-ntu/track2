#!/usr/bin/python
import sys, pickle, os
from DATA import *
from collections import defaultdict
from filter_v6 import author_name_filter

def main():
	global AuthorPath
	global PaperAuthorPath

	if len(sys.argv) != 2:
		sys.stderr.write('Usage: %s more_name_dict_pickle\n' % (sys.argv[0]))
		exit(1)
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
	PaperAuthor_attr, PaperAuthor_table = readinput(PaperAuthorPath)

	print 'stage 0'
#	reproduce dedup_dict
	dedup_dict = dict([(row[0], author_name_filter(row[1])) for row in Author_table if row[0] in dedup_Ids])
	more_name_dict = defaultdict(set)
	print 'stage 1'
#	derive all name of authorIds dedup_dict in PaperAuthor.csv
	for row in PaperAuthor_table:
		authorId = row[1]
		if authorId in dedup_Ids:
			more_name_dict[authorId].add(author_name_filter(row[2]))
	print 'stage 2'

	with open(sys.argv[1], 'wb') as f:
		pickle.dump(more_name_dict, f)


if __name__ == '__main__':
	main()
