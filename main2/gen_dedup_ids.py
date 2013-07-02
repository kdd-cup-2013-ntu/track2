#!/usr/bin/python -u
import csv, re, sys, os, pickle
from collections import defaultdict
from DATA import *

def main():
	global AuthorPath
	global PaperPath
	global TrainPath
	global ValidPath
	global PaperAuthorPath
	
	if len(sys.argv) != 2:
		sys.stderr.write('Usage: %s output_file\n' % (sys.argv[0]))
		exit(1)

	Author_attr, Author_table = readinput(AuthorPath)
	PaperAuthor_attr, PaperAuthor_table = readinput(PaperAuthorPath)

	single_dict = dict()
	dedup_dict = dict()
	PaperAuthor_dict = defaultdict(set)
	for row in PaperAuthor_table:
		PaperAuthor_dict[row[1]].add(row[2])
	

#	single_dict, dedup_dict, noname_dict: authorId -> name
#	authors do not apppear in PaperAuthor.csv
	single_dict = dict([(row[0], row[1]) for row in Author_table if row[0] not in PaperAuthor_dict])
#	authors apppear in PaperAuthor.csv and have name in Author.csv
	dedup_dict = dict([(row[0], row[1]) for row in Author_table if row[0] in PaperAuthor_dict and row[1] != ''])
#	authors apppear in PaperAuthor.csv and have no name in 
	noname_dict = dict([(row[0], row[1]) for row in Author_table if row[0] in PaperAuthor_dict and row[1] == ''])

#	put the noname authors that have name in PaperAuthor.csv into dedup_dict
	for authorId in noname_dict:
		if ''.join(PaperAuthor_dict[authorId]) == '':
			single_dict[authorId] = ''
		else:
			dedup_dict[authorId] = max(PaperAuthor_dict[authorId], key = len)
		
	print '#single = ' + str(len(single_dict))
	print '#dedup = ' + str(len(dedup_dict))
	
	dedup_ids = set([authorId for authorId in dedup_dict])

	with open(sys.argv[1]+'_single.pkl', 'wb') as f:
		pickle.dump(single_dict, f)
	with open(sys.argv[1]+'_dedup.pkl', 'wb') as f:
		pickle.dump(dedup_dict, f)
	with open('dedup_Ids.pkl', 'wb') as f:
		pickle.dump(dedup_ids, f)
	

if __name__ == "__main__":
	main()
