#!/usr/bin/python -u
import sys, pickle

def main():
	if len(sys.argv) != 2:
		sys.stderr.write('Usage: %s input_file\n' % (sys.argv[0]))
		exit(1)

	with open(sys.argv[1], 'rb') as f:
		single_dict = pickle.load(f)

	sys.stderr.write('#single = ' + str(len(single_dict)) + '\n')

	print 'AuthorId,DuplicateAuthorIds'
	for authorId in single_dict:
		print authorId + ',' + authorId

if __name__ == "__main__":
	main()
