#!/usr/bin/env python3
import sys
import collections
import csv
import re
import pickle
from kdd.util import *


def token(name):
    return ''.join(re.sub('[^\w]', '', name).lower().split())

def get_abbr_name(name):
    return [x for x in name if len(x.split('.')) > 1]

def get_full_name(name):
    return [x for x in name if len(x.split('.')) == 1 and len(x) > 1]

def main():
    if len(sys.argv) < 4:
        print('pre_sub_f, partial_output, track2_cn, new_sub_f')
        exit(0)
    aid_with_p_dic = {}

    cn_info_dic = pickle.load(open(sys.argv[3], 'rb'))[0]

    sub_f = open(sys.argv[1])
    sub_f.readline()
    sub_dic = {}

    for line in sub_f:
        line_split = line.split(',')
        aid = line_split[0]
        aids = set(line_split[1].split())
        sub_dic[aid] = aids

    count_dic = collections.defaultdict(set)

    for line in open(sys.argv[2]):
        line_split = line.split()
        aid = line_split[0]
        if len(line.split('-->')[0].split()) == 1 or len(line.split('-->')[1].split()) == 1: continue
        can = line_split[-1]
        aid_name = line.split('-->')[0].split()[1:]

        if len(aid_name) == 2:
            if len(aid_name[0]) < 5 and len(aid_name[1]) < 5:
                continue
        can_name = line.split('-->')[1].split()[:-1]

        if len(can_name) == 2:
            if len(can_name[0]) < 5 and len(can_name[1]) < 5:
                continue
        
        aid_full_word = get_full_name(aid_name)
        can_full_word = get_full_name(can_name)
        aid_abbr_word = get_abbr_name(aid_name)
        can_abbr_word = get_abbr_name(can_name)

        if len(aid_full_word) == 2 and len(aid_abbr_word) == 1:
            count_dic[' '.join(aid_full_word)].add(aid_abbr_word[0])
        if len(can_full_word) == 2 and len(can_abbr_word) == 1:
            count_dic[' '.join(can_full_word)].add(can_abbr_word[0])

    for line in open(sys.argv[2]):
        line_split = line.split()
        aid = line_split[0]
        if len(line.split('-->')[0].split()) == 1 or len(line.split('-->')[1].split()) == 1: continue
        can = line_split[-1]
        aid_name = line.split('-->')[0].split()[1:]

        if len(aid_name) == 2:
            if len(aid_name[0]) < 5 and len(aid_name[1]) < 5:
                continue
        can_name = line.split('-->')[1].split()[:-1]

        if len(can_name) == 2:
            if len(can_name[0]) < 5 and len(can_name[1]) < 5:
                continue
        
        aid_full_word = get_full_name(aid_name)
        can_full_word = get_full_name(can_name)
        aid_abbr_word = get_abbr_name(aid_name)
        can_abbr_word = get_abbr_name(can_name)

        if len(count_dic[' '.join(aid_full_word)]) >= 2 and len(aid_full_word) == 2: continue
        if len(count_dic[' '.join(can_full_word)]) >= 2 and len(can_full_word) == 2: continue


        if int(aid) in cn_info_dic and int(can) in cn_info_dic:
            if are_same_names(cn_info_dic[int(aid)]['name'], cn_info_dic[int(can)]['name']):
                if can not in sub_dic[aid] or aid not in sub_dic[can]:
                    sub_dic[aid].add(can)
                    sub_dic[can].add(aid)
                    for item in sub_dic[aid]:
                        sub_dic[item] = sub_dic[item].union(sub_dic[aid])
                    for item in sub_dic[can]:
                        sub_dic[item] = sub_dic[item].union(sub_dic[can])
            if len(cn_info_dic[int(aid)]['name'].split()) > 2 and len(cn_info_dic[int(can)]['name']) > 2:
                min_full_word_len = min(len(aid_full_word), len(can_full_word))
                if len(set(aid_full_word).intersection(set(can_full_word))) >= min_full_word_len:
                    if can not in sub_dic[aid] or aid not in sub_dic[can]:
                        sub_dic[aid].add(can)
                        sub_dic[can].add(aid)
                        for item in sub_dic[aid]:
                            sub_dic[item] = sub_dic[item].union(sub_dic[aid])
                        for item in sub_dic[can]:
                            sub_dic[item] = sub_dic[item].union(sub_dic[can])
        else:
            if can not in sub_dic[aid] or aid not in sub_dic[can]:
                sub_dic[aid].add(can)
                sub_dic[can].add(aid)
                for item in sub_dic[aid]:
                    sub_dic[item] = sub_dic[item].union(sub_dic[aid])
                for item in sub_dic[can]:
                    sub_dic[item] = sub_dic[item].union(sub_dic[can])

    new_sub_writer = csv.writer(open(sys.argv[4], 'w'))

    new_sub_writer.writerow(['AuthorId','DuplicateAuthorIds'])
    for item in sub_dic.keys():
        new_sub_writer.writerow([item, ' '.join(list(sub_dic[item]))])

if __name__ == '__main__':
    main()
