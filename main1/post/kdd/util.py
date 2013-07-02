__all__ = ['start_do','end_do','is_abbr_name','tokenize_name','extend_name','remove_middle_name','write_track2_submit','read_track2_submit','get_possible_first_names','is_abbr_of_full','are_same_abbrs','are_same_fulls','final_process','fill_indirect_links','are_duplicates','load_pickle_with_timer','dump_pickle_with_timer','extract_full_words','are_same_names','is_abbr_word','is_abbr_of','have_same_aliases','may_be_duplicates','split_abbr_full','is_exact_abbr_of','is_subset_of','have_different_middle_names','get_first_chars','is_chinese_name','lack_a_middle_name','may_be_duplicates_partial','are_similar']

import sys,time,itertools,re,csv,random,collections,copy,pickle
from . stats import *

def start_do(msg):
    sys.stdout.write(msg + '...')
    sys.stdout.flush()
    return time.time()

def end_do(start_time):
    sys.stdout.write("done. {0}\n".format(round(time.time()-start_time,2)))
    sys.stdout.flush()

def tokenize_name(name):
    splitted_name = []
    for word in name.split():
        if len(word)==2 and word.count('.')==0 and word.isupper():
            word = ' '.join(word)
        splitted_name.append(word)
    name = ' '.join(splitted_name)
    name = name.replace("'",'')
    name = name.replace("’",'')
    name = re.sub('[^\w.]',' ',name).lower()
    for pair in SPEC_WORD_PAIRS:
        name = name.replace(pair[0],pair[1])
    splitted_name = []
    for word in name.split():
        if word.replace('.','') in STOPWORDS: continue
        if word in NICKNAME_DICT: word = NICKNAME_DICT[word]
        if word.count('.')>1: word = ' '.join(word.split('.'))
        splitted_name.append(word)
    name = ' '.join(splitted_name)
    name = re.sub(' +',' ',name.encode('ascii','ignore').decode('ascii'))
    return name

def is_abbr_name(name):
    name,nr_full_words = name.split(),0
    for word in name:
        if not is_abbr_word(word): nr_full_words += 1
    return nr_full_words<2

def is_abbr_word(w):
    return w.endswith('.') or len(w)==1

def extend_name(raw,candidates):
    max_nr_full_words,max_nr_words,max_name_len,first_chars_of_raw,best_candidate,new_candidates = 0,len(raw.split()),len(raw),get_first_chars(raw),raw,set()
    for candidate in candidates:
        if is_abbr_of(raw,candidate):
            new_candidates.add(candidate)
    for word in raw.split():
        if not is_abbr_word(word): max_nr_full_words += 1
    for candidate in new_candidates:
        if get_first_chars(candidate)!=first_chars_of_raw: 
            continue
        nr_full_words,nr_words,name_len = 0,len(candidate.split()),len(candidate)
        for word in candidate.split():
            if not is_abbr_word(word): nr_full_words += 1
        if nr_full_words>max_nr_full_words:
            max_nr_full_words,max_nr_words,max_name_len,best_candidate = nr_full_words,nr_words,name_len,candidate
            continue
        if nr_full_words==max_nr_full_words and nr_words>max_nr_words:
            max_nr_words,max_name_len,best_candidate = nr_words,name_len,candidate
            continue
        if nr_full_words==max_nr_full_words and nr_words==max_nr_words and name_len>max_name_len:
            max_name_len,best_candidate = name_len,candidate
            continue
    return best_candidate

def remove_middle_name(name):
    new_name = []
    for word in name.split():
        if is_abbr_word(word): continue
        new_name.append(word)
    return ' '.join(new_name)

def write_track2_submit(path,aids,duplicates,verbose=True):
# f: an opened file
# aids: all author identifiers
# duplicates: a dictionary whose key and value are aid and a set of aid of duplicates, respectively
    #duplicates = final_process(aids,duplicates,verbose)
    if verbose: start = start_do('writing to {0}'.format(path))
    if not (isinstance(duplicates,dict) and isinstance(next(iter(duplicates.values())),set)):
        raise Exception('"duplicates" should be a dictionary whose keys and values are aids and sets of aids of duplicates, respectively')
    f = csv.writer(open(path,'w'))
    f.writerow(['AuthorId','DuplicateAuthorIds'])
    for aid in aids:
        if not aid in duplicates: duplicates[aid] = set()
        duplicates[aid].add(aid)
        f.writerow([str(aid),' '.join(map(str,duplicates[aid]))])
    if verbose: end_do(start)

def read_track2_submit(path):
    start = start_do('reading from {0}'.format(path))
    aids,duplicates = [],{}
    f = csv.reader(open(path,'r'))
    next(f)
    for row in f:
        aid,duplicates_of_author = int(row[0]),set(map(int,row[1].split()))
        aids.append(aid)
        duplicates[aid] = duplicates_of_author
    end_do(start) 
    return aids,duplicates

def get_possible_first_names(name):
    return extract_full_words(name)

def extract_full_words(name):
    full_words = set()
    for word in name.split():
        if is_abbr_word(word): continue
        full_words.add(word) 
    return frozenset(full_words)

def get_first_chars(name):
    if isinstance(name,list):
        name = ' '.join(name)
    first_chars = collections.defaultdict(int)
    for word in name.split():
        first_chars[word[0]] += 1
    return first_chars

def split_abbr_full(name):
    abbr_part,full_part = [],[]
    for word in name.split():
        if is_abbr_word(word):
            abbr_part.append(word.replace('.',''))
        else:
            full_part.append(word)
    return abbr_part,full_part

def is_abbr_of_full(abbr,full):
    full_word_of_abbr = ''
    for word in abbr.split():
        if is_abbr_word(word): continue
        full_word_of_abbr = word
    if full_word_of_abbr=='': return False
    if not full_word_of_abbr in full: return False
    abbr,full = abbr.replace(full_word_of_abbr,''),full.replace(full_word_of_abbr,'')
    first_chars_abbr,first_chars_full = get_first_chars(abbr),get_first_chars(full)
    return first_chars_abbr == first_chars_full
#def is_abbr_of_full(abbrname,fullname):
#    abbrwords_of_abbrname,fullwords_of_abbrname = split_abbr_full(abbrname)
#    abbrwords_of_fullname,fullwords_of_fullname = split_abbr_full(fullname)
#    abbrwords_of_abbrname,fullwords_of_abbrname,abbrwords_of_fullname,fullwords_of_fullname = set(abbrwords_of_abbrname),set(fullwords_of_abbrname),set(abbrwords_of_fullname),set(fullwords_of_fullname)
#    if not fullwords_of_abbrname: return False
#    if not fullwords_of_abbrname.intersection(fullwords_of_fullname): return False
#    common_words = fullwords_of_abbrname.intersection(fullwords_of_fullname)
#    abbrname,fullname = abbrname.split(),fullname.split()
#    for word in common_words:
#        abbrname.remove(word)
#        fullname.remove(word)
#    first_chars_abbr,first_chars_full = get_first_chars(abbrname),get_first_chars(fullname)
#    if len(abbrwords_of_abbrname)<1:
#        return first_chars_abbr == first_chars_full
#    else:
#        diff = 0
#        for char in set(first_chars_abbr.keys()).intersection(set(first_chars_full.keys())):
#            diff += abs(first_chars_abbr[char] - first_chars_full[char])
#        for char in set(first_chars_abbr.keys()).difference(set(first_chars_full.keys())):
#            diff += first_chars_abbr[char]
#        for char in set(first_chars_full.keys()).difference(set(first_chars_abbr.keys())):
#            diff += first_chars_full[char]
#        return diff<2

def are_same_abbrs(a,b):
    if not (is_abbr_name(a) and is_abbr_name(b)): return False
    abbr_a,full_a = split_abbr_full(a)
    abbr_b,full_b = split_abbr_full(b)
    if full_a!=full_b: return False
    return get_first_chars(' '.join(abbr_a)) == get_first_chars(' '.join(abbr_b))

def are_same_fulls(a,b):
    abbr_a,full_a = split_abbr_full(a)
    abbr_b,full_b = split_abbr_full(b)
    abbr_a,full_a,abbr_b,full_b = set(abbr_a),set(full_a),set(abbr_b),set(full_b)
    return (abbr_a.issubset(abbr_b) or abbr_b.issubset(abbr_a)) and (full_a.issubset(full_b) or full_b.issubset(full_a))

def are_same_names(a,b):
    def name2dict(name):
        name_dict = collections.defaultdict(int)
        for word in name.split():
            name_dict[word] += 1
        return name_dict
    if len(a.split()) == 2 and (len(a.split()[0]) < 6 and len(a.split()[1]) < 6):
        return False
    if len(b.split()) == 2 and (len(b.split()[0]) < 6 and len(b.split()[1]) < 6):
        return False
    return name2dict(a.replace('.',' ')) == name2dict(b.replace('.',' '))

def is_abbr_of(a,b,partial=False):
    if are_same_names(a,b): return False
    abbr_part_a,full_part_a = split_abbr_full(a)
    abbr_part_b,full_part_b = split_abbr_full(b)
    common_words = set(abbr_part_a+full_part_a).intersection(set(abbr_part_b+full_part_b))
    for word in common_words:
        if len(word)<2: continue
        if word in abbr_part_a: abbr_part_a.remove(word)
        if word in full_part_a: full_part_a.remove(word)
        if word in abbr_part_b: abbr_part_b.remove(word)
        if word in full_part_b: full_part_b.remove(word)
    abbr_part_b_copy,full_part_b_copy = copy.copy(abbr_part_b),copy.copy(full_part_b)
    for word_a in full_part_a:
        if partial:
            include = False
            for word_b in full_part_b:
                if word_b.startswith(word_a):
                    full_part_b_copy.remove(word_b)
                    include = True
                    break
            if not include: return False
        else:
            if word_a in full_part_b:
                full_part_b_copy.remove(word_a)
            else:
                return False
        full_part_b = full_part_b_copy
    for word_a in abbr_part_a:
        startswith = False
        for word_b in abbr_part_b:
            if word_b.startswith(word_a):
                abbr_part_b_copy.remove(word_b)
                startswith = True
                break
        for word_b in full_part_b:
            if word_b.startswith(word_a):
                full_part_b_copy.remove(word_b)
                startswith = True
                break
        if not startswith: return False
        abbr_part_b,full_part_b = abbr_part_b_copy,full_part_b_copy
    return True

def is_exact_abbr_of(a,b):
    if len(a.split())!=len(b.split()): return False
    return is_abbr_of(a,b)

def is_subset_of(a,b):
    return set(a.split()).issubset(set(b.split()))

def are_duplicates(a,b):
    if is_abbr_name(a):
        if is_abbr_name(b):
            return are_same_abbrs(a,b)
        else:
            return is_abbr_of_full(a,b)
    else:
        if is_abbr_name(b):
            return is_abbr_of_full(b,a)
        else:
            return are_same_fulls(a,b)

def final_process(aids,duplicates,verbose=False):
    if not verbose: start = start_do('final processing')
    new_duplicates = collections.defaultdict(set)
    for aid,duplicated_aids in duplicates.items():
        for duplicated_aid in duplicated_aids:
            if aid not in duplicates[duplicated_aid]:
                if verbose: print('add ({0},{1})'.format(duplicated_aid,aid))
                new_duplicates[duplicated_aid].add(aid)
        new_duplicates[aid] = new_duplicates[aid].union(duplicated_aids)
    duplicates = copy.copy(new_duplicates)
    for aid,duplicated_aids in duplicates.items():
        if aid in BLACK_LIST:
            if verbose: print('remove all duplicates of {0}'.format(aid))
            new_duplicates[aid] = set([aid])
            continue
        new_duplicated_aids = copy.copy(duplicated_aids)
        for duplicated_aid in duplicated_aids:
            if duplicated_aid in BLACK_LIST:
                if verbose: print('remove ({0},{1})'.format(aid,duplicated_aid))
                new_duplicated_aids.remove(duplicated_aid)
        new_duplicates[aid] = new_duplicated_aids
    if not verbose: end_do(start)
    return new_duplicates

def fill_indirect_links(authors,duplicates,verbose=False):
    if not verbose: start = start_do('filling indirect links')
    new_duplicates,counter = copy.copy(duplicates),0
    for aid,duplicated_aids in duplicates.items():
        for aid1,aid2 in itertools.product(duplicated_aids,duplicated_aids):
            if not (aid1 in authors and aid2 in authors): continue
            name1,name2 = tokenize_name(authors[aid1]['name']),tokenize_name(authors[aid2]['name'])
            if are_duplicates(name1,name2):
                if aid2 not in new_duplicates[aid1] or aid1 not in new_duplicates[aid2]:
                    new_duplicates[aid1].add(aid2)
                    new_duplicates[aid2].add(aid1)
                    if verbose: print('{0}  <-->  {1}'.format(authors[aid1]['name'],authors[aid2]['name']))
                    counter += 1
    if not verbose: end_do(start)
    print('{0} links added'.format(counter))
    return new_duplicates

def load_pickle_with_timer(path,verbose=True):
    if verbose: start = start_do('loading from {0}'.format(path))
    dumpobj = pickle.load(open(path,'rb'))
    if verbose: end_do(start)
    return dumpobj

def dump_pickle_with_timer(obj,path,verbose=True):
    if verbose: start = start_do('dumping to {0}'.format(path))
    pickle.dump(obj,open(path,'wb'))
    if verbose: end_do(start)

def have_same_aliases(a,b):
    return a.intersection(b)
    #return len(a.intersection(b))/len(a.union(b)) > 0.5

def may_be_duplicates(a,b):
    return are_same_names(a,b) or is_abbr_of(a,b) or is_abbr_of(b,a)

def may_be_duplicates_partial(a,b):
    return are_same_names(a,b) or is_abbr_of(a,b,True) or is_abbr_of(b,a,True)

def have_different_middle_names(a,b):
    abbr_a,full_a = split_abbr_full(a)
    abbr_b,full_b = split_abbr_full(b)
    if set(full_a)!=set(full_b): return False
    return abbr_a!=abbr_b

def is_chinese_name(name):
    for word in name.split():
        if word in FREQ_FIRST_NAMES:
            return True
    return False

def lack_a_middle_name(a,b):
    abbr_a,full_a = split_abbr_full(a)
    abbr_b,full_b = split_abbr_full(b)
    if set(full_a)==set(full_b) and abs(len(abbr_a)-len(abbr_b))==1: return True
    return False

def are_similar(names):
    total_links,valid_links = 0,0
    for a,b in itertools.combinations(names,2):
        if may_be_duplicates_partial(a,b): valid_links += 1
        total_links += 1
    if total_links<4: return valid_links==total_links
    return valid_links>=0.75*total_links
