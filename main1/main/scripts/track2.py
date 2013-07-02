#!/usr/bin/env python3

import sys,os,collections,re,pickle,copy,itertools
sys.path.append(os.path.join(os.path.dirname(__file__),'..'))
from kdd.raw import *
from kdd.util import *
from kdd.stats import *

#global variables
NR_STAGES,CUR_STAGE,STAGES,FREQ_THRS,authors,candidates,duplicates,output_rank,aids,sorted_authors,marry_ranks,black_list,log = 12,0,{0:'tokenize',1:'clean',2:'scan',3:'link',4:'marry1',5:'marry2',6:'marry3',7:'marry4',8:'marry5',9:'marry6',10:'marry7',11:'marry8'},50,None,collections.defaultdict(set),None,None,None,[],{},set(),None

# This options are not be used for generating the final model, they are for development.
def exit_with_help():
    print('''usage: {0} [options] src dst
-k <start_stage>:<end_stage>:
    0:  tokenize
    1:  clean
    2:  scan
    3:  link
    4:  marry1
    5:  marry2
    6:  marry3
    7:  marry4
    8:  marry5
-w: dump the result of every stage into the disk
-l <log>: write log
-r <rank>: write rank'''.format(sys.argv[0]))
    sys.exit(1)

def parse_options():
    global options,output_rank,log
    if len(sys.argv)<3: exit_with_help()
    options = {'start_stage':0,'end_stage':NR_STAGES,'write':False,'src':sys.argv[-2],'dst':sys.argv[-1]}
    i,argv = 0,sys.argv[1:-2]
    while i < len(argv):
        if argv[i] == '-w':
            options['write'] = True
            i += 1
        elif argv[i] == '-r':
            output_rank = open(argv[i+1],'w')
            i += 2
        elif argv[i] == '-l':
            log = open(argv[i+1],'w')
            i += 2
        elif argv[i] == '-k':
            start_stage,end_stage = argv[i+1].split(':')
            options['start_stage'] = 0 if start_stage=='' else int(start_stage)
            options['end_stage'] = NR_STAGES if end_stage=='' else int(end_stage)
            i += 2
        else:
            print('invalid option: {0}'.format(argv[i+1]))
            sys.exit(1)
    if not options['src'].endswith('.dump'):
        print('The extension of the source file should be .dump')
        sys.exit(1)
    options['src'] = os.path.splitext(options['src'])[0]
    options['dst'] = os.path.splitext(options['dst'])[0]

#0 tokenize authors names and aliases using tokenize_name in util.py
def tokenize():
    global authors
    start,new_authors = start_do('tokenize'),copy.copy(authors)
    for id,author in authors.items():
        new_authors[id]['name'],new_aliases = tokenize_name(authors[id]['name']),set()
        for name in author['aliases']:
            new_aliases.add(tokenize_name(name))
            #print('{0}  -->  {1}'.format(name,tokenize_name(name)))
        new_authors[id]['aliases'] = new_aliases
    authors = new_authors
    end_do(start)

#1 remove aliases that are not similar to raw name. (use may_be_duplicates in util.py)
def clean():
    global authors
    start = start_do('clean')
    for id,author in authors.items():
        new_aliases = set()
        for alias in author['aliases']:
            if may_be_duplicates(author['name'],alias):
                new_aliases.add(alias) 
        author['aliases'] = new_aliases
    end_do(start)

#2 extract keys from authors names and a construct dictionary "candidates"
#  For examples, for an authors name "c. j. lin" whose aid is 100, we do the following operations:
#  candidates[frozenset('c',)]].add(100)
#  candidates[frozenset('j',)]].add(100)
#  ...
#  candidates[frozenset('c','lin')]].add(100)
#  ...
#  candidates[frozenset('c','j','lin')]].add(100)
def scan():
    global candidates
    def are_all_abbr(words):
        ret = True
        for word in words:
            if not is_abbr_word(word):
                ret = False
        return ret
    start = start_do('scan')
    for id,author in authors.items():
        for alias in author['aliases']:
            alias = set([x.replace('.','') for x in alias.split()])
            for k in range(1,4):
                for key in itertools.combinations(alias,k):
                    if are_all_abbr(key): continue
                    candidates[frozenset(key)].add(id)
    for aids in candidates.values():
        if len(aids)>17: aids.clear()
    end_do(start)

#3 Find the possible candidates for each author.
def link():
    global authors,sorted_authors,black_list
    start = start_do('link')
    for id,author in authors.items():
        author['candidates'],name = set(),set([x.replace('.','') for x in author['name'].split()])
        for k in range(1,4):
            for key in itertools.combinations(name,k):
                author['candidates'] = author['candidates'].union(candidates[frozenset(key)])
        rich_middle_names = set()
        for candidate in author['candidates']:
            if lack_a_middle_name(author['name'],authors[candidate]['name']): rich_middle_names.add(authors[candidate]['name'])
        if len(rich_middle_names) > 4:
            black_list.add(id)
    for id,author in authors.items():
        sorted_authors.append((id,len(author['candidates'])))
    sorted_authors.sort(key=lambda x:x[1])
    sorted_authors = [x[0] for x in sorted_authors]
    end_do(start)

# A function to marry two authors.
def marryone(id,duplicate,rank):
    new_aids,added_links = duplicates.marry(id,duplicate)
    for aid in new_aids:
        if (id,aid) not in marry_ranks.keys():
            marry_ranks[(id,aid)] = rank
            marry_ranks[(aid,id)] = rank
    if log:
        for link in added_links:
            log.write('[{0}]  {1} ({2})  <==>  {3} ({4})\n'.format(rank,authors[link[0]]['name'],link[0],authors[link[1]]['name'],link[1]))

# The main marry function, the input is different function for select candidates
def marry(func,func_name,rank):
    global duplicates
    start = start_do(func_name)
    for id in sorted_authors:
        possibles = set()
        for candidate in authors[id]['candidates']:
            if candidate==id or ((id in black_list or candidate in black_list) and not are_same_names(authors[id]['name'],authors[candidate]['name'])): continue
            if not func(id,candidate): continue
            possibles.add(candidate)
        possibles_copy = copy.copy(possibles)
        for did in possibles_copy:
            possibles = possibles.union(duplicates.marry(id,did,True)[0])
        if are_similar(set([authors[x]['name'] for x in possibles])):
            for did in possibles:
                marryone(id,did,rank)
    end_do(start)
    print('number of duplicates: {0}'.format(duplicates.nr_duplicates))

def marryb(func,func_name,rank):
    global duplicates
    start = start_do(func_name)
    for id in sorted_authors:
        for candidate in authors[id]['candidates']:
            if candidate==id: continue
            if not func(id,candidate): continue
            marryone(id,candidate,rank)
    end_do(start)
    print('number of duplicates: {0}'.format(duplicates.nr_duplicates))

#4 marry1 marries two authors with the same names.
def marry1():
    def func(a,b):
        a,b = authors[a]['name'],authors[b]['name']
        return are_same_names(a,b)
    marry(func,'marry1',1)

#5 marry2 marries two authors if one author is an abbreviation of the other author. 
#  The first chars of each words of two authors should be the same.
def marry2():
    def func(a,b):
        name_a,name_b = authors[a]['name'],authors[b]['name']
        if authors[a]['is_cn'] and authors[b]['is_cn']: 
            abbr_a,full_a = split_abbr_full(name_a)
            abbr_b,full_b = split_abbr_full(name_b)
            if len(abbr_a)==0 and len(abbr_b)==0:
                return False
        if authors[a]['is_cn'] and len(name_a.split())<=2: return False
        return is_abbr_of(name_a,name_b) and get_first_chars(name_a)==get_first_chars(name_b)
    marry(func,'marry2',2)

#6 marry3 marries two authors if one author is an abbreviation of the other author.
def marry3():
    def func(a,b):
        if authors[a]['is_cn'] and authors[b]['is_cn']: return False
        a,b = authors[a]['name'],authors[b]['name']
        return is_abbr_of(a,b)
    marry(func,'marry3',3)

#7 marry4 marries two authors if one author is an abbreviation of the other author.
#  here string can be parital matched. "Chi Jen Lin" and "Chih Jen Lin" can be the same here.
def marry4():
    def func(a,b):
        if authors[a]['is_cn'] and authors[b]['is_cn']: return False
        a,b = authors[a]['name'],authors[b]['name']
        return is_abbr_of(a,b,True)
    marry(func,'marry4',4)

#8 marry5 marries two authors if one author has more complex aliases that is in the other authors' aliases.
def marry5():
    def func(a,b):
        def remove_simpler(names,base):
            new_names = set()
            for name in names:
                if is_abbr_of(base,name): new_names.add(name)
            return new_names
        a,b = authors[a],authors[b]
        return not remove_simpler(a['aliases'],a['name']).isdisjoint(b['aliases'])
    marry(func,'marry5',5)

#9 marry6 marries two authors if one author has the same affiliations and paper ids with the other authors.
def marry6():
    def func(a,b):
        if authors[a]['is_cn'] and authors[b]['is_cn']: return False
        a,b = authors[a],authors[b]
        if len(a['name'])==0 or len(b['name'])==0 or not may_be_duplicates_partial(a['name'],b['name']): return False
        return not (a['affs'].isdisjoint(b['affs']) and a['pids'].isdisjoint(b['pids']))
    marry(func,'marry6',6)

#10
def marry7():
    def func(a,b):
        a,b = authors[a]['name'],authors[b]['name']
        if len(a)==0 or len(b)==0: return False
        if len(a.split()[-1]) < 3 or len(b.split()[-1]) < 3: return False
        return a.split()[:-1] == b.split()[:-1] and (a.split()[-1][:-1] == b.split()[-1] or b.split()[-1][:-1] == a.split()[-1])
    marry(func,'marry7',7)

#11 marry8 marries a special case:
#   "Michael S. Jordon" and "Michael Jordonn" are duplicates.
def marry8():
    def func(a,b):
        if authors[a]['is_cn'] and authors[b]['is_cn']: return False
        a,b = authors[a]['name'],authors[b]['name']
        if has_middle_name(a)!=has_middle_name(b):
            if has_middle_name(a): a = remove_middle_name(a)
            if has_middle_name(b): b = remove_middle_name(b)
        else:
            return False
        a,b = a.replace(' ',''),b.replace(' ','')
        if a!=b and (a.startswith(b) or b.startswith(a)) and abs(len(a)-len(b))<3: return True
        return False
    marry(func,'marry8',8)

# The input data is generated from preprocessing.
parse_options()
if options['start_stage'] == 0:
    authors,aids = load_pickle_with_timer(options['src']+'.dump',True)
    duplicates = Duplicates(aids)

# No need to see this part, it is for development
for i in range(NR_STAGES):
    path,stage,CUR_STAGE = options['src'] + '.{0}.dump'.format(i),STAGES[i],i
    if options['end_stage']==i: break
    if options['start_stage']==i+1:
        print('skip stage {0}: {1}'.format(i,stage))
        authors,candidates,duplicates,aids,sorted_authors,marry_ranks,black_list = load_pickle_with_timer(path,True)
    elif options['start_stage']<=i:
        eval('{0}()'.format(stage))
        if i>3 and i!=NR_STAGES-1:
            duplicates.write(options['dst']+'.{0}.csv'.format(i-3))
        if options['write'] and i!=NR_STAGES-1:
            dump_pickle_with_timer((authors,candidates,duplicates,aids,sorted_authors,marry_ranks,black_list),path,True)
    else:
        print('skip stage {0}: {1}'.format(i,stage))

duplicates.write(options['dst']+'.csv')
if output_rank:
    start = start_do('writing rank')
    for pair,rank in marry_ranks.items():
        if pair[0]==pair[1]:
            continue
        output_rank.write('{0} {1} {2}\n'.format(rank,pair[0],pair[1]))
    end_do(start)
    output_rank.close()
if log: log.close()

