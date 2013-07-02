# written by Felix Wu
#
#
def read_predict(filename):
	predict = dict()
	with open(filename, 'r') as f:
		for line in f:
			Id, line = line.split(',')
			if Id == 'AuthorId':
				continue
			Id = Id
			line = line.split()
			predict[Id] = set(line)
	return predict

def write_predict(predict, filename, title = True):
	with open(filename, 'w') as f:
		if title:
			f.write('AuthorId,DuplicateAuthorIds\n')
		for Id in predict:
			f.write(str(Id) + ',' + ' '.join(map(str, predict[Id])) + '\n')
