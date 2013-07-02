#!/usr/bin/env python3

import sys,os,collections,re,pickle,copy,itertools
sys.path.append(os.path.join(os.path.dirname(__file__),'..'))
from kdd.raw import *
from kdd.util import *
from kdd.stats import *

if len(sys.argv)<2:
    print('{0} Author.csv prediction output'.format(sys.argv[0]))

authors,duplicates,output = Authors(sys.argv[1]),Duplicates(sys.argv[2]),sys.argv[3]

def have_rich_names(ids):
    names_with_two_words_and_full,faults = set(),0
    for id in ids:
        name = tokenize_name(authors[id]['name'])
        if not is_abbr_name(name) and len(name.split())==2: names_with_two_words_and_full.add(name)
    for a,b in itertools.combinations(names_with_two_words_and_full,2):
        if not may_be_duplicates_partial(a,b): faults += 1
    if faults>=4:
        #print(names_with_two_words_and_full)
        return True
    return False

new_duplicates = copy.deepcopy(duplicates)
for id in duplicates:
    name,dids = authors[id]['name'],duplicates[id]
    #if id==650022: print(id,name,dids,is_abbr_name(name))
    if not (is_abbr_name(name) and len(name.split())==2): continue
    if have_rich_names(dids):
        for did in dids:
            new_duplicates.divorce(did)
new_duplicates.write(output) 
