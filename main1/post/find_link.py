#!/usr/bin/env python3

import sys, csv
from kdd.util import *
import re
import collections

def token(name):
    return re.sub('[^\w.]', ' ', name).lower().split()

def check_name(name1, name2):
    name1_token = token(name1)
    name1_full_word_set = set([x for x in name1_token if len(x.split('.')) == 1])
    name2_token = token(name2)
    name2_full_word_set = set([x for x in name2_token if len(x.split('.')) == 1])

    min_val = min(len(name1_full_word_set), len(name2_full_word_set))

    if len(name1_full_word_set.intersection(name2_full_word_set)) >= min_val:
        return True
    else:
        return False


def main():
    if len(sys.argv) < 5:
        print('same_ppr_ttl, PaperAuthor.csv, Author.csv, out')
        exit(0)
    same_ppr_ttl = open(sys.argv[1], 'r', encoding='utf-8')
    pa_f = open(sys.argv[2], 'r', encoding='utf-8')
    a_f = open(sys.argv[3], 'r', encoding='utf-8')
    out_f = open(sys.argv[4], 'w', encoding='utf-8')

    ppr_athr_dic = collections.defaultdict(set)
    aid_dic = {}
    aid_with_ppr_dic = {}
    for aid, name, aff in csv.reader(a_f):
        aid_dic[aid] = name

    for pid, aid, name, aff in csv.reader(pa_f):
        if aid not in aid_dic: continue
        ppr_athr_dic[pid].add(aid)

    for line in same_ppr_ttl:
        athr_set = set()

        line_split = line.split()

        for pid in line_split:
            athr_set = athr_set.union(ppr_athr_dic[pid])

        for aid in athr_set:
            for aid_can in athr_set:
                if aid == aid_can: continue
                if may_be_duplicates_partial(aid_dic[aid], aid_dic[aid_can]):
                    out_f.write('{0} {1} --> {2} {3}\n'.format(aid, aid_dic[aid], aid_dic[aid_can], aid_can))


if __name__ == '__main__':
    main()
