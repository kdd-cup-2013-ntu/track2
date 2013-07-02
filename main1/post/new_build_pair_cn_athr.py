#!/usr/bin/env python3

import sys,os,collections,re,pickle,copy,itertools
sys.path.append(os.path.join(os.path.dirname(__file__),'..'))
from kdd.raw import *
from kdd.util import *
from kdd.stats import *

NR_STAGES,CUR_STAGE,STAGES,FREQ_THRS,authors,candidates,duplicates,log,aids,sorted_authors,marry_ranks = 11,0,{0:'tokenize',1:'clean',2:'scan',3:'link',4:'marry1',5:'marry2',6:'marry3',7:'marry4',8:'marry5',9:'marry6',10:'marry7'},50,None,collections.defaultdict(set),None,None,None,[],[]

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
-w: dump the result of every stage into the disk
-v <log>: write log'''.format(sys.argv[0]))
    sys.exit(1)

def parse_options():
    global options,log
    if len(sys.argv)<3: exit_with_help()
    options = {'start_stage':0,'end_stage':NR_STAGES,'write':False,'src':sys.argv[-2],'dst':sys.argv[-1]}
    i,argv = 0,sys.argv[1:-2]
    while i < len(argv):
        if argv[i] == '-w':
            options['write'] = True
            i += 1
        elif argv[i] == '-v':
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

def cmp_min_len(a, b):
    min_len = min(len(a), len(b))

    if len(set(a).intersection(set(b))) >= min_len:
        return True
    else:
        return False

def add_duplicate(id,duplicate,rank):
    added_pairs = duplicates.marry(id,duplicate)
    if added_pairs is None: return
    for pair in added_pairs:
        marry_ranks.append((rank,pair))

def tokenize():
    global authors
    start,new_authors = start_do('tokenize'),copy.copy(authors)
    for id,author in authors.items():
        new_authors[id]['name'],new_aliases = tokenize_name(authors[id]['name']),set()
        for name in author['aliases']:
            new_aliases.add(tokenize_name(name))
        new_authors[id]['aliases'] = new_aliases
    authors = new_authors
    end_do(start)

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
            alias = alias.split()
            for k in range(1,4):
                for key in itertools.combinations(alias,k):
                    if are_all_abbr(key): continue
                    candidates[key].add(id)
    for aids in candidates.values():
        if len(aids)>20: aids.clear()
    end_do(start)

def link():
    global authors,sorted_authors
    start = start_do('link')
    for author in authors.values():
        author['candidates'],name = set(),author['name'].split()
        for k in range(1,4):
            for key in itertools.combinations(name,k):
                author['candidates'] = author['candidates'].union(candidates[key])
    for id,author in authors.items():
        sorted_authors.append((id,len(author['candidates'])))
    sorted_authors.sort(key=lambda x:x[1])
    sorted_authors = [x[0] for x in sorted_authors]
    end_do(start)

def marry(func,func_name):
    global duplicates
    start = start_do(func_name)
    for id in sorted_authors:
        a = authors[id]['name']
        for candidate in authors[id]['candidates']:
            if candidate==id: continue
            b = authors[candidate]['name']
            if not func(a,b): continue
            added_relations =  duplicates.marry(id,candidate,True)
            if are_similar(set([authors[x[0]]['name'] for x in added_relations]+[authors[x[1]]['name'] for x in added_relations])):
                duplicates.marry(id,candidate)
    end_do(start)
    print('number of duplicates: {0}'.format(duplicates.nr_duplicates))

def marry1():
    marry(are_same_names,'marry1')

def marry2():
    global duplicates
    start = start_do('marry2')
    for id in sorted_authors:
        a = authors[id]['name']
        for candidate in authors[id]['candidates']:
            if authors[id]['aliases'] != authors[candidate]['aliases']: continue
            if len(authors[id]['affs'].intersection(authors[candidate]['affs'])) > 0:
                duplicates.marry(id,candidate)
    end_do(start)
    print('number of duplicates: {0}'.format(duplicates.nr_duplicates))

def marry3():
    global duplicates
    start = start_do('marry3')
    for id in sorted_authors:
        a_name = authors[id]['name']
        a_abbr,a_full = split_abbr_full(a_name)
        if len(a_abbr) != 0 or len(set(a_full)) < 3: continue
        for candidate in authors[id]['candidates']:
            b_name = authors[candidate]['name']
            b_abbr,b_full = split_abbr_full(b_name)
            if len(b_abbr) != 0 or len(set(b_full)) < 3: continue
            if set(a_full).issubset(set(b_full)) or set(b_full).issubset(set(a_full)):
                duplicates.marry(id,candidate)
    end_do(start)
    print('number of duplicates: {0}'.format(duplicates.nr_duplicates))

def marry4():
    global duplicates
    start = start_do('marry4')
    for id in sorted_authors:
        a_name = authors[id]['name']
        a_ini_list = [x[0] for x in a_name.split()]
        if len(a_ini_list) < 4: continue
        for candidate in authors[id]['candidates']:
            b_name = authors[candidate]['name']
            b_ini_list = [x[0] for x in b_name.split()]
            if len(b_ini_list) < 4: continue
            if a_ini_list == b_ini_list or a_ini_list == ([b_ini_list[-1]] + b_ini_list[:-1]):
                duplicates.marry(id,candidate)
    end_do(start)
    print('number of duplicates: {0}'.format(duplicates.nr_duplicates))

def marry5():
    global duplicates
    start = start_do('marry5')
    for id in sorted_authors:
        a_name = authors[id]['name']
        for candidate in authors[id]['candidates']:
            b_name = authors[candidate]['name']
            if len(a_name.split()[-1]) < 3 or len(b_name.split()[-1]) < 3: continue
            if a_name.split()[:-1] != b_name.split()[:-1]: continue
            if a_name.split()[-1][:-1] == b_name.split()[-1] or b_name.split()[-1][:-1] == a_name.split()[-1]:
                duplicates.marry(id,candidate)
    end_do(start)
    print('number of duplicates: {0}'.format(duplicates.nr_duplicates))

def marry6():
    global duplicates
    start = start_do('marry6')
    for id in sorted_authors:
        a_name = authors[id]['name']
        a_abbr,a_full = split_abbr_full(a_name)
        if len(a_abbr) != 0 or len(set(a_full)) < 3: continue
        for candidate in authors[id]['candidates']:
            b_name = authors[candidate]['name']
            b_abbr,b_full = split_abbr_full(b_name)

            if len(b_full) > 2 and len(a_full) > 2 and cmp_min_len(a_full, b_full):
                duplicates.marry(id,candidate)
    end_do(start)
    print('number of duplicates: {0}'.format(duplicates.nr_duplicates))

def marry7():
    global duplicates
    start = start_do('marry7')
    for id in sorted_authors:
        a_name = authors[id]['name']
        a_abbr,a_full = split_abbr_full(a_name)
        a_ini_list = [x[0] for x in a_name.split()]

        if len(a_abbr) == 2 and len(a_full) == 1: continue
        if len(a_abbr) == 1 and len(a_full) == 2: continue

        for candidate in authors[id]['candidates']:
            b_name = authors[candidate]['name']
            b_abbr,b_full = split_abbr_full(b_name)
            b_ini_list = [x[0] for x in b_name.split()]

            if len(a_ini_list) != 3 or not cmp_min_len(a_full, b_full): continue
            if a_ini_list == b_ini_list: 
                duplicates.marry(id,candidate)
            if a_ini_list[:-1] == b_ini_list[1:] and a_ini_list[-1] == b_ini_list[0]:
                duplicates.marry(id,candidate)
            if b_ini_list[:-1] == a_ini_list[1:] and b_ini_list[-1] == a_ini_list[0]:
                duplicates.marry(id,candidate)

    end_do(start)
    print('number of duplicates: {0}'.format(duplicates.nr_duplicates))

parse_options()
if options['start_stage'] == 0:
    authors,aids = load_pickle_with_timer(options['src'] + '.dump',True)
    duplicates = Duplicates(aids)

for i in range(NR_STAGES):
    path,stage,CUR_STAGE = options['src'] + '.{0}.dump'.format(i),STAGES[i],i
    if options['end_stage']==i: break
    if options['start_stage']==i+1:
        print('skip stage {0}: {1}'.format(i,stage))
        authors,candidates,duplicates,aids,sorted_authors,marry_ranks = load_pickle_with_timer(path,True)
    elif options['start_stage']<=i:
        eval('{0}()'.format(stage))
        if i>3 and i!=NR_STAGES-1:
            duplicates.write(options['dst']+'.{0}.csv'.format(i-3))
        if options['write'] and i!=NR_STAGES-1:
            dump_pickle_with_timer((authors,candidates,duplicates,aids,sorted_authors,marry_ranks),path,True)
    else:
        print('skip stage {0}: {1}'.format(i,stage))

duplicates.write(options['dst']+'.csv')
if log:
    start = start_do('writing log')
    for rank in marry_ranks:
        log.write('{0} {1} {2}\n'.format(rank[0],rank[1][0],rank[1][1]))
    end_do(start)
