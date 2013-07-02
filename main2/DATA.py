AuthorPath = '../data/Author.csv'
PaperPath = '../data/Paper.csv'
TrainPath = '../data/Train.csv'
ValidPath = '../data/Valid.csv'
PaperAuthorPath = '../data/PaperAuthor.csv'
import csv

def readinput(input_path):
	table = list()
	with open(input_path, "r") as f:
		reader = csv.reader(f)
		for row in reader:
			table.append(row)
	attr = table.pop(0)
	return attr, table

