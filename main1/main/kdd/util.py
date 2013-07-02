__all__ = ['start_do','end_do','is_abbr_name','tokenize_name','remove_middle_name','is_abbr_of_full','are_same_abbrs','are_same_fulls','are_duplicates','load_pickle_with_timer','dump_pickle_with_timer','are_same_names','is_abbr_word','is_abbr_of','may_be_duplicates','split_abbr_full','is_exact_abbr_of','get_first_chars','lack_a_middle_name','may_be_duplicates_partial','are_similar','has_middle_name']

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

def remove_middle_name(name):
    new_name = []
    for word in name.split():
        if is_abbr_word(word): continue
        new_name.append(word)
    return ' '.join(new_name)

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
    return name2dict(a.replace('.',' ')) == name2dict(b.replace('.',' '))

def is_abbr_of(a,b,partial=False,loose=False):
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
    if not loose:
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
            if not startswith: 
                    return False
            abbr_part_b,full_part_b = abbr_part_b_copy,full_part_b_copy
        return True
    else:
        first_chars_a,first_chars_b = get_first_chars(' '.join(abbr_part_a+full_part_a)),get_first_chars(' '.join(abbr_part_b+full_part_b))
        if not (set(first_chars_b.keys()).issubset(first_chars_a.keys()) or set(first_chars_a.keys()).issubset(first_chars_b.keys())): return False
        if len(abbr_part_a)==0 and len(abbr_part_b)==0:
            for word_a in full_part_a:
                prefix = word_a if len(word_a)<4 else word_a[:3]
                startswith = False
                for word_b in full_part_b:
                    if word_b.startswith(prefix): startswith = True
                if not startswith: return False
        return True

def is_exact_abbr_of(a,b):
    if len(a.split())!=len(b.split()): return False
    return is_abbr_of(a,b)

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

def load_pickle_with_timer(path,verbose=True):
    if verbose: start = start_do('loading from {0}'.format(path))
    dumpobj = pickle.load(open(path,'rb'))
    if verbose: end_do(start)
    return dumpobj

def dump_pickle_with_timer(obj,path,verbose=True):
    if verbose: start = start_do('dumping to {0}'.format(path))
    pickle.dump(obj,open(path,'wb'))
    if verbose: end_do(start)

def may_be_duplicates(a,b):
    return are_same_names(a,b) or is_abbr_of(a,b) or is_abbr_of(b,a)

def may_be_duplicates_partial(a,b,loose=False):
    ret = are_same_names(a,b) or is_abbr_of(a,b,True) or is_abbr_of(b,a,True)
    if loose: ret = ret or is_abbr_of(a,b,True,True) or is_abbr_of(b,a,True,True)
    return ret

def lack_a_middle_name(a,b):
    abbr_a,full_a = split_abbr_full(a)
    abbr_b,full_b = split_abbr_full(b)
    if set(full_a)==set(full_b) and len(full_a)==2 and len(full_b)==2 and len(abbr_a)==0 and len(abbr_b)==1: return True
    return False

def are_similar(names):
    if not names or len(names)==1: return True
    len_of_most_complex_names,most_complex_names = len(next(iter(names)).split()),set()
    for name in names:
        length = len(name.split())
        if length==len_of_most_complex_names: most_complex_names.add(name)
        elif length>len_of_most_complex_names: 
            len_of_most_complex_names = length
            most_complex_names = set((name,))
    for a,b in itertools.combinations(most_complex_names,2): 
        if not may_be_duplicates_partial(a,b,True): return False
    for name in names:
        passed = False
        for complex_name in most_complex_names:
            if may_be_duplicates_partial(name,complex_name,True):
                passed = True
                break
        if not passed: return False
    return True

def has_middle_name(name):
    abbr,full = split_abbr_full(name)
    return len(abbr)==1 and len(full)==2
