#!/usr/bin/python -u
import csv, sys, pickle
from multiprocessing import Pool
from filter_v6 import author_name_filter
from nick_names import replace_nickname
from DATA import *

def readinput(input_path):
	table = list()
	with open(input_path, "r") as f:
		reader = csv.reader(f)
		for row in reader:
			table.append(row)
	attr = table.pop(0)
	return attr, table


def main():
	global AuthorPath
	global PaperAuthorPath
	
	if len(sys.argv) != 3:
		sys.stderr.write('Usage: %s raw_name_set_pickle filtered_name_set_pickle\n' % (sys.argv[0]))
		exit(1)
	with open(sys.argv[1], 'rb') as f:
		raw_name_set = pickle.load(f)

	print '#raw_name = ' + str(len(raw_name_set))
	
	filtered_name_set = set(map(author_name_filter, raw_name_set))
	for name in filtered_name_set.copy():
		filtered_name_set.add(replace_nickname(name))

	print '#filtered_name = ' + str(len(filtered_name_set))

	with open(sys.argv[2], 'wb') as f:
		pickle.dump(filtered_name_set, f)

if __name__ == "__main__":
	main()
