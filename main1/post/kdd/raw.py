__all__ = ['Authors','Papers','Pairs','Venues','Duplicates']

import sys,csv,pickle,time,collections
from collections import defaultdict
from operator import itemgetter
from . util import *

class Elements(object):
    def __init__(self,path=None):
        self.elements = {}
        if path is None:
            return
        elif path.endswith('.csv'):
            self.scan(path)
        elif path.endswith('.dump'):
            self.load(path)
        else:
            raise Exception('unknown file type')
    def __getitem__(self,key):
        return self.elements[key]
    def __setitem__(self,key,value):
        self.elements[key] = value
    def __iter__(self):
        for id in self.elements.keys():
            yield id
    def __len__(self):
        return len(self.elements)
    def __contains__(self,id):
        return id in self.elements
    def keys(self):
        for id in self.elements.keys():
            yield id
    def values(self):
        for element in self.elements.values():
            yield element
    def items(self):
        for id,element in self.elements.items():
            yield id,element
    def dump(self,path):
        if not path.endswith('.dump'):
            print('Warning: append ".dump" to {0}'.format(path))
            path = path + '.dump'
        start = start_do("dumping to {0}".format(path))
        pickle.dump(self.elements,open(path,'wb'))
        end_do(start)
    def load(self,path):
        start = start_do("loading from {0}".format(path))
        self.elements = pickle.load(open(path,'rb'))
        end_do(start)
    def write(self,path):
        if not path.endswith('.csv'):
            print('Warning: append ".csv" to {0}'.format(path))
            path = path + '.csv'
        start = start_do("writing to {0}".format(path))
        f = csv.writer(open(path,'w'))
        for id in self.elements.keys():
            self.to_csv(f,id)
        end_do(start)
    def scan(self,path):
        start = start_do("scanning from {0}".format(path))
        for row in csv.reader(open(path,'r')):
            self.parse(row)
        end_do(start)
    def parse(self,row):
        pass
    def to_csv(self,f,id):
        pass

class Authors(Elements):
    def parse(self,row):
        id,name,affiliation = int(row[0]),row[1],row[2]
        self.elements[id] = {'name':name,'affiliation':affiliation}
    def to_csv(self,f,id):
        element = self.elements[id]
        f.writerow([id,element['name'],element['affiliation']])

class Papers(Elements):
    def parse(self,row):
        id,title,year,cid,jid,keywords = int(row[0]),row[1],int(row[2]),int(row[3]),int(row[4]),row[5]
        self.elements[id] = {'title':title,'year':year,'cid':cid,'jid':jid,'keywords':keywords}

class Venues(Elements):
    def parse(self,row):
        id,sname,fname,homepage = int(row[0]),row[1],row[2],row[3]
        self.elements[id] = {'sname':sname,'fname':fname,'homepage':homepage}
    
class Pairs(Elements):
    def __init__(self,path=None):
        super(Pairs,self).__init__(path)
        self.author_dict,self.paper_dict = defaultdict(list),defaultdict(list)
    def extract(self):
        start = start_do("constructing paper and author dictionaries")
        for id,element in self.elements.items():
            self.paper_dict[id[0]].append((id[1],element))
            self.author_dict[id[1]].append((id[0],element))
        end_do(start)
    def parse(self,row):
        pid,aid,name,affiliation = int(row[0]),int(row[1]),row[2],row[3]
        id,element = (pid,aid),{'name':name,'affiliation':affiliation}
        if id in self.elements:
            self.elements[id].append(element)
        else:
            self.elements[id] = [element]
    def to_csv(self,f,id):
        for member in self.elements[id]:
            f.writerow(list(id) + list(member))
    def search_by_aid(self,id):
        try:
            return self.author_dict[id] 
        except:
            return None
    def search_by_pid(self,id):
        try:
            return self.paper_dict[id] 
        except:
            return None

class Duplicates:
    def __init__(self,arg):
        self.duplicates = collections.defaultdict(set)
        self.nr_duplicates = 0
        if isinstance(arg,str):
            if arg.endswith('.dump'):
                self.load(arg)
            elif arg.endswith('.csv'):
                self.read(arg)
            else:
                raise Exception('unknown file type')
        elif isinstance(arg,list):
            for aid in arg:
                self.duplicates[aid].add(aid)
        else:
            raise Exception('invalid argument')
    def dump(self,path):
        dump_pickle_with_timer(self.__dict__,path,True)
    def load(self,path):
        self.__dict__ = load_pickle_with_timer(path,True)
    def write(self,path,verbose=True):
        if verbose: start = start_do('writing to {0}'.format(path))
        f = csv.writer(open(path,'w'))
        f.writerow(['AuthorId','DuplicateAuthorIds'])
        for id,dids in self.duplicates.items():
            f.writerow([str(id),' '.join(map(str,dids))])
        if verbose: end_do(start)
    def read(self,path):
        start = start_do('reading from {0}'.format(path))
        f = csv.reader(open(path,'r'))
        next(f)
        for row in f:
            id,dids = int(row[0]),set(map(int,row[1].split()))
            self.duplicates[id] = dids
        end_do(start) 
    def marry(self,a,b,dryrun=False):
        if b in self.duplicates[a]: return []
        added_relations = []
        if not dryrun: self.nr_duplicates += 1
        for duplicate_of_a in self.duplicates[a]:
            if duplicate_of_a==a: continue
            for duplicate_of_b in self.duplicates[b]:
                if not duplicate_of_b in self.duplicates[duplicate_of_a]:
                    if not dryrun: self.duplicates[duplicate_of_a].add(duplicate_of_b)
                    added_relations.append((duplicate_of_a,duplicate_of_b))
        for duplicate_of_b in self.duplicates[b]:
            if duplicate_of_b==b: continue
            for duplicate_of_a in self.duplicates[a]:
                if not duplicate_of_a in self.duplicates[duplicate_of_b]:
                    if not dryrun: self.duplicates[duplicate_of_b].add(duplicate_of_a)
                    added_relations.append((duplicate_of_b,duplicate_of_a))
        for duplicate_of_b in self.duplicates[b]:
            if not duplicate_of_b in self.duplicates[a]:
                if not dryrun: self.duplicates[a].add(duplicate_of_b)
                added_relations.append((a,duplicate_of_b))
        for duplicate_of_a in self.duplicates[a]:
            if not duplicate_of_a in self.duplicates[b]:
                if not dryrun: self.duplicates[b].add(duplicate_of_a)
                added_relations.append((b,duplicate_of_a))
        return added_relations
    def divorce(self,a):
        if len(self.duplicates[a])==1: return []
        removed_relations,self.nr_duplicates = [],self.nr_duplicates-1
        for did in self.duplicates[a]:
            if did==a: continue
            self.duplicates[did].remove(a)
            removed_relations.append((a,did))
        self.duplicates[a] = set([a])
        return removed_relations
    def are_duplicates(self,duplicates):
        if not duplicates: return False
        first_duplicate = next(iter(duplicates))
        for duplicate in duplicates:
            if duplicate not in self.duplicates[first_duplicate]:
                return False
        return True
    def __getitem__(self,key):
        return self.duplicates[key]
    def __setitem__(self,key,value):
        self.duplicates[key] = value
    def __iter__(self):
        for id in self.duplicates.keys():
            yield id
    def __len__(self):
        return len(self.duplicates)
    def __contains__(self,id):
        return id in self.duplicates
    def keys(self):
        for id in self.duplicates.keys():
            yield id
    def values(self):
        for duplicate in self.duplicates.values():
            yield duplicate
    def items(self):
        for id,duplicate in self.duplicates.items():
            yield id,duplicate
