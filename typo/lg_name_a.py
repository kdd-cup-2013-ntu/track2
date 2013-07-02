#!/usr/bin/env python
import os, sys, cPickle, csv
import re
import collections

def lev_dis(s1, s2):
    if len(s1) < len(s2):
        return lev_dis(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = xrange(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

def token(name):
    name.replace('\'', ' ')
    return re.sub('[^\w.]', ' ', name).lower() 

def main():
    if len(sys.argv) < 2:
        print 'PaperAuthor.csv Author.csv'
        exit(0)
    pa_f = open(sys.argv[1], 'r')
    a_f = open(sys.argv[2], 'r')
    outfile = 'tmpdata/a.count'
    out = open(outfile, 'w')

    athr_with_ppr_dic = {}
    athr_dic = {}

    for pid, aid, name, aff in csv.reader(pa_f):
	athr_with_ppr_dic[aid] = 1

    word_count_dic = collections.defaultdict(int)
    word_count_id_dic = collections.defaultdict(list)

    for aid, name, aff in csv.reader(a_f):
#	if aid not in athr_with_ppr_dic:continue
        name_post = token(name)
        name_split = name_post.split()
	athr_dic[aid] = 1

        for word in name_split:
            if len(word) > 5:
                word_count_dic[word.lower()] += 1
		if aid in athr_with_ppr_dic:
			word_count_id_dic[word.lower()].append(aid)

    #print word_count_id_dic['pohlmann']
    for item in word_count_dic.keys():
        #if word_count_dic[item] == 1 and word_count_id_dic[item][0] not in athr_dic:
	if word_count_id_dic[item] == []:
	    continue
	line = item + ' ' + str(word_count_dic[item]) + ','
	for i in word_count_id_dic[item]:
	    line = line + ' ' + str(i)
	out.write(line + '\n')

    out.close()
    #print item, word_count_dic[item]
	
if __name__ == '__main__':
    main()
