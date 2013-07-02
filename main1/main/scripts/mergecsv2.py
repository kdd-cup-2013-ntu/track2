#!/usr/bin/env python3

import sys,os,collections,re,pickle
sys.path.append(os.path.join(os.path.dirname(__file__),'..'))
from kdd.raw import *
from kdd.util import *
from kdd.stats import *

if len(sys.argv)!=5: 
    print('Usage: {0} Author.csv a b output'.format(sys.argv[0]))
    sys.exit(1)

author_path,path_a,path_b,path_out = sys.argv[1:5]

duplicates_a = Duplicates(path_a)
duplicates_b = Duplicates(path_b)
authors = Authors(author_path)
word_freq = collections.defaultdict(int)
high_freq_words = set()

start = start_do('tokenize')
for id in authors:
    authors[id]['name'] = tokenize_name(authors[id]['name'])
    for word in authors[id]['name'].split():
        word_freq[word] += 1
end_do(start)

for word,count in word_freq.items():
    if count>1200:
        high_freq_words.add(word)

start = start_do('merging')
for aid in duplicates_a:
    for aid_b in duplicates_b[aid]:
        new_aids,ignore = duplicates_a.marry(aid,aid_b,True)[0],False
        for word in set(authors[aid]['name'].split()+authors[aid_b]['name'].split()):
            if word in high_freq_words: ignore = True
        if ignore: continue
        if are_similar(set([authors[candidate]['name'] for candidate in new_aids])):
            duplicates_a.marry(aid,aid_b)
end_do(start)

duplicates_a.write(path_out)
