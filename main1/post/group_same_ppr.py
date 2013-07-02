#!/usr/bin/env python2
import sys, csv
import collections
import re

def token(name):
    return ''.join(re.sub('[^\w]', '', name).lower().split())


def main():
    if len(sys.argv) < 3:
        print 'Paper.csv, out_f'
        exit(0)
    ppr_f = open(sys.argv[1], 'r')
    out_f = open(sys.argv[2], 'w')

    ppr_dic = collections.defaultdict(set)

    for pid, name, yr, con_id, jr_id,key in csv.reader(ppr_f):
        if name == '': continue
        ppr_dic[token(name)].add(pid)

    for item in ppr_dic.keys():
        if len(ppr_dic[item]) == 1: continue
        out_f.write('{0}\n'.format(' '.join(list(ppr_dic[item]))))



if __name__ == '__main__':
    main()
