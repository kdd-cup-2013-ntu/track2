inputfile = 'tmpdata/a.count.sort'
out1 = open('tmpdata/singleword','w')
out2 = open('tmpdata/dupword','w')

for l in open(inputfile, 'r').readlines():
	if ' 1,' in l:
		out1.write(l)
	elif ',' in l:
		out2.write(l)

out1.close()
out2.close()
