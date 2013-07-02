#!/usr/bin/env python2
import sys
import collections
import csv
import re
import cPickle

def token(name):
    return ''.join(re.sub('[^\w]', '', name).lower().split())

def tokenize(name):
    return ' '.join(re.sub('[^\w.]', ' ', name).lower().split())

def is_add(name):
    name_post = tokenize(name)
    name_post_full = [x for x in name_post.split() if '.' not in x]
    name_post_abbr = [x for x in name_post.split() if '.' in x]

    if len(name_post_full) == 2 and len(name_post_abbr) == 1 and len(name_post_full[-1]) > 4:
        return True
    if len(name_post_full) > 2 and len(name_post_full[-1]) > 4:
        return True

    if len(name) > 12:
        return True

    if len(min(name_post_full, key=len)) < 4:
        return False

    
    for word in name_post_full:
        if len(word) < 5:
            return False
    return True

def is_add2(name):
    name_post = tokenize(name)
    name_post_full = [x for x in name_post.split() if '.' not in x]

    if len(name) > 15 and len(name_post_full[-1]) > 5:
        return True
    if len(name_post_full) >2 and len(name_post_full[-1]) > 5:
        return True

    return False

def main():
    if len(sys.argv) < 4:
        print 'PaperAuthor, Author, pre_sub_f, new_sub_f'
        exit(0)
    aid_with_p_dic = {}
    name_dic = collections.defaultdict(list)
    true_name_dic = collections.defaultdict(list)
    for pid, aid, name, aff in csv.reader(open(sys.argv[1])):
        aid_with_p_dic[aid] = 0


    for aid, name, aff in csv.reader(open(sys.argv[2])):
        true_name_dic[token(name)].append(aid)

    for aid, name, aff in csv.reader(open(sys.argv[2])):
        if name == '': continue
        if aid not in aid_with_p_dic: continue
        name_dic[token(name)].append(aid)

        if is_add(name):
            name_dic[token(name)[:-1]].append(aid)

        if is_add2(name):
            name_dic[token(name)[:-2]].append(aid)

    sub_f = open(sys.argv[3])
    sub_f.readline()
    sub_dic = {}

    for line in sub_f:
        line_split = line.split(',')
        aid = line_split[0]
        aids = set(line_split[1].split())
        sub_dic[aid] = aids

    for aid, name, aff in csv.reader(open(sys.argv[2])):
        if name == '': continue
        if aid not in aid_with_p_dic: continue
        for can in name_dic[token(name)]:
            if can not in sub_dic[aid] or aid not in sub_dic[can]:
                sub_dic[aid].add(can)
                sub_dic[can].add(aid)
                for item in sub_dic[aid]:
                    sub_dic[item] = sub_dic[item].union(sub_dic[aid])
                for item in sub_dic[can]:
                    sub_dic[item] = sub_dic[item].union(sub_dic[can])

        if is_add(name):
            for can in name_dic[token(name)[:-1]]:
                if can not in sub_dic[aid] or aid not in sub_dic[can]:
                    sub_dic[aid].add(can)
                    sub_dic[can].add(aid)
                    for item in sub_dic[aid]:
                        sub_dic[item] = sub_dic[item].union(sub_dic[aid])
                    for item in sub_dic[can]:
                        sub_dic[item] = sub_dic[item].union(sub_dic[can])

        if is_add2(name):
            for can in name_dic[token(name)[:-2]]:
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
