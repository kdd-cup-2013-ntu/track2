#!/usr/bin/python -u
import csv, sys, pickle, os
from DATA import *


def main():
	global AuthorPath
	global PaperAuthorPath
	
	if len(sys.argv) != 2:
		sys.stderr.write('Usage: %s raw_name_set_pickle\n' % (sys.argv[0]))
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

	single_dict = dict([(row[0], row[1]) for row in Author_table if row[0] not in dedup_Ids])
	dedup_dict = dict([(row[0], row[1]) for row in Author_table if row[0] in dedup_Ids])
		
	print '#single = ' + str(len(single_dict))
	print '#dedup = ' + str(len(dedup_dict))
	
#	sellect the names in Author.csv
	raw_name_set = set([dedup_dict[authorId] for authorId in dedup_dict])
#	sellect all names in PaperAuthor.csv if the author do not have any name in Author.csv
	raw_name_set |= set([row[2] for row in PaperAuthor_table if row[1] in dedup_dict and dedup_dict[row[1]] == ''])
#	raw_name_set |= set([row[2] for row in PaperAuthor_table if row[1] in dedup_dict])
	print '#raw_name = ' + str(len(raw_name_set))

	with open(sys.argv[1], 'wb') as f:
		pickle.dump(raw_name_set, f)

if __name__ == "__main__":
	main()
