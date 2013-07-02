import sys, os
import jellyfish
import csv

out1 = 'tmpdata/singlename'
out2 = 'tmpdata/dupname'
out3 = 'singleanddup'
out4 = 'tmpdata/wordtypo'

o1 = open(out1, 'w')
o2 = open(out2, 'w')
o3 = open(out3, 'w')
o4 = open(out4, 'w')

inputfile = '/tmp2/KDDCUP2013/DataAsCsvFiles/Author.csv'

idfindname = dict()
with open(inputfile,'r') as f:
	reader = csv.reader(f)
	for idx,row in enumerate(reader):
		if idx == 0:
			continue
		idfindname[row[0].strip('\n')] = row[1].strip('\n')



inputfile = 'tmpdata/dupword'
dup_name_list = []
dup_id_list = dict()

for l in open(inputfile, 'r').readlines():
	name = l.split()[0]
	count = int(l.split()[1].strip(','))
	id_list = l.split(',')[1]
	dup_id_list[name] = id_list.split()
	dup_name_list.append(name)



inputfile = 'tmpdata/singleword'

for l in open(inputfile, 'r').readlines():
	name = l.split()[0]
	count = int(l.split()[1].strip(','))
	single_id = l.split(',')[1].strip('\n').strip(' ')
	if len(name) < 5: continue
	for dname in dup_name_list:
		if jellyfish.levenshtein_distance(name, dname) == 1:
			for did in dup_id_list[dname]:
				slastname = idfindname[single_id].split()[len(idfindname[single_id].split())-1]
				dlastname = idfindname[did].split()[len(idfindname[did].split())-1]
				slastc = slastname[len(slastname)-1]
				dlastc = dlastname[len(dlastname)-1]
				slastcw = slastname[len(slastname)-2]
				dlastcw = dlastname[len(dlastname)-2]
				if jellyfish.jaro_distance(idfindname[single_id], idfindname[did]) > 0.85 and (len(name) == len(dname) - 1  or len(name) == len(dname) + 1) and idfindname[single_id][0] == idfindname[did][0] and slastname[0] == dlastname[0] and slastc== dlastc and slastcw == dlastcw and idfindname[single_id].lower().replace(' ','').replace('.','').replace('-','') != idfindname[did].lower().replace(' ','').replace('.','').replace('-',''):
					o1.write(idfindname[single_id] + '\n')
					o2.write(idfindname[did] + '\n')
					o3.write( single_id +', '+idfindname[single_id] + ', '+did +', '+ idfindname[did] + '\n')
					o4.write( name + ', ' + dname + '\n')
o1.close()
o2.close()
o3.close()
o4.close()
