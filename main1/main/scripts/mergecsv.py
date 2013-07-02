#!/usr/bin/env python3

import sys,os,collections,re,pickle
sys.path.append(os.path.join(os.path.dirname(__file__),'..'))
from kdd.raw import *
from kdd.util import *
from kdd.stats import *

if len(sys.argv)!=4: 
    print('Usage: {0} a b output'.format(sys.argv[0]))
    sys.exit(1)

path_a,path_b,path_out = sys.argv[1:4]

duplicates_a = Duplicates(path_a)
duplicates_b = Duplicates(path_b)

start = start_do('merging')
for aid in duplicates_a:
    for aid_b in duplicates_b[aid]:
        duplicates_a.marry(aid,aid_b)
end_do(start)

duplicates_a.write(path_out)
