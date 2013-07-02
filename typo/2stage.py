#!/usr/bin/python -u
import csv, re
import sys
import bisect 
from collections import defaultdict
from author_filter import author_name_filter

StopWords = set(['department', 'university','universitt', 'school', 'college' , 'center', 'institute', 'and', 'of', 'technology','state'])


def index(a,x):
    i = bisect.bisect_left(a,x)
    if i!=len(a) and a[i]==x:
        return i
    return -1

def readauthor(input_path):
    table = dict()
    with open(input_path, "r") as f:
        reader = csv.reader(f)
        for idx,row in enumerate(reader):
            #print row
            if idx ==0:
                attr = row
            else:
                table[int(row[0])]=(author_name_filter(row[1]),author_name_filter(row[2]))
    return attr, table

def readRemove(input_path):
    idpair = list()
    npair = list()
    with open(input_path,'r') as f:
        for line in f:
            line = line.strip().split(',')
            aid = int(line[0])
            bid = int(line[2])
            na = line[1].lstrip()
            nb = line[1].lstrip()
            idpair.append((aid,bid))
            npair.append((na,nb))
    return idpair, npair

def WriteFile(final, output_path, aucsv):
    allid = list()
    id2id = defaultdict(list)
    for y in final:
        allid.append(y[0])
        allid.append(y[1])
        id2id[y[0]].append(y[1])
        id2id[y[1]].append(y[0])
    allid = list(set(allid))
    allid = sorted(allid)
    fout = open(output_path,'w')
    fout.write('AuthorId,DuplicateAuthorIds\n')
    for key, value in sorted(aucsv.items()):
        fout.write('%d,%d' % (key,key))
        if index(allid,key) !=-1:
            for bid in id2id[key]:
                if bid != key:
                    fout.write(' %d' % (bid))
        fout.write('\n')
    fout.close()


def main(argv):
    RawDir = '/tmp2/KDDCUP2013/DataAsCsvFiles/'
    TrainFile = RawDir + 'Train.csv'
    AuthorPath = RawDir + 'Author.csv'
  
    Result_path = 'typo.csv'
    att, aucsv = readauthor(AuthorPath)

    AllFile = 'singleanddup'
    aidpair, anpair = readRemove(AllFile)

    final = list()
    tod = list()
    sizet=0

    for idx in range(len(aidpair)):
        aid = aidpair[idx][0] 
        bid = aidpair[idx][1]
        cc = (set(aucsv[aid][1].split()) & set(aucsv[bid][1].split())) - StopWords

        ## Intersect in aff from Author.csv
        if len(cc) > sizet:
            tod.append((aid,bid))
            final.append((aid,bid))
            continue
    WriteFile(final, Result_path,aucsv)
    return

if __name__ == "__main__":
    main(sys.argv)
